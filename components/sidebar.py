import streamlit as st
from typing import Dict, Any, Optional, Tuple
import logging

# Setup logger
logger = logging.getLogger(__name__)

def display_sidebar() -> Dict[str, Any]:
    """
    Display the sidebar with all settings and return the RAG parameters.
    
    Returns:
        Dict[str, Any]: A dictionary containing RAG parameters and prompt gallery selection
    """
    # Import here to avoid circular imports
    from i18n import get_direction, get_text, get_font_options, LANGUAGES, get_current_user_prompt_starters, get_prompt_templates, get_current_language
    from services.retriever import get_retriever_status
    from services.openai_service import get_openai_status
    from utils.sanitization import escape_html
    import config
    
    text_direction = get_direction()
    current_language = get_current_language()
    
    # Use Streamlit's native sidebar
    with st.sidebar:
        # All sidebar header items
        st.header(get_text('settings_title'))
        st.subheader(get_text('display_settings'))
        
        # Language selector
        language_options = {code: name for code, name in LANGUAGES.items()}
        current_language_index = list(language_options.keys()).index(st.session_state.language) if st.session_state.language in language_options else 0
        
        selected_language = st.selectbox(
            get_text('language_setting'),
            options=list(language_options.keys()),
            format_func=lambda x: language_options.get(x, x),
            index=current_language_index
        )
        
        # Update language if changed
        if selected_language != st.session_state.language:
            # Update session state and clear template
            st.session_state.language = selected_language
            if "active_template" in st.session_state:
                st.session_state.active_template = None
                
            # Notification and rerun
            st.success(f"Language changed to {language_options.get(selected_language, selected_language)}", icon="✅")
            st.rerun()
        
        # Font selector
        font_options = get_font_options()
        font_index = list(font_options.keys()).index(st.session_state.hebrew_font) if st.session_state.hebrew_font in font_options else 0
        
        selected_font = st.selectbox(
            get_text('font_setting'),
            options=list(font_options.keys()),
            format_func=lambda x: font_options.get(x, x),
            index=font_index
        )
        
        # Update font if changed
        if selected_font != st.session_state.hebrew_font:
            st.session_state.hebrew_font = selected_font
            st.success(f"Font changed to {font_options.get(selected_font, selected_font)}", icon="✅")
            st.rerun()
        
        # Font preview
        font_preview_text = get_text('font_preview').format(font_options.get(selected_font, selected_font))
        
        # Use streamlit container instead of custom HTML for preview
        preview = st.container(border=True)
        with preview:
            st.markdown(f"<div style='font-family: \"David Libre\", serif;direction:{text_direction};text-align:{'right' if text_direction=='rtl' else 'left'}'>{font_preview_text}</div>", unsafe_allow_html=True)
        
        st.divider()  # Native divider instead of HTML hr
        
        # Service status with native components
        retriever_ready, _ = get_retriever_status()
        openai_ready, _ = get_openai_status()
        
        status_col1, status_col2 = st.columns(2)
        with status_col1:
            st.write(f"**{get_text('retriever_status')}**")
        with status_col2:
            st.write("✅" if retriever_ready else "❌")
            
        if not retriever_ready:
            st.error(get_text('retriever_error'), icon="🛑")
            st.stop()
        
        status_col3, status_col4 = st.columns(2)
        with status_col3:
            st.write(f"**{get_text('openai_status')}**")
        with status_col4:
            st.write(f"{'✅' if openai_ready else '❌'}")
            
        if not openai_ready:
            st.warning(get_text('openai_error'), icon="⚠️")
        
        # RAG parameters
        n_retrieve = st.slider(get_text('retrieval_count'), 1, 300, config.DEFAULT_N_RETRIEVE)
        max_validate = min(n_retrieve, 100)
        n_validate = st.slider(
            get_text('validation_count'),
            1,
            max_validate,
            min(config.DEFAULT_N_VALIDATE, max_validate),
            disabled=not openai_ready
        )
        st.info(get_text('validation_info'), icon="ℹ️")
        
        # Prompt editors in expander
        with st.expander(get_text('edit_prompts'), expanded=False):
            config.OPENAI_SYSTEM_PROMPT = st.text_area(
                get_text('system_prompt'),
                value=config.OPENAI_SYSTEM_PROMPT,
                height=200
            )
            config.VALIDATION_PROMPT_TEMPLATE = st.text_area(
                get_text('validation_prompt'),
                value=config.VALIDATION_PROMPT_TEMPLATE,
                height=200
            )
            
        # ----- PROMPT GALLERY SECTION (MOVED FROM MAIN APP) -----
        st.divider()
        
        # Determine text alignment based on text direction
        text_align = "right" if text_direction == "rtl" else "left"
        
        # Style for section headers
        section_style = f"""
            direction: {text_direction};
            text-align: {text_align};
            font-family: "{st.session_state.hebrew_font}", "Open Sans Hebrew", "Alef Hebrew", "Arial Hebrew", sans-serif;
        """
        
        # Display examples section
        st.markdown(f"""<h3 dir="{text_direction}" style="{section_style}">
            {get_text('example_questions')}
        </h3>""", unsafe_allow_html=True)
        
        # Initialize session state for storing clicked question or template
        if "clicked_example_question" not in st.session_state:
            st.session_state.clicked_example_question = None
        
        if "clicked_template" not in st.session_state:
            st.session_state.clicked_template = None
        
        # Get example questions in the current language
        starters = get_current_user_prompt_starters()
        
        # Helper function to create language-aware button labels
        def create_button_label(text):
            max_length = 40  # Shorter preview for button labels
            
            if len(text) > max_length:
                # Extract the beginning of the text for the preview
                preview = text[:max_length].strip()
                
                # Try to find a good breakpoint (end of a word) 
                last_space = preview.rfind(' ')
                if last_space > max_length // 2:  # Only use space if it's reasonably far in
                    preview = preview[:last_space]
                    
                preview += "..."
                return escape_html(preview)
            
            return escape_html(text)
        
        # Display example questions as clickable items
        for i, question in enumerate(starters):
            # Create clickable button for each question
            if st.button(
                create_button_label(question),
                key=f"question_{i}",
                use_container_width=True,
                help=question if len(question) > 40 else None  # Show full text as tooltip for long questions
            ):
                st.session_state.clicked_example_question = question
                st.session_state.clicked_template = None
        
        # Display templates section
        templates = get_prompt_templates()
        
        if templates:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"""<h3 dir="{text_direction}" style="{section_style}">
                {get_text('prompt_templates')}
            </h3>""", unsafe_allow_html=True)
            
            # Display templates as clickable items
            for i, template in enumerate(templates):
                template_name = template.get('name', f"Template {i+1}")
                template_desc = template.get('description', '')
                template_text = template.get('template', '')
                
                # Create button label 
                button_label = f"{template_name}"
                if template_desc:
                    button_label = f"{template_name} - {template_desc}"
                
                # Tooltip contains a preview of the template
                tooltip = template_text[:100] + "..." if len(template_text) > 100 else template_text
                
                # Create clickable button for each template
                if st.button(
                    create_button_label(button_label),
                    key=f"template_{i}",
                    use_container_width=True,
                    help=tooltip
                ):
                    # Set the template in session state
                    st.session_state.clicked_template = template
                    st.session_state.clicked_example_question = None
                    st.rerun()  # Rerun to update the UI with the selected template

    # Process prompt gallery selections
    prompt_gallery_result = None
    selected_prompt = st.session_state.clicked_example_question
    selected_template = st.session_state.clicked_template
    
    if selected_prompt:
        # Reset after use
        st.session_state.clicked_example_question = None
        prompt_gallery_result = (selected_prompt, None)
    elif selected_template:
        # For templates, we return a tuple of (template_preview, template_data)
        template_text = selected_template.get('template', '')
        template_preview = template_text.split("\n\n")[0] + "..."
        prompt_gallery_result = (template_preview, selected_template)

    return {
        "n_retrieve": n_retrieve, 
        "n_validate": n_validate, 
        "services_ready": (retriever_ready and openai_ready),
        "prompt_gallery_result": prompt_gallery_result
    } 