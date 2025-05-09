# Configuration Module Guide

## Overview
The `config.py` module serves as the central configuration hub for the Divrei Yoel AI Chat application. It contains environment variable handling, default settings, and configuration parameters that control the behavior of the RAG pipeline and UI components.

## Environment Variables Management

### Loading Environment Variables
```python
dot_env_path = os.path.join(os.path.dirname(__file__), '.env')

# If on a platoform like Hugging Face, the .env file is not needed and we should use load_dotenv with no arguments
if os.path.exists(dot_env_path):
    load_dotenv(dotenv_path=dot_env_path, verbose=True, override=True, stream=sys.stdout)
else:
    load_dotenv()
```
- Uses python-dotenv to load variables from .env file
- Handles both local development (.env file exists) and deployment scenarios (environment variables)
- Provides diagnostics via verbose mode when loading local .env files
- Supports platforms like Hugging Face with different environment handling

### API Keys Configuration
```python
# --- API Keys (Required) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
```
- Loads critical API keys for OpenAI and Pinecone services
- Uses os.environ.get() for consistent environment variable access
- No hardcoded defaults for security reasons

## LangSmith Tracing Configuration

```python
# --- LangSmith Configuration ---
LANGSMITH_ENDPOINT = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING", "true")
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "DivreyYoel-RAG-GPT4-Gen")
```
- Configures LangSmith for tracing and observability
- Sets default endpoint and project name
- Enables/disables tracing via environment variable
- Supports custom LangSmith API key

## Model Configuration

```python
# --- Model Configuration ---
EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_VALIDATION_MODEL = os.environ.get("OPENAI_VALIDATION_MODEL", "gpt-4o")
OPENAI_GENERATION_MODEL = os.environ.get("OPENAI_GENERATION_MODEL", "o3")
```
- Configures OpenAI models for different pipeline stages
- Separates embedding, validation, and generation models
- Provides sensible defaults (GPT-4o for validation, text-embedding-3-large for embeddings)
- Allows configuration via environment variables

## Pinecone Configuration

```python
# --- Pinecone Configuration ---
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "chassidus-index")
```
- Configures Pinecone vector database settings
- Sets default index name for Pinecone
- Allows customization via environment variables

## RAG Pipeline Parameters

```python
# --- Default RAG Pipeline Parameters ---
DEFAULT_N_RETRIEVE = 30  # Reduced from 300 for better performance/cost balance
DEFAULT_N_VALIDATE = 15  # Reduced from 100 for better performance/cost balance
```
- Controls retrieval and validation batch sizes
- Balances performance, cost, and quality
- Documents optimization rationale in comments

## Prompt Configuration

```python
# Import prompts from the prompts module
try:
    from prompts import OPENAI_SYSTEM_PROMPT, VALIDATION_PROMPT_TEMPLATE
except ImportError:
    print("Warning: Failed to import prompts module. Using default prompts.")
    # Fallback prompts would be defined here if needed
```
- Imports prompt templates from a dedicated module
- Provides graceful error handling if import fails
- Separates prompt content from configuration logic

## Helper Functions

### Environment Variable Validation
```python
def check_env_vars():
    missing_keys = []
    if not LANGSMITH_API_KEY: missing_keys.append("LANGSMITH_API_KEY")
    if not OPENAI_API_KEY: missing_keys.append("OPENAI_API_KEY")
    if not PINECONE_API_KEY: missing_keys.append("PINECONE_API_KEY")
    return missing_keys
```
- Validates the presence of required API keys
- Returns a list of missing keys for diagnosis
- Called during module initialization to provide early warnings

### LangSmith Configuration
```python
def configure_langsmith():
    os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
    if LANGSMITH_API_KEY: os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    if LANGSMITH_PROJECT: os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    print(f"LangSmith configured: Endpoint={LANGSMITH_ENDPOINT}, Tracing={LANGSMITH_TRACING}, Project={LANGSMITH_PROJECT or 'Default'}")
```
- Sets up LangSmith environment variables for tracing
- Provides diagnostic output about the configuration
- Conditionally sets variables only if values are available

## Initialization Checks
The module performs automatic validation on import:
```python
missing = check_env_vars()
if missing:
    print(f"Warning: Missing essential API keys: {', '.join(missing)}")
else:
    print("All essential API keys found.")

configure_langsmith()
```
- Validates environment on module import
- Provides immediate feedback about missing configuration
- Sets up LangSmith tracing automatically
- Avoids silent configuration errors

## Security Considerations
- API keys are loaded from environment variables, not hardcoded
- Sensitive configuration is validated but not exposed in logs
- Environment-specific configuration supported via .env files
- No default values provided for sensitive API keys 