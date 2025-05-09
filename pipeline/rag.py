import asyncio
import logging
import traceback
from typing import Dict, Any, List, Callable, Optional

import streamlit as st

# Setup logger
logger = logging.getLogger(__name__)

async def process_rag_request(
    history: List[Dict[str, Any]], 
    params: Dict[str, Any], 
    status_callback: Optional[Callable[[str], None]] = None,
    stream_callback: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    """
    Process a RAG request asynchronously.

    Args:
        history (List[Dict[str, Any]]): Message history
        params (Dict[str, Any]): RAG parameters
        status_callback (Optional[Callable]): Callback for status updates
        stream_callback (Optional[Callable]): Callback for streaming response chunks

    Returns:
        Dict[str, Any]: Response data including final response, documents, and logs
    """
    from i18n import get_text
    from rag_processor import execute_validate_generate_pipeline

    try:
        return await execute_validate_generate_pipeline(
            history=history,
            params=params,
            status_callback=status_callback,
            stream_callback=stream_callback
        )
    except asyncio.CancelledError:
        logger.warning("RAG request was cancelled")
        return {
            "final_response": get_text('request_cancelled'),
            "error": "Request cancelled",
            "status_log": ["Request cancelled by user or system"],
            "generator_input_documents": [],
            "pipeline_used": "Cancelled"
        }
    except asyncio.TimeoutError:
        logger.error("RAG request timed out")
        return {
            "final_response": get_text('request_timeout'),
            "error": "Request timed out",
            "status_log": ["Request exceeded maximum allowed time"],
            "generator_input_documents": [],
            "pipeline_used": "Timeout"
        }
    except Exception as e:
        logger.exception("Error in RAG processing")
        return {
            "final_response": f"{get_text('processing_error')}: {type(e).__name__}",
            "error": str(e),
            "status_log": [f"Error: {type(e).__name__}", traceback.format_exc()],
            "generator_input_documents": [],
            "pipeline_used": "Error"
        }

def create_async_execution_context():
    """
    Create or get the appropriate asyncio execution context.

    Returns:
        asyncio.AbstractEventLoop: The event loop to use
    """
    try:
        # Try to get the current running loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop

def extract_citations(response: str) -> List[str]:
    """
    Extract citation IDs from a response text.

    Args:
        response (str): Response text with potential citations

    Returns:
        List[str]: List of citation IDs
    """
    # Early return if empty response
    if not response or not response.strip():
        return []

    try:
        from services.openai_service import extract_citations_with_openai
        loop = create_async_execution_context()
        return loop.run_until_complete(extract_citations_with_openai(response))
    except Exception as e:
        logger.exception("Failed to extract citations")
        st.error(f"Citation extraction failed: {e}", icon="⚠️")
        return []
# Format the message with proper RTL styling
    if err:
        formatted_msg = f"""
        <div dir='{text_direction}' class='error-message {text_direction}-text' style='font-family: "David Libre", serif;'>
"""