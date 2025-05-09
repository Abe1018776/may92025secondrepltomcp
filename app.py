import streamlit as st
import logging
import traceback
import time
import os
import shutil
from pathlib import Path

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    # Import i18n module for internationalization
    from i18n import (
        get_text, get_direction, get_language_name, 
        DEFAULT_LANGUAGE, LANGUAGES
    )

    # Import components
    from components.sidebar import display_sidebar
    from components.chat import display_chat_message, process_prompt

    # Import CSS utilities
    from css import init_styles

    # Import config and necessary services
    import config
    from services.retriever import init_retriever
    from services.openai_service import init_openai_client

    logger.info("App: Imports successful.")
except ImportError as e:
    st.error(f"Fatal Error: Module import failed. {e}", icon="🚨")
    logger.error(f"Import error: {e}", exc_info=True)
    traceback.print_exc()
    st.stop()
except Exception as e:
    st.error(f"Fatal Error during initial setup: {e}", icon="🚨")
    logger.error(f"Initialization error: {e}", exc_info=True)
    traceback.print_exc()
    st.stop()

def setup_static_resources():
    """
    Copy the Noto Rashi Hebrew fonts to a location accessible by Streamlit.

    Streamlit requires static files to be in specific directories for proper URL paths.
    """
    try:
        # Ensure the static directory exists for Streamlit
        static_dir = Path("static")
        static_dir.mkdir(exist_ok=True)

        # Create a subdirectory for the Noto Rashi fonts
        font_static_dir = static_dir / "Noto_Rashi_Hebrew"
        font_static_dir.mkdir(exist_ok=True)
        static_fonts_dir = font_static_dir / "static"
        static_fonts_dir.mkdir(exist_ok=True)

        # Define the source and destination paths
        src_dir = Path("Noto_Rashi_Hebrew")

        # Copy the variable font
        var_font_src = src_dir / "NotoRashiHebrew-VariableFont_wght.ttf"
        var_font_dest = font_static_dir / "NotoRashiHebrew-VariableFont_wght.ttf"

        if var_font_src.exists() and not var_font_dest.exists():
            shutil.copy2(var_font_src, var_font_dest)
            logger.info(f"Copied variable font to {var_font_dest}")

        # Copy the static fonts
        static_src_dir = src_dir / "static"

        if static_src_dir.exists():
            for font_file in static_src_dir.glob("*.ttf"):
                dest_file = static_fonts_dir / font_file.name
                if not dest_file.exists():
                    shutil.copy2(font_file, dest_file)
                    logger.info(f"Copied static font {font_file.name} to {dest_file}")

        logger.info("Static resources setup complete")
    except Exception as e:
        logger.error(f"Error setting up static resources: {e}", exc_info=True)
        # Don't stop the app, just log the error

def main():
    """Main application function."""
    # --- Initialize Required Services ---
    logger.info("App: Initializing services...")
    try:
        retriever_ready_init, retriever_msg_init = init_retriever()
        openai_ready_init, openai_msg_init = init_openai_client()
        logger.info("App: Service initialization calls complete.")
    except Exception as init_err:
        st.error(f"Error during service initialization: {init_err}", icon="🔥")
        logger.error(f"Service initialization error: {init_err}", exc_info=True)
        traceback.print_exc()
        st.stop()

    # Ensure the Noto Rashi Hebrew font is accessible to Streamlit
    setup_static_resources()

    # --- Streamlit Page Configuration and Styling ---
    st.set_page_config(
        page_title="Divrey Yoel AI Chat (GPT-4o Gen)", 
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    # Initialize session state variables if not already set
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    elif st.session_state.language not in LANGUAGES:  # Validate language
        st.session_state.language = DEFAULT_LANGUAGE

    if "hebrew_font" not in st.session_state:
        st.session_state.hebrew_font = "David Libre"  # Default font

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "prompt_input" not in st.session_state:
        st.session_state.prompt_input = ""

    if "active_template" not in st.session_state:
        st.session_state.active_template = None
    elif st.session_state.active_template is not None:
        # Check if template language matches current language
        template_lang = st.session_state.active_template.get("language_code")
        if template_lang and template_lang != st.session_state.language:
            st.session_state.active_template = None

    # Get current text direction and generate CSS
    text_direction = get_direction()

    # Initialize styles
    init_styles()

    # Center-aligned title and subtitle using translated text with David Libre font
    st.markdown(f"<h1 dir='{text_direction}' lang='{st.session_state.language}' class='app-title'>{get_text('app_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p dir='{text_direction}' lang='{st.session_state.language}' class='app-title'>{get_text('app_subtitle')}</p>", unsafe_allow_html=True)

    # Display sidebar and get RAG parameters
    rag_params = display_sidebar()

    # Render chat history
    for msg in st.session_state.messages:
        display_chat_message(msg)

    # Get prompt gallery result from sidebar
    prompt_gallery_result = rag_params.get("prompt_gallery_result")

    # Initialize prompt variable to avoid potential uninitialized usage
    prompt = None

    # If we have a stored prompt to use
    if st.session_state.prompt_input:
        prompt = st.session_state.prompt_input
        st.session_state.prompt_input = ""

    # Process prompt from chat input (takes precedence over stored prompt)
    chat_input_prompt = st.chat_input(get_text('chat_placeholder'), disabled=not rag_params["services_ready"])

    # If user enters new text, check if there's an active template
    if chat_input_prompt:
        # If user is entering text while a template is active, combine them
        if st.session_state.active_template:
            template = st.session_state.active_template
            # Combine the template text with user input
            full_prompt = template["template"] + chat_input_prompt
            # Store the original user query for search
            if template.get("isolate_query", False):
                rag_params["original_query"] = chat_input_prompt
            else:
                rag_params["original_query"] = None
            prompt = full_prompt
            # Clear the active template after use
            st.session_state.active_template = None
        else:
            prompt = chat_input_prompt
            rag_params["original_query"] = None

        # Process the prompt
        process_prompt(prompt, rag_params)
    # If we have a selected template or a stored prompt from prompt gallery
    elif prompt_gallery_result:
        selected_prompt, template_data = prompt_gallery_result
        if template_data:
            # Set the active template for next input
            st.session_state.active_template = template_data
            # Display an info message that the template is active
            st.info(get_text('template_active_message'), icon="ℹ️")
        else:
            # For regular example questions, process immediately
            process_prompt(selected_prompt, rag_params)

if __name__ == "__main__":
    main()