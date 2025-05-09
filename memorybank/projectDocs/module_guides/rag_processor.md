# RAG Processor Module Guide

## Overview
The `rag_processor.py` module serves as the central implementation of the Retrieval-Augmented Generation (RAG) pipeline in the Divrei Yoel AI Chat application. It orchestrates a three-stage process (Retrieve → Validate → Generate) to produce high-quality responses based on relevant Hebrew texts.

## Architecture
The processor implements a modular pipeline with the following key components:

### Pipeline Structure
```
┌───────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ 1. Retrieval  │────>│ 2. Validation     │────>│ 3. Generation     │
│   (Pinecone)  │     │     (GPT-4o)      │     │     (GPT-4o)      │
└───────────────┘     └───────────────────┘     └───────────────────┘
```

### Key Functions

#### 1. `run_retrieval_step`
```python
@traceable(name="rag-step-retrieve")
async def run_retrieval_step(query: str, n_retrieve: int, update_status: StatusCallback) -> List[Dict]
```
- **Purpose**: Retrieves potentially relevant documents from vector database
- **Parameters**:
  - `query`: User's query text
  - `n_retrieve`: Number of documents to retrieve
  - `update_status`: Callback for status updates
- **Returns**: List of retrieved documents
- **Tracing**: Integrated with LangSmith for observability
- **Internationalization**: Uses i18n for status messages

#### 2. `run_gpt4o_validation_filter_step`
```python
@traceable(name="rag-step-gpt4o-filter")
async def run_gpt4o_validation_filter_step(
    docs_to_process: List[Dict], query: str, n_validate: int, update_status: StatusCallback
) -> List[Dict]
```
- **Purpose**: Filters retrieved documents by validating relevance using GPT-4o
- **Parameters**:
  - `docs_to_process`: Retrieved documents to validate
  - `query`: Original user query
  - `n_validate`: Maximum number of documents to validate
  - `update_status`: Callback for status updates
- **Returns**: Filtered list of validated documents
- **Key Features**:
  - Parallel processing using `asyncio.gather`
  - Structured validation output with relevance scores
  - Comprehensive error handling for validation failures
- **Internationalization**: Uses i18n for status messages

#### 3. `run_openai_generation_step`
```python
@traceable(name="rag-step-openai-generate")
async def run_openai_generation_step(
    history: List[Dict], context_documents: List[Dict],
    update_status: StatusCallback, stream_callback: Callable[[str], None],
    dynamic_system_prompt: Optional[str] = None
) -> Tuple[str, Optional[str]]
```
- **Purpose**: Generates the final response using validated documents
- **Parameters**:
  - `history`: Conversation history
  - `context_documents`: Validated documents to use as context
  - `update_status`: Callback for status updates
  - `stream_callback`: Callback for streaming tokens
  - `dynamic_system_prompt`: Optional custom system prompt
- **Returns**: Tuple of (response_text, error_message)
- **Key Features**:
  - Streaming response generation
  - Dynamic system prompt support
  - Comprehensive error handling
  - Internationalization support

#### 4. `execute_validate_generate_pipeline`
```python
@traceable(name="rag-execute-validate-generate-gpt4o-pipeline")
async def execute_validate_generate_pipeline(
    history: List[Dict], params: Dict[str, Any],
    status_callback: StatusCallback, stream_callback: Callable[[str], None],
    dynamic_system_prompt: Optional[str] = None
) -> Dict[str, Any]
```
- **Purpose**: Main entrypoint that orchestrates the entire RAG pipeline
- **Parameters**:
  - `history`: Conversation history
  - `params`: Configuration parameters (includes `n_retrieve` and `n_validate`)
  - `status_callback`: Callback for status updates
  - `stream_callback`: Callback for streaming tokens
  - `dynamic_system_prompt`: Optional custom system prompt
- **Returns**: Dictionary with results and metadata:
  ```python
  {
      "final_response": str,           # Generated response text
      "validated_documents_full": List, # Complete validated docs
      "generator_input_documents": List, # Docs used for generation
      "status_log": List[str],         # Status updates log
      "error": Optional[str],          # Error message if any
      "pipeline_used": str             # Pipeline identifier
  }
  ```
- **Process Flow**:
  1. Extract the current query from history
  2. Run retrieval step
  3. Run validation step
  4. Simplify documents for generation
  5. Run generation step
  6. Return comprehensive results including documents and status

## Error Handling
The module implements robust error handling at multiple levels:
- Per-step try/except blocks with graceful degradation
- Detailed status updates for user feedback
- Error logging with traceback capture
- Structured error responses with user-friendly formatting
- HTML formatting for error messages to match app styling

## Internationalization
Status messages use the i18n (internationalization) module for proper translation support:
```python
update_status(get_text("retrieving_docs").format(n_retrieve))
```
This ensures consistent user experience across languages while maintaining Hebrew as the primary focus.

## Tracing and Observability
Each pipeline step is decorated with LangSmith's `@traceable` decorator:
```python
@traceable(name="rag-step-retrieve")
async def run_retrieval_step(...):
```
This provides:
- Performance metrics collection
- Input/output capture for debugging
- Error tracking in a central dashboard
- Trace correlation across pipeline steps

## Implementation Notes

### Document Processing
The pipeline processes documents in these stages:
1. **Retrieval**: Gets initial batch of documents
2. **Validation**: Filters for relevance using LLM
3. **Preparation**: Simplifies documents for generation:
   ```python
   simplified_doc = {
       'hebrew_text': hebrew_text,
       'original_id': doc.get('original_id', 'unknown'),
       'source_name': doc.get('source_name')
   }
   ```

### Callback System
The module uses a callback system for real-time updates:
- `status_callback`: For detailed progress updates
- `stream_callback`: For streaming response chunks

## Usage Example
```python
# Execute the pipeline
result = await execute_validate_generate_pipeline(
    history=conversation_history,
    params={"n_retrieve": 50, "n_validate": 25},
    status_callback=update_status_ui,
    stream_callback=update_response_ui
)

# Access results
response_text = result["final_response"]
sources = result["generator_input_documents"]
log = result["status_log"]
``` 