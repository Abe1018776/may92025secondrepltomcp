import streamlit as st
from typing import Dict, Any, List
import logging
import re
from utils.sanitization import escape_html, sanitize_html

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

    # Force RTL and David Libre font styling for sources
    source_html = f"""
    <div class='source-info rtl-text hebrew-font' dir='rtl' lang="he" style="font-family: 'David Libre', serif !important;">
        <strong>{get_text('source_label').format(i)}</strong> {source}
    </div>
    """

    text_html = f"""
    <div class='hebrew-text rtl-text hebrew-font' dir='rtl' lang="he" style="font-family: 'David Libre', serif !important;">
        {text}
    </div>
    """

    return source_html, text_html

def display_chat_message(message: Dict[str, Any]) -> None:
    """
    Display a chat message in the Streamlit UI.

    Args:
        message (Dict[str, Any]): The message to display
    """
    # Add inline style to ensure David Libre is used with explicit size
    st.markdown("""
    <style>
    .stChatMessage div[data-testid="stChatMessageContent"] {
        font-family: "David Libre", "David", serif !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.chat_message(message["role"]):
        # Get the message content
        content = message.get('content', '')
        role = message.get('role', '')
        
        # Import necessary functions
        from i18n import get_direction, get_text
        text_direction = get_direction()
        hebrew_font = st.session_state.get('hebrew_font', 'David Libre')
        
        if isinstance(content, str):
            # Check if the content is already HTML formatted to prevent double rendering
            if content.strip().startswith('<div') and 'rtl-text' in content:
                # Content is already formatted HTML, display directly
                st.markdown(content, unsafe_allow_html=True)
            else:
                # For plain text, apply the normal formatting process
                # Escape any HTML tags in the original content
                content = escape_html(content)
                content = sanitize_html(content)

                # Process with the mixed language handler - always force David Libre font
                from ui.hebrew import handle_mixed_language_text
                
                # Standardize inline citations format for consistency
                # Look for citation patterns like "מקור X" and ensure they're not already in HTML tags
                citation_pattern = re.compile(r'(?<!<[^>]*)(מקור \d+)')
                content = citation_pattern.sub(r'\1', content)  # Remove any special formatting
                
                content = handle_mixed_language_text(content, "David Libre")
                # Final sanitization after processing
                content = sanitize_html(content)

                # Display full content for all messages
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
                style="font-family: 'David Libre', serif !important;"
            >{get_text('processing_log')}</div>""", unsafe_allow_html=True)

            for u in status_log:
                st.markdown(
                    f"""<code 
                        class='status-update {text_direction}-text hebrew-font' 
                        dir="{text_direction}"
                        style="font-family: 'David Libre', serif !important;"
                    >- {u}</code>""",
                    unsafe_allow_html=True
                )