# System Patterns

## Architectural Patterns
1. **Three-Stage RAG Pipeline Pattern**
   - Distinct Retrieval → Validation → Generation flow
   - Clear separation between stages with independent error handling
   - Traceable pipeline with performance monitoring at each stage
   - Implementation in `rag_processor.py` with async orchestration

2. **Streaming Response Pattern**
   - Token-by-token delivery to UI for perceived responsiveness
   - Fallback handling for non-streaming models
   - Implemented in `openai_service.py:generate_openai_stream()`
   - Connected to UI via async generator pattern

3. **Validation Filter Pattern**
   - Two-stage content filtering (retrieval + LLM validation)
   - Quality gate ensuring only relevant content passes to generation
   - Parallel processing with async execution in `run_gpt4o_validation_filter_step()`
   - Structured JSON output format for consistent validation results

4. **Observability Integration Pattern**
   - Function-level tracing with `@traceable` decorators from LangSmith
   - Granular performance timing for each processing stage
   - Status logging throughout pipeline for visibility
   - Implementation across all core functions in pipeline

## Code Patterns
1. **Comprehensive Error Handling Pattern**
   - Multi-level try/except blocks with specific exception types
   - Graceful degradation strategies in `rag_processor.py`
   - User-facing error displays with expandable technical details
   - Consistent error propagation from services to UI

2. **Configuration Externalization Pattern**
   - Environment variable management in `config.py`
   - Runtime configuration validation with `check_env_vars()`
   - Separate prompt templates for different pipeline stages
   - UI-configurable parameters with sliders

3. **Status Update Callback Pattern**
   - Callback function pattern for real-time status updates
   - Passed through pipeline functions as `update_status_callback`
   - Consistent status format with timing information
   - Visual status indicators in Streamlit UI

4. **Service Initialization Pattern**
   - Lazy initialization with health checking in `init_retriever()` and `init_openai_client()`
   - Service status tracking via global state
   - Clear status reporting with detailed error messages
   - Auto-retry logic for transient failures

5. **Embedding Generation Pattern**
   - Rate limit handling with exponential backoff
   - Text preprocessing before embedding generation
   - Multiple retry attempts for API resilience
   - Implementation in `utils.py:get_embedding()`

## UI Patterns
1. **Expandable Context Pattern**
   - Collapsible sections for source text display
   - Citation-based filtering of displayed sources
   - Implementation in `display_chat_message()` function
   - Strategic use of Streamlit expanders

2. **RTL Text Handling Pattern**
   - Consistent RTL markers with `dir='rtl'` attributes
   - CSS classes for Hebrew text styling
   - Proper text direction management in HTML components
   - Implementation throughout UI rendering functions

3. **Interactive Configuration Pattern**
   - Sidebar controls for pipeline parameters
   - Dynamic parameter adjustment based on other settings
   - Parameter validation (e.g., max validation count)
   - Implementation in `display_sidebar()` function

4. **Citation Integration Pattern**
   - Source numbering with regex-based citation detection
   - Source expansion based on citation references
   - Implementation in `re.findall(r'מקור[\s\u00A0\u2000-\u200F...)` 
   - Automatic highlighting of cited sources in UI

## Implementation Patterns
1. **Content Processing Pattern**
   - Text cleaning with regex normalization
   - Consistent source formatting for model input
   - Structure-preserving text transformations
   - Implementation in `clean_source_text()` and `format_context_for_openai()`

2. **Async Execution Pattern**
   - Parallel validation with `asyncio.gather(*tasks)`
   - Event loop management with `nest_asyncio`
   - Streaming response handling with async generators
   - Implementation throughout the pipeline for performance

3. **Response Construction Pattern**
   - Structured formatting of documents for context
   - Clear headers for source attribution
   - Consistent response assembly in generation step
   - Implementation in `format_context_for_openai()`

4. **Session State Management Pattern**
   - Chat history preservation in Streamlit session state
   - Message structure with metadata for rendering
   - UI state management for expandable sections
   - Implementation in app.py message handling 