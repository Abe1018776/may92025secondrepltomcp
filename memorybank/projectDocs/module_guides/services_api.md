# Services Module Guide

## Overview
The `services` directory contains modules that manage external API connections for the Divrei Yoel AI Chat application. It provides clean abstractions for OpenAI and retrieval services, handling authentication, connection management, and error handling.

## OpenAI Service (`openai_service.py`)

### Key Components
```
┌───────────────────────────────────┐
│ openai_service.py                 │
├───────────────────────────────────┤
│ ┌─────────────────────────────┐   │
│ │ Initialization              │   │
│ └─────────────────────────────┘   │
│                                   │
│ ┌─────────────────────────────┐   │
│ │ Validation                  │   │
│ └─────────────────────────────┘   │
│                                   │
│ ┌─────────────────────────────┐   │
│ │ Generation                  │   │
│ └─────────────────────────────┘   │
│                                   │
│ ┌─────────────────────────────┐   │
│ │ Citation Extraction         │   │
│ └─────────────────────────────┘   │
└───────────────────────────────────┘
```

### Client Initialization
```python
def init_openai_client() -> Tuple[bool, str]:
    """Initializes the OpenAI async client."""
```
- Creates and configures the OpenAI async client
- Validates API key presence
- Returns initialization status (bool) and message (str)

### Status Checking
```python
def get_openai_status() -> Tuple[bool, str]:
    """Returns the current status of the OpenAI service."""
```
- Provides real-time status of the OpenAI service
- Initializes the client if needed
- Returns a tuple of (status_boolean, status_message)

### Validation Function
```python
@traceable(name="openai-validate-paragraph")
async def validate_relevance_openai(
    paragraph_data: Dict, user_question: str, paragraph_index: int
) -> Optional[Dict]:
```
- Validates the relevance of a paragraph to a user question
- Uses OpenAI's models to perform validation
- Returns a dictionary with validation results
- Integrated with LangSmith tracing for observability

### Generation Function
```python
@traceable(name="openai-generate-stream")
async def generate_openai_stream(
    messages: List[Dict],
    context_documents: List[Dict],
    dynamic_system_prompt: Optional[str] = None
) -> AsyncGenerator[str, None]:
```
- Generates a response using OpenAI models with streaming
- Supports custom system prompts
- Falls back to non-streaming for o-series models if streaming fails
- Returns an async generator that yields response chunks
- Integrated with LangSmith tracing

### Citation Extraction Function
```python
@traceable(name="openai-extract-citations")
async def extract_citations_with_openai(text: str) -> Set[str]:
```
- Extracts citation numbers from response text using OpenAI
- Returns a set of citation IDs as strings
- Returns empty set if extraction fails
- Integrated with LangSmith tracing

## Retriever Service (`retriever.py`)

### Key Functions

```python
def init_retriever() -> Tuple[bool, str]:
    """Initialize the document retriever with configuration."""
```
- Establishes connection to vector database
- Validates all required configuration parameters
- Returns initialization status (bool) and message (str)

```python
def retrieve_documents(query_text: str, n_results: int = 10) -> List[Dict]:
    """Retrieve documents similar to the query text."""
```
- Performs vector similarity search
- Formats and returns document results
- Supports configurable result count
- Includes error handling for service unavailability

## Error Handling
Both services implement comprehensive error handling:
- Exception catching for all external API calls
- Detailed logging with error messages
- User-friendly status messages
- Graceful degradation when services are unavailable

## Thread Safety
The services ensure thread safety for connections:
- Global client variables with proper initialization
- Error handling for concurrent access
- Proper async/await handling in OpenAI service

## Tracing & Observability
- All key OpenAI functions use `@traceable` decorator from LangSmith
- Functions include custom trace names for better identification
- Errors are properly reported and captured in traces

## Usage Example
```python
# Initialize services
retriever_ready, retriever_msg = init_retriever()
openai_ready, openai_msg = init_openai_client()

# Retrieve documents
docs = retrieve_documents(query_text="Some user query", n_results=20)

# Validate relevance
validation_results = await validate_relevance_openai(docs[0], "User question", 0)

# Generate response
async for chunk in generate_openai_stream(messages, docs):
    # Process streaming chunks
    process_chunk(chunk)

# Extract citations
citations = await extract_citations_with_openai(response_text) 