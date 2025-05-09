from .sanitization import sanitize_html
import re
import os
import asyncio
from typing import List, Dict, Optional
from openai import AsyncOpenAI

# Change relative imports to absolute imports
import config
from config import OPENAI_API_KEY, EMBEDDING_MODEL

def clean_source_text(text: str) -> str:
    """
    Clean and format source text for display.
    
    Args:
        text (str): The source text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    text = text.replace('\x00', '').replace('\ufffd', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_api_key(api_key: str) -> str:
    """
    Clean API key by removing 'Bearer ' prefix if present
    
    Args:
        api_key (str): The API key to clean
        
    Returns:
        str: Cleaned API key
    """
    if not api_key:
        return ""
    # Remove 'Bearer ' prefix if present
    if api_key.startswith("Bearer "):
        return api_key.replace("Bearer ", "").strip()
    return api_key.strip()

async def get_embedding(text: str, model: str = None, max_retries: int = 3) -> Optional[List[float]]:
    """
    Get embedding for text using OpenAI's API asynchronously
    
    Args:
        text (str): Text to get embedding for
        model (str): Model to use for embedding
        max_retries (int): Maximum number of retries
        
    Returns:
        List[float]: Embedding vector or None if failed
    """
    if model is None:
        model = EMBEDDING_MODEL
    
    # Clean the API key before using it
    cleaned_api_key = clean_api_key(OPENAI_API_KEY)
    
    openai_client = AsyncOpenAI(api_key=cleaned_api_key)
    
    if not text or not isinstance(text, str):
        print("Error: Invalid input text for embedding.")
        return None
        
    cleaned_text = text.replace("\n", " ").strip()
    if not cleaned_text:
        print("Warning: Text is empty after cleaning, cannot get embedding.")
        return None
        
    attempt = 0
    while attempt < max_retries:
        try:
            response = await openai_client.embeddings.create(input=[cleaned_text], model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding (Attempt {attempt + 1}/{max_retries}): {type(e).__name__} - {str(e)}")
            wait_time = (2 ** attempt)
            print(f"Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)
            attempt += 1
            
    print(f"Failed embedding after {max_retries} attempts.")
    return None

def format_context_for_openai(documents: List[Dict]) -> str:
    """
    Formats documents for the OpenAI prompt context section using numbered list.
    
    Args:
        documents (List[Dict]): List of document dictionaries
        
    Returns:
        str: Formatted context for OpenAI
    """
    if not documents:
        return "No source texts provided."
    formatted_docs = []
    language_key = 'hebrew_text'
    id_key = 'original_id'
    source_key = 'source_name' # Optional: Include source name if available

    for index, doc in enumerate(documents):
        if not isinstance(doc, dict):
            print(f"Warning: Skipping non-dict item in documents list: {doc}")
            continue

        text = clean_source_text(doc.get(language_key, ''))
        doc_id = doc.get(id_key, f'unknown_{index+1}')
        source_name = doc.get(source_key, '') # Get source name

        if text:
            # Start with 1-based indexing for readability
            header = f"Source {index + 1} (ID: {doc_id}"
            if source_name:
                header += f", SourceName: {source_name}"
            header += ")"
            formatted_docs.append(f"{header}:\n{text}\n---") # Add separator

    if not formatted_docs:
         return "No valid source texts could be formatted."

    return "\n".join(formatted_docs) 