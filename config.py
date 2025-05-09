import os
import sys
from dotenv import load_dotenv

dot_env_path = os.path.join(os.path.dirname(__file__), '.env')

# If on a platoform like Hugging Face, the .env file is not needed and we should use load_dotenv with no arguments
if os.path.exists(dot_env_path):
    load_dotenv(dotenv_path=dot_env_path, verbose=True, override=True, stream=sys.stdout)
else:
    load_dotenv()

# Import prompts from the prompts module
try:
    from prompts import OPENAI_SYSTEM_PROMPT, VALIDATION_PROMPT_TEMPLATE
except ImportError:
    print("Warning: Failed to import prompts module. Using default prompts.")
    # Fallback prompts would be defined here if needed

# --- LangSmith Configuration ---
LANGSMITH_ENDPOINT = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING", "true")
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "DivreyYoel-RAG-GPT4-Gen")

# --- API Keys (Required) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# --- Model Configuration ---
EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_VALIDATION_MODEL = os.environ.get("OPENAI_VALIDATION_MODEL", "gpt-4o")
OPENAI_GENERATION_MODEL = os.environ.get("OPENAI_GENERATION_MODEL", "o3")

# --- Pinecone Configuration ---
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "chassidus-index")

# --- Default RAG Pipeline Parameters ---
DEFAULT_N_RETRIEVE = 30  # Reduced from 300 for better performance/cost balance
DEFAULT_N_VALIDATE = 15  # Reduced from 100 for better performance/cost balance

# --- Helper Functions ---
def check_env_vars():
    missing_keys = []
    if not LANGSMITH_API_KEY: missing_keys.append("LANGSMITH_API_KEY")
    if not OPENAI_API_KEY: missing_keys.append("OPENAI_API_KEY")
    if not PINECONE_API_KEY: missing_keys.append("PINECONE_API_KEY")
    return missing_keys

def configure_langsmith():
    os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
    if LANGSMITH_API_KEY: os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    if LANGSMITH_PROJECT: os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    print(f"LangSmith configured: Endpoint={LANGSMITH_ENDPOINT}, Tracing={LANGSMITH_TRACING}, Project={LANGSMITH_PROJECT or 'Default'}")

missing = check_env_vars()
if missing:
    print(f"Warning: Missing essential API keys: {', '.join(missing)}")
else:
    print("All essential API keys found.")

configure_langsmith()
