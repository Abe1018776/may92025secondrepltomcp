import streamlit as st
from typing import Dict, Any, List
import asyncio
import logging
import traceback
import nest_asyncio

# Apply nest_asyncio once during module import
nest_asyncio.apply()

# Setup logger
logger = logging.getLogger(__name__)

# Import our refactored modules
from ui.hebrew import handle_mixed_language_text
from ui.chat_render import display_chat_message, display_status_updates, format_source_html
from pipeline.rag import process_rag_request, create_async_execution_context, extract_citations

def process_prompt(prompt: str, rag_params: Dict[str, Any]):
    """
    Process a user prompt and generate a response.
    
    Args:
        prompt (str): User input prompt (may contain template)
        rag_params (Dict[str, Any]): RAG parameters from sidebar
    """
    # Import here to avoid circular imports
    from i18n import get_direction, get_text
    from utils.sanitization import sanitize_html
    from rag_processor import PIPELINE_VALIDATE_GENERATE_GPT4O
    
    # Initialize session state if needed
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    text_direction = get_direction()
    hebrew_font = st.session_state.hebrew_font
    
    # Add the visible prompt to chat history (what the user sees)
    st.session_state.messages.append({"role": "user", "content": prompt})
    display_chat_message(st.session_state.messages[-1])

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        status_container = st.status(get_text('processing'), expanded=True)
        chunks: List[str] = []
        try:
            def status_cb(m): status_container.update(label=f"{get_text('processing_step')} {m}")
            def stream_cb(c):
                # Sanitize the chunk before appending
                if isinstance(c, str):
                    c = sanitize_html(c)
                chunks.append(c)
                # Process the entire response with mixed language handler first
                joined_text = ''.join(chunks) + "▌"  # Add cursor
                display_html = handle_mixed_language_text(joined_text, hebrew_font)
                # Sanitize the final HTML to prevent injection
                safe_html = sanitize_html(display_html)
                msg_placeholder.markdown(safe_html, unsafe_allow_html=True)

            try:
                # Get the current event loop or create a new one
                loop = create_async_execution_context()
                
                final_rag = loop.run_until_complete(
                    process_rag_request(
                        history=st.session_state.messages,
                        params=rag_params,
                        status_callback=status_cb,
                        stream_callback=stream_cb
                    )
                )
                
                # Extract citations after getting the response
                cited_ids = []
                if isinstance(final_rag, dict):
                    raw = final_rag.get("final_response", "")
                    # Only attempt to extract citations if we have a valid response
                    if raw and raw.strip():
                        cited_ids = extract_citations(raw)
            except (RuntimeError, asyncio.CancelledError, asyncio.TimeoutError) as loop_err:
                st.error(f"{get_text('error_async')} {loop_err}", icon="⚠️")
                # Format error message with RTL support
                err_html = f"""
                <div dir='{text_direction}' class='{text_direction}-text hebrew-font'>
                    <strong>{get_text('request_error')}</strong><br>
                    {get_text('error_async')}<br>
                    {type(loop_err).__name__}
                </div>
                """
                # Sanitize error HTML
                err_html = sanitize_html(err_html)
                msg_placeholder.markdown(err_html, unsafe_allow_html=True)
                # Create minimal final_rag result for error case
                final_rag = {
                    "final_response": get_text('error_async'),
                    "error": str(loop_err),
                    "status_log": [f"Asyncio error: {type(loop_err).__name__}"],
                    "generator_input_documents": [],
                    "pipeline_used": "Error"
                }
                cited_ids = []

            if isinstance(final_rag, dict):
                # Sanitize raw content
                raw = final_rag.get("final_response", "")
                if isinstance(raw, str):
                    raw = sanitize_html(raw)
                    
                err = final_rag.get("error")
                log = final_rag.get("status_log", [])
                docs = final_rag.get("generator_input_documents", [])
                pipeline = final_rag.get("pipeline_used", PIPELINE_VALIDATE_GENERATE_GPT4O)

                # Process final content with mixed language handler
                if not (err and raw.strip().startswith("<div")):
                    final = handle_mixed_language_text(raw, hebrew_font)
                    # Final sanitization after processing
                    final = sanitize_html(final)
                else:
                    final = sanitize_html(raw)
                
                msg_placeholder.markdown(final, unsafe_allow_html=True)

                # Use the citations extracted earlier instead of making another async call
                if cited_ids:
                    enumerated_docs = list(enumerate(docs, start=1))
                    docs_to_show = [(idx, doc) for idx, doc in enumerated_docs if str(idx) in cited_ids]
                else:
                    docs_to_show = list(enumerate(docs, start=1))

                if docs_to_show:
                    # Use a simple text title for the expander
                    with st.expander(f"{get_text('sources_title')} ({len(docs_to_show)})", expanded=False):
                        # Add RTL Hebrew wrapper with embed
                        expander_title = f"""
                        <div class='expander-title rtl-text hebrew-font' dir='rtl' lang="he">
                            {get_text('sources_text').format(len(docs_to_show))}
                        </div>
                        """
                        st.markdown(expander_title, unsafe_allow_html=True)
                        
                        # Container for all sources with RTL direction
                        st.markdown(f"""
                        <div dir='rtl' lang="he" class='expander-content rtl-text hebrew-font'>
                        """, unsafe_allow_html=True)
                        
                        # Format each source consistently using our helper function
                        for idx, doc in docs_to_show:
                            source_html, text_html = format_source_html(doc, idx, hebrew_font, get_text)
                            st.markdown(source_html, unsafe_allow_html=True)
                            st.markdown(text_html, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)

                # store message
                assistant_data = {
                    "role": "assistant",
                    "content": final,
                    "final_docs": docs,
                    "pipeline_used": pipeline,
                    "status_log": log,
                    "error": err
                }
                st.session_state.messages.append(assistant_data)
                display_status_updates(log)
                if err:
                    status_container.update(label=f"{get_text('error')}!", state="error", expanded=False)
                else:
                    status_container.update(label=get_text('processing_complete'), state="complete", expanded=False)
            else:
                # Format communication error message with proper RTL support
                err_msg = f"""
                <div dir='{text_direction}' class='{text_direction}-text hebrew-font'>
                    <strong>{get_text('communication_error')}</strong>
                </div>
                """
                msg_placeholder.markdown(sanitize_html(err_msg), unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": get_text('communication_error'),
                    "final_docs": [],
                    "pipeline_used": "Error",
                    "status_log": ["Unexpected result"],
                    "error": "Unexpected"
                })
                status_container.update(label=f"{get_text('error')}!", state="error", expanded=False)

        except Exception as e:
            logger.exception("Unhandled exception in RAG processing")
            traceback.print_exc()
            # Format critical error with RTL support
            err_html = f"""
            <div dir='{text_direction}' class='{text_direction}-text hebrew-font'>
                <strong>{get_text('critical_error')}</strong><br>
                {get_text('reload')}
                <details>
                    <summary>{get_text('details')}</summary>
                    <pre>{sanitize_html(traceback.format_exc())}</pre>
                </details>
            </div>
            """
            # Sanitize error HTML
            err_html = sanitize_html(err_html)
            msg_placeholder.error(err_html, icon="🔥")
            st.session_state.messages.append({
                "role": "assistant",
                "content": err_html,
                "final_docs": [],
                "pipeline_used": "Critical Error",
                "status_log": [f"Critical: {type(e).__name__}"],
                "error": str(e)
            })
            status_container.update(label=get_text('processing_error'), state="error", expanded=False) 