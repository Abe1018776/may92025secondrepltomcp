import time
import asyncio
import traceback
from typing import List, Dict, Any, Optional, Callable, Tuple
from langsmith import traceable

try:
    import config
    from services import retriever, openai_service
    from i18n import get_text
except ImportError:
    print("Error: Failed to import config, services, or i18n in rag_processor.py")
    raise SystemExit("Failed imports in rag_processor.py")

PIPELINE_VALIDATE_GENERATE_GPT4O = "GPT-4o Validator + GPT-4o Synthesizer"
StatusCallback = Callable[[str], None]

# --- Step Functions ---

@traceable(name="rag-step-retrieve")
async def run_retrieval_step(query: str, n_retrieve: int, update_status: StatusCallback, original_query: str = None) -> List[Dict]:
    """
    Retrieve documents from the vector store.

    Args:
        query (str): The full query text (may include template)
        n_retrieve (int): Number of documents to retrieve
        update_status (StatusCallback): Status update callback function
        original_query (str, optional): The original user query without template

    Returns:
        List[Dict]: List of retrieved documents
    """
    # Import inside function to avoid circular imports
    from i18n import get_text
    from services.retriever import retrieve_documents

    # Use original query for Pinecone search if provided
    search_query = original_query if original_query else query

    update_status(get_text("retrieving_docs").format(n_retrieve))
    start_time = time.time()
    retrieved_docs = await retrieve_documents(query_text=search_query, n_results=n_retrieve)
    retrieval_time = time.time() - start_time
    update_status(get_text("retrieved_docs").format(len(retrieved_docs), f"{retrieval_time:.2f}"))
    if not retrieved_docs:
        update_status(get_text("no_docs_found"))
    return retrieved_docs

@traceable(name="rag-step-gpt4o-filter")
async def run_gpt4o_validation_filter_step(
    docs_to_process: List[Dict], query: str, n_validate: int, update_status: StatusCallback
) -> List[Dict]:
    if not docs_to_process:
        update_status(get_text("skipping_validation"))
        return []
    validation_count = min(len(docs_to_process), n_validate)
    update_status(get_text("validating_docs").format(validation_count, len(docs_to_process)))
    validation_start_time = time.time()
    tasks = [openai_service.validate_relevance_openai(doc, query, i)
             for i, doc in enumerate(docs_to_process[:validation_count])]
    validation_results = await asyncio.gather(*tasks, return_exceptions=True)
    passed_docs = []
    passed_count = failed_validation_count = error_count = 0
    update_status(get_text("filtering_docs"))
    for i, res in enumerate(validation_results):
        original_doc = docs_to_process[i]
        if isinstance(res, Exception):
            print(f"GPT-4o Validation Exception doc {i}: {res}")
            error_count += 1
        elif isinstance(res, dict) and 'validation' in res:
            if res['validation'].get('contains_relevant_info')):
                original_doc['validation_result'] = res['validation']
                passed_docs.append(original_doc)
                passed_count += 1
            else:
                failed_validation_count += 1
        else:
            print(f"GPT-4o Validation Unexpected result doc {i}: {type(res)}")
            error_count += 1
    validation_time = time.time() - validation_start_time
    update_status(get_text("validation_complete").format(
        passed_count, failed_validation_count, error_count, f"{validation_time:.2f}"
    ))
    update_status(get_text("filtered_docs").format(len(passed_docs)))
    return passed_docs

@traceable(name="rag-step-openai-generate")
async def run_openai_generation_step(
    history: List[Dict], context_documents: List[Dict],
    update_status: StatusCallback, stream_callback: Callable[[str], None],
    dynamic_system_prompt: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    generator_name = "OpenAI"
    if not context_documents:
        update_status(get_text("skipping_generation").format(generator_name))
        return get_text("no_sources_for_response"), None
    update_status(get_text("generating_response").format(generator_name, len(context_documents)))
    start_gen_time = time.time()
    try:
        full_response = []
        error_msg = None
        generator = openai_service.generate_openai_stream(
            messages=history, context_documents=context_documents, 
            dynamic_system_prompt=dynamic_system_prompt
        )
        async for chunk in generator:
            if isinstance(chunk, str) and chunk.strip().startswith("--- Error:"):
                if not error_msg:
                    error_msg = chunk.strip()
                print(f"OpenAI stream yielded error: {chunk.strip()}")
                break
            if isinstance(chunk, str):
                full_response.append(chunk)
                stream_callback(chunk)
        final_response_text = "".join(full_response)
        gen_time = time.time() - start_gen_time
        if error_msg:
            update_status(get_text("generation_error").format(generator_name, f"{gen_time:.2f}"))
            return final_response_text, error_msg
        update_status(get_text("generation_complete").format(generator_name, f"{gen_time:.2f}"))
        return final_response_text, None
    except Exception as gen_err:
        gen_time = time.time() - start_gen_time
        error_msg_critical = (f"--- Error: Critical failure during {generator_name} generation "
                              f"({type(gen_err).__name__}): {gen_err} ---")
        update_status(get_text("generation_critical_error").format(generator_name, f"{gen_time:.2f}"))
        traceback.print_exc()
        return "", error_msg_critical

@traceable(name="rag-execute-validate-generate-gpt4o-pipeline")
async def execute_validate_generate_pipeline(
    history: List[Dict], params: Dict[str, Any],
    status_callback: StatusCallback, stream_callback: Callable[[str], None],
    dynamic_system_prompt: Optional[str] = None
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "final_response": "",
        "validated_documents_full": [],
        "generator_input_documents": [],
        "status_log": [],
        "error": None,
        "pipeline_used": PIPELINE_VALIDATE_GENERATE_GPT4O
    }
    status_log_internal: List[str] = []

    def update_status_and_log(message: str):
        print(f"Status Update: {message}")
        status_log_internal.append(message)
        status_callback(message)

    current_query_text = ""
    if history and isinstance(history, list):
        for msg_ in reversed(history):
            if isinstance(msg_, dict) and msg_.get("role") == "user":
                current_query_text = str(msg_.get("content") or "")
                break
    if not current_query_text:
        result["error"] = get_text("error")
        result["final_response"] = f"<div class='rtl-text'>{result['error']}</div>"
        result["status_log"] = status_log_internal
        return result

    try:
        # Extract original query for search if present
        original_query = params.get('original_query')

        # 1. Retrieval
        start_time_retrieval = time.time()
        update_status_and_log(f"1. Retrieving up to {params['n_retrieve']} paragraphs from Pinecone...")
        retrieved_docs = await run_retrieval_step(
            current_query_text, params['n_retrieve'], update_status_and_log, original_query
        )
        time_retrieval = time.time() - start_time_retrieval
        if not retrieved_docs:
            result["error"] = get_text("no_docs_found")
            result["final_response"] = f"<div class='rtl-text'>{result['error']}</div>"
            result["status_log"] = status_log_internal
            return result

        # 1. Retrieval completed
        update_status_and_log(f"1. Retrieved {len(retrieved_docs)} paragraphs in {round(time_retrieval, 2)} seconds.")

        # 2. Validation
        start_time_validation = time.time()
        update_status_and_log(f"2. [GPT-4o] Starting parallel validation ({len(retrieved_docs)} / {params['n_validate']} paragraphs)...")
        validation_results = await openai_service.validate_documents(retrieved_docs, current_query_text)
        time_validation = time.time() - start_time_validation
        update_status_and_log(f"2. GPT-4o validation complete ({len(validation_results['passed'])} passed, {len(validation_results['rejected'])} rejected, {len(validation_results['errors'])} errors) in {round(time_validation, 2)} seconds.")

        # 3. Filtering by validation results
        update_status_and_log("3. [GPT-4o] Filtering paragraphs based on validation results...")
        validated_docs_full = [doc for doc in validation_results['passed_docs']]
        update_status_and_log(f"3. Collected {len(validated_docs_full)} relevant paragraphs after GPT-4o validation.")
        result["validated_documents_full"] = validated_docs_full

        if not validated_docs_full:
            result["error"] = get_text("no_relevant_passages")
            result["final_response"] = f"<div class='rtl-text'>{result['error']}</div>"
            update_status_and_log(f"4. {result['error']} {get_text('generation_critical_error')}")
            return result
            
        # --- Simplify Docs for Generation ---
        simplified_docs_for_generation: List[Dict[str, Any]] = []
        print(f"Processor: Simplifying {len(validated_docs_full)} docs...")
        for doc in validated_docs_full:
            if isinstance(doc, dict):
                hebrew_text = doc.get('hebrew_text', '')
                validation = doc.get('validation_result')
                if hebrew_text:
                    simplified_doc: Dict[str, Any] = {
                        'hebrew_text': hebrew_text,
                        'original_id': doc.get('original_id', 'unknown')
                    }
                    if doc.get('source_name'):
                        simplified_doc['source_name'] = doc.get('source_name')
                    if validation is not None:
                        simplified_doc['validation_result'] = validation  # include judgment
                    simplified_docs_for_generation.append(simplified_doc)
            else:
                print(f"Warn: Skipping non-dict item: {doc}")
        result["generator_input_documents"] = simplified_docs_for_generation
        print(f"Processor: Created {len(simplified_docs_for_generation)} simplified docs with validation results.")
        
        # 4. Generation
        pipeline = PIPELINE_VALIDATE_GENERATE_GPT4O # GPT-4o
        start_time_generation = time.time()
        update_status_and_log(f"4. [{pipeline}] Generating final response from {len(validated_docs_full)} context passages...")

        final_response_text, generation_error = await run_openai_generation_step(
            history=history,
            context_documents=simplified_docs_for_generation,
            update_status=update_status_and_log,
            stream_callback=stream_callback,
            dynamic_system_prompt=dynamic_system_prompt
        )
        time_generation = time.time() - start_time_generation
        
        # 5. Generation completed
        update_status_and_log(f"4. Response generation ({pipeline}) completed in {round(time_generation, 2)} seconds.")
        
        result["final_response"] = final_response_text
        result["error"] = generation_error

        if generation_error and not result["final_response"].strip().startswith(("<div", get_text("no_sources_for_response"))):
            result["final_response"] = (
                f"<div class='rtl-text'><strong>{get_text('generation_error').format(pipeline, '')}</strong><br>"
                f"{get_text('details')}: {generation_error}<br>---<br>{result['final_response']}</div>"
            )
        elif result["final_response"] == get_text("no_sources_for_response"):
            result["final_response"] = f"<div class='rtl-text'>{result['final_response']}</div>"

    except Exception as e:
        error_type = type(e).__name__
        error_msg = f"{get_text('critical_error')} RAG ({error_type}): {e}"
        print(f"Critical RAG Error: {error_msg}")
        traceback.print_exc()
        result["error"] = error_msg
        result["final_response"] = (
            f"<div class='rtl-text'><strong>{get_text('critical_error')} ({error_type})</strong><br>{get_text('reload')}"
            f"<details><summary>{get_text('details')}</summary><pre>{traceback.format_exc()}</pre></details></div>"
        )
        update_status_and_log(f"{get_text('critical_error')}: {error_type}")

    result["status_log"] = status_log_internal
    return result