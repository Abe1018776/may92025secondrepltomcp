import streamlit as st
from typing import Dict, Any, List
import logging

# Setup logger
logger = logging.getLogger(__name__)

def format_source_html(doc: Dict[str, Any], i: int, hebrew_font: str, get_text: callable) -> tuple:
    """
    Format a single source document as HTML with proper RTL styling.

    Args:
        doc (Dict): Source document
        i (int): Source index
        hebrew_font (str): Hebrew font to use
        get_text (callable): Function to get translated text

    Returns:
        tuple: (source_html, text_html) formatted HTML strings
    """
    from utils.sanitization import sanitize_html
    from utils import clean_source_text

    source = doc.get('source_name', '') or get_text('unknown_source')
    source = sanitize_html(source)

    # Clean and sanitize the Hebrew text
    text = doc.get('hebrew_text', '')
    if text is None:
        text = get_text('no_text_available')
    text = clean_source_text(text)
    text = sanitize_html(text)

    # Force RTL and proper Hebrew font styling for sources
    source_html = f"""
    <div class='source-info rtl-text hebrew-font' dir='rtl' lang="he">
        <strong>{get_text('source_label').format(i)}</strong> {source}
    </div>
    """

    text_html = f"""
    <div class='hebrew-text rtl-text hebrew-font' dir='rtl' lang="he">
        {text}
    </div>
    """

    return source_html, text_html

def display_chat_message(message: Dict[str, Any]):
    """
    Display a chat message with proper formatting.

    Args:
        message (Dict[str, Any]): Message object with role, content, and optional metadata
    """
    # Import here to avoid circular imports
    from i18n import get_direction, get_text
    from utils.sanitization import sanitize_html, escape_html
    from ui.hebrew import handle_mixed_language_text

    text_direction = get_direction()
    role = message.get("role", "assistant")

    # Always use David Libre font
    hebrew_font = "David Libre"

    with st.chat_message(role):
        # Sanitize the message content for HTML rendering
        content = message.get('content', '')
        if isinstance(content, str):
            # Escape any HTML tags in the original content
            content = escape_html(content)
            content = sanitize_html(content)

            # Process with the mixed language handler
            content = handle_mixed_language_text(content, hebrew_font)
            # Final sanitization after processing
            content = sanitize_html(content)

            # If this is a user message (prompt) and it's longer than a threshold, show it in an expandable section
            if role == "user" and len(content) > 150:
                # Create a preview of the content
                preview_content = content[:147] + "..."
                preview_content = handle_mixed_language_text(preview_content, hebrew_font)
                preview_content = sanitize_html(preview_content)

                # Show the preview
                st.markdown(preview_content, unsafe_allow_html=True)

                # Show the full content in an expander
                with st.expander(get_text('show_full_prompt'), expanded=False):
                    st.markdown(f"""<div dir="{text_direction}" 
                        class="prompt-full-text {text_direction}-text">
                        {content}
                    </div>""", unsafe_allow_html=True)
            else:
                # Display normal content
                st.markdown(content, unsafe_allow_html=True)

        if role == "assistant" and message.get("final_docs"):
            docs = message["final_docs"]
            # Use a simple text title for the expander
            with st.expander(f"{get_text('sources_title')} ({len(docs)})", expanded=False):
                # Add the rich HTML content inside the expander (static HTML is safe)
                expander_title = f"""
                <div class='expander-title rtl-text hebrew-font' dir="rtl" lang="he">
                    {get_text('sources_text').format(len(docs))}
                </div>
                """
                st.markdown(expander_title, unsafe_allow_html=True)
                st.markdown(f"""
                <div dir='rtl' lang="he" class='expander-content rtl-text hebrew-font'>
                """, unsafe_allow_html=True)

                for i, doc in enumerate(docs, start=1):
                    source_html, text_html = format_source_html(doc, i, hebrew_font, get_text)
                    st.markdown(source_html, unsafe_allow_html=True)
                    st.markdown(text_html, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)


def display_status_updates(status_log: List[str]):
    """
    Display processing status log in an expander.

    Args:
        status_log (List[str]): List of status update messages
    """
    # Import here to avoid circular imports
    from i18n import get_direction, get_text

    text_direction = get_direction()

    # Ensure we have a valid font setting
    if 'hebrew_font' not in st.session_state:
        st.session_state.hebrew_font = "Noto Rashi Hebrew"

    hebrew_font = st.session_state.hebrew_font

    # Text alignment based on direction
    text_align = "right" if text_direction == "rtl" else "left"

    if status_log:
        # Use a simple text title for the expander
        with st.expander(get_text('processing_details'), expanded=False):
            # Add the rich HTML content inside the expander
            st.markdown(f"""<div 
                class='expander-title {text_direction}-text hebrew-font' 
                dir="{text_direction}"
            >{get_text('processing_log')}</div>""", unsafe_allow_html=True)

            for u in status_log:
                st.markdown(
                    f"""<code 
                        class='status-update {text_direction}-text hebrew-font' 
                        dir="{text_direction}"
                    >- {u}</code>""",
                    unsafe_allow_html=True
                )