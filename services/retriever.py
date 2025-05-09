# services/retriever.py
# Keep this file exactly as it was in the previous correct version.
# It correctly uses config and utils.
import time
import traceback
import os
import asyncio
from typing import List, Dict, Optional, Tuple
from pinecone import Pinecone, Index
from langsmith import traceable

# Change relative imports to absolute imports
import config
from config import (
    PINECONE_API_KEY,
    OPENAI_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_MODEL
)
from utils import clean_source_text, get_embedding, clean_api_key

# --- Globals ---
pinecone_client: Optional[Pinecone] = None
pinecone_index: Optional[Index] = None
is_retriever_ready: bool = False
retriever_status_message: str = "Retriever not initialized."

# --- Initialization ---
def init_retriever() -> Tuple[bool, str]:
    """Initializes the Pinecone client and index connection."""
    global pinecone_client, pinecone_index, is_retriever_ready, retriever_status_message
    if is_retriever_ready: return True, retriever_status_message
    if not PINECONE_API_KEY:
        retriever_status_message = "Error: PINECONE_API_KEY not found in Secrets."
        is_retriever_ready = False; return False, retriever_status_message
    if not OPENAI_API_KEY:
        retriever_status_message = "Error: OPENAI_API_KEY not found (needed for query embeddings)."
        is_retriever_ready = False; return False, retriever_status_message
    try:
        print("Retriever: Initializing Pinecone client...")
        # Clean the API key before using it
        cleaned_pinecone_key = clean_api_key(PINECONE_API_KEY)
        pinecone_client = Pinecone(api_key=cleaned_pinecone_key)
        index_name = PINECONE_INDEX_NAME
        print(f"Retriever: Checking for Pinecone index '{index_name}'...")
        available_indexes = [idx.name for idx in pinecone_client.list_indexes().indexes]
        if index_name not in available_indexes:
            retriever_status_message = f"Error: Pinecone index '{index_name}' does not exist."
            is_retriever_ready = False; pinecone_client = None; return False, retriever_status_message
        print(f"Retriever: Connecting to Pinecone index '{index_name}'...")
        pinecone_index = pinecone_client.Index(index_name)
        stats = pinecone_index.describe_index_stats()
        print(f"Retriever: Pinecone index stats: {stats}")
        if stats.total_vector_count == 0:
            retriever_status_message = f"Retriever connected, but index '{index_name}' is empty."
        else:
            retriever_status_message = f"Retriever ready (Index: {index_name}, Embed Model: {EMBEDDING_MODEL})."
        is_retriever_ready = True
        return True, retriever_status_message
    except Exception as e:
        error_msg = f"Error initializing Pinecone: {type(e).__name__} - {e}"; print(error_msg); traceback.print_exc()
        retriever_status_message = error_msg; is_retriever_ready = False; pinecone_client = None; pinecone_index = None
        return False, retriever_status_message

def get_retriever_status() -> Tuple[bool, str]:
    if not is_retriever_ready: init_retriever()
    return is_retriever_ready, retriever_status_message

# --- Core Function ---
@traceable(name="pinecone-retrieve-documents")
async def retrieve_documents(query_text: str, n_results: int) -> List[Dict]:
    global pinecone_index
    ready, message = get_retriever_status()
    if not ready or pinecone_index is None:
        print(f"Retriever not ready: {message}"); return []
    print(f"Retriever: Retrieving top {n_results} docs for query: '{query_text[:100]}...'"); start_time = time.time()
    try:
        query_embedding = await get_embedding(query_text, model=EMBEDDING_MODEL)
        if query_embedding is None: print("Retriever: Failed query embedding."); return []
        # Run Pinecone query in a thread to avoid blocking
        response = await asyncio.to_thread(
            pinecone_index.query,
            vector=query_embedding,
            top_k=n_results,
            include_metadata=True
        )
        formatted_results = []
        if not response or not response.matches: print("Retriever: No results found."); return []
        for match in response.matches:
            metadata = match.metadata if match.metadata else {}
            doc_data = {
                "vector_id": match.id, "original_id": metadata.get('original_id', match.id),
                "source_name": metadata.get('source_name', 'Unknown Source'),
                "hebrew_text": metadata.get('hebrew_text', ''), "english_text": metadata.get('english_text', ''),
                "similarity_score": match.score, 'metadata_raw': metadata
            }
            formatted_results.append(doc_data)
        total_time = time.time() - start_time; print(f"Retriever: Retrieved {len(formatted_results)} docs in {total_time:.2f}s.")
        return formatted_results
    except Exception as e:
        print(f"Retriever: Error during query/processing: {type(e).__name__}"); traceback.print_exc(); return []