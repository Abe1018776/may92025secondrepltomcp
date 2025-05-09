import openai
import traceback
import json
import asyncio
from typing import Dict, Optional, Tuple, List, AsyncGenerator, Set
from langsmith import traceable

try:
    import config
    from utils import format_context_for_openai
except ImportError:
    # More detailed error handling for better debugging
    print("Error: Failed to import config or utils in openai_service.py")
    traceback.print_exc()
    print("Current directory:", __file__)
    raise SystemExit("Failed imports in openai_service.py")

# --- Globals ---
openai_async_client: Optional[openai.AsyncOpenAI] = None
is_openai_ready: bool = False
openai_status_message: str = "OpenAI service not initialized."

# --- Initialization ---
def init_openai_client() -> Tuple[bool, str]:
    """Initializes the OpenAI async client."""
    global openai_async_client, is_openai_ready, openai_status_message
    if is_openai_ready:
        return True, openai_status_message
    if not config.OPENAI_API_KEY:
        openai_status_message = "Error: OPENAI_API_KEY not found in Secrets."
        is_openai_ready = False
        return False, openai_status_message
    try:
        openai_async_client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        openai_status_message = (
            f"OpenAI service ready (Validate: {config.OPENAI_VALIDATION_MODEL}, "
            f"Generate: {config.OPENAI_GENERATION_MODEL})."
        )
        is_openai_ready = True
        print("OpenAI Service: Async client initialized.")
        return True, openai_status_message
    except Exception as e:
        error_msg = f"Error initializing OpenAI async client: {type(e).__name__} - {e}"
        print(error_msg)
        traceback.print_exc()
        openai_status_message = error_msg
        is_openai_ready = False
        openai_async_client = None
        return False, openai_status_message


def get_openai_status() -> Tuple[bool, str]:
    """Returns the current status of the OpenAI service."""
    if not is_openai_ready:
        init_openai_client()
    return is_openai_ready, openai_status_message

# --- Validation Function (uses template) ---
@traceable(name="openai-validate-paragraph")
async def validate_relevance_openai(
    paragraph_data: Dict, user_question: str, paragraph_index: int
) -> Optional[Dict]:
    global openai_async_client
    ready, msg = get_openai_status()
    if not ready or openai_async_client is None:
        print(f"OpenAI validation failed (Para {paragraph_index+1}): Client not ready - {msg}")
        return None

    safe_paragraph_data = paragraph_data.copy() if isinstance(paragraph_data, dict) else {}
    hebrew_text = paragraph_data.get('hebrew_text', '').strip()
    english_text = paragraph_data.get('english_text', '').strip()
    if not hebrew_text and not english_text:
        return {
            "validation": {"contains_relevant_info": False, "justification": "Paragraph text empty."},
            "paragraph_data": safe_paragraph_data
        }

    validation_model = config.OPENAI_VALIDATION_MODEL
    prompt_content = config.VALIDATION_PROMPT_TEMPLATE.format(
        user_question=user_question,
        paragraph_index=paragraph_index+1,
        hebrew_text=hebrew_text or "(No Hebrew)",
        english_text=english_text or "(No English)"
    )

    try:
        response = await openai_async_client.chat.completions.create(
            model=validation_model,
            messages=[{"role": "user", "content": prompt_content}],
            temperature=0.1,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        validation_result = json.loads(response.choices[0].message.content)
        return {"validation": validation_result, "paragraph_data": safe_paragraph_data}
    except Exception as e:
        print(f"Error (OpenAI Validate {paragraph_index+1}): {e}")
        traceback.print_exc()
        return {
            "validation": {"contains_relevant_info": False, "justification": "Error during validation."},
            "paragraph_data": safe_paragraph_data
        }

# --- Generation Function (unchanged) ---
@traceable(name="openai-generate-stream")
async def generate_openai_stream(
    messages: List[Dict],
    context_documents: List[Dict],
    dynamic_system_prompt: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Generates a response using OpenAI GPT model based on history and context.
    Falls back to non-streaming for o-series models if streaming fails.
    
    If dynamic_system_prompt is provided, it will be used instead of the static 
    system prompt from config.
    """
    global openai_async_client
    ready, msg = get_openai_status()
    if not ready or openai_async_client is None:
        yield f"--- Error: OpenAI client not available: {msg} ---"
        return

    # Format context
    if not isinstance(context_documents, list) or not all(isinstance(item, dict) for item in context_documents):
        yield "--- Error: Invalid context_documents format ---"
        return
    formatted_context = format_context_for_openai(context_documents)
    if not formatted_context or formatted_context.startswith("No"):
        yield "--- Error: No valid context provided ---"
        return

    last_user = next((m['content'] for m in reversed(messages) if m.get('role')=='user'), "")
    user_prompt = (
        f"Source Texts:\n{formatted_context}\n\n"
        f"User Question:\n{last_user}\n\n"
        "Answer (in Hebrew, based ONLY on the Source Texts provided):"
    )
    
    # Use dynamic system prompt if provided, otherwise fall back to the static one
    sys_msg = dynamic_system_prompt if dynamic_system_prompt else config.OPENAI_SYSTEM_PROMPT
    
    # Print a log message to show we're using the dynamic prompt
    if dynamic_system_prompt:
        print(f"Using dynamic system prompt (length: {len(dynamic_system_prompt)})")
    else:
        print("Using default system prompt from config")
        
    api_messages = [{"role":"system","content":sys_msg},{"role":"user","content":user_prompt}]

    model = config.OPENAI_GENERATION_MODEL
    print(f"Using generation model: {model}")

    # Determine token parameter
    token_key = "max_completion_tokens" if model.startswith(("o1","o3","o4")) else "max_tokens"
    kwargs = {"model":model, "messages":api_messages, token_key:3000}

    # Attempt streaming for non-o-series
    if not model.startswith(("o1","o3","o4")):
        kwargs.update({"stream":True, "temperature":0.5})
        try:
            stream = await openai_async_client.chat.completions.create(**kwargs)
            async for chunk in stream:
                c = chunk.choices[0].delta.content
                if c:
                    yield c
            return
        except Exception as e:
            print(f"Streaming failed for model {model}: {e}")
            traceback.print_exc()

    # Fallback or direct call (o-series or streaming error)
    try:
        resp = await openai_async_client.chat.completions.create(**kwargs)
        text = resp.choices[0].message.content
        yield text
    except Exception as e:
        err = f"--- Error generating response: {e} ---"
        print(err)
        traceback.print_exc()
        yield err

# --- Citation Extraction Function ---
@traceable(name="openai-extract-citations")
async def extract_citations_with_openai(text: str) -> Set[str]:
    """
    Extract citation numbers from a response text using OpenAI.
    Returns a set of citation IDs as strings.
    Returns empty set if extraction fails.
    """
    global openai_async_client
    ready, msg = get_openai_status()
    if not ready or openai_async_client is None or not text:
        print(f"OpenAI citation extraction failed: Client not ready - {msg}")
        return set()
    
    try:
        response = await openai_async_client.chat.completions.create(
            model=config.OPENAI_VALIDATION_MODEL,
            messages=[
                {"role": "system", "content": "Extract all source citation numbers mentioned in the Hebrew text. Citations may appear in various formats like 'מקור X', 'מקורות X, Y, Z', 'מקור X, ראה Y', or similar patterns where X, Y, Z are numbers. Return only a JSON object with 'citations' containing an array of strings representing all the numbers found."},
                {"role": "user", "content": f"Text: {text}\n\nExtract all source citation numbers and return as JSON."}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=150
        )
        
        result = json.loads(response.choices[0].message.content)
        citations = result.get("citations", [])
        print(f"OpenAI citation extraction found: {citations}")
        return set(str(c) for c in citations)
    except Exception as e:
        print(f"Error during OpenAI citation extraction: {e}")
        traceback.print_exc()
        return set()
