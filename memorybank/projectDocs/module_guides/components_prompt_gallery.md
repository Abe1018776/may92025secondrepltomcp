# Prompt Gallery Component

> **DEPRECATED**: This component has been integrated into the `sidebar.py` component to create a cleaner UI layout. The code remains in this document for reference.

This module provides a gallery of predefined prompts and templates that users can select from to interact with the application.

## Overview

The Prompt Gallery displays:
1. Example questions that users can use directly
2. Template prompts that require additional user input

## Functions

### `display_prompt_gallery()`

**DEPRECATED**: This function has been integrated into the `display_sidebar()` function in `sidebar.py`.

This function renders a gallery of example questions and template prompts with an easy insertion mechanism.

**Returns:**
- `Tuple[str, Optional[Dict[str, Any]]] or None`: A tuple with (selected_prompt, template_data) if a prompt or template is selected, otherwise None

## Usage in Application

Previously, this component was displayed in the main content area, but now it's integrated into the sidebar for a cleaner UI layout.

## Key Features

- Displays example questions in expandable containers
- Shows template prompts with detailed instructions
- Supports RTL languages like Hebrew with proper text direction
- Uses language-sensitive truncation for previews
- Returns selected prompts to the main application for processing

## Session State Variables

The component uses the following session state variables:
- `clicked_example_question`: Stores the selected example question
- `clicked_template`: Stores the selected template data
- `active_template`: Set in the main app when a template is selected

## Original Implementation

```python
import streamlit as st
from typing import Dict, Any, Optional, Tuple
import logging

# Setup logger
logger = logging.getLogger(__name__)

def display_prompt_gallery():
    """
    Display a gallery of starter prompts with easy insertion.
    
    Returns:
        Tuple[str, Optional[Dict[str, Any]]] or None: A tuple with (selected_prompt, template_data) if a prompt or template is selected, otherwise None
    """
    # Import here to avoid circular imports
    from i18n import get_direction, get_text, get_current_user_prompt_starters, get_prompt_templates, get_current_language
    from utils.sanitization import escape_html
    
    text_direction = get_direction()
    current_language = get_current_language()
    
    # Determine text alignment based on text direction
    text_align = "right" if text_direction == "rtl" else "left"
    
    # Log current language to help debug template selection issues
    logger.info(f"Current language in prompt gallery: {current_language}")
    
    # Display examples section with proper RTL styling
    section_style = f"""
        direction: {text_direction};
        text-align: {text_align};
        font-family: "{st.session_state.hebrew_font}", "Open Sans Hebrew", "Alef Hebrew", "Arial Hebrew", sans-serif;
    """
    
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
        # For Hebrew text, we may need to adjust the preview length differently
        # because Hebrew characters may display differently
        max_length = 40  # Shorter preview for button labels
        
        if len(text) > max_length:
            # Extract the beginning of the text for the preview
            preview = text[:max_length].strip()
            
            # Try to find a good breakpoint (end of a word) 
            # to avoid cutting words in the middle
            last_space = preview.rfind(' ')
            if last_space > max_length // 2:  # Only use space if it's reasonably far in
                preview = preview[:last_space]
                
            preview += "..."
            return escape_html(preview)
        
        return escape_html(text)
    
    # Create two columns for the question expanders
    col1, col2 = st.columns(2)
    
    # Split questions evenly between columns
    half = len(starters) // 2 + (len(starters) % 2)
    
    # First column
    with col1:
        for i in range(half):
            if i < len(starters):
                question = starters[i]
                # Create expandable container for each question with a descriptive preview
                with st.expander(create_button_label(question), expanded=False):
                    # Show the full question with proper RTL styling
                    st.markdown(f"""<div dir="{text_direction}" 
                        style="{section_style}" 
                        class="question-full-text">
                        {escape_html(question)}
                    </div>""", unsafe_allow_html=True)
                    # Add button to use this question
                    if st.button(
                        get_text('use_this_question'),
                        key=f"use_q_{i}",
                        use_container_width=True
                    ):
                        st.session_state.clicked_example_question = question
                        st.session_state.clicked_template = None
    
    # Second column
    with col2:
        for i in range(half, len(starters)):
            question = starters[i]
            # Create expandable container for each question with a descriptive preview
            with st.expander(create_button_label(question), expanded=False):
                # Show the full question with proper RTL styling
                st.markdown(f"""<div dir="{text_direction}" 
                    style="{section_style}" 
                    class="question-full-text">
                    {escape_html(question)}
                </div>""", unsafe_allow_html=True)
                # Add button to use this question
                if st.button(
                    get_text('use_this_question'),
                    key=f"use_q_{i}",
                    use_container_width=True
                ):
                    st.session_state.clicked_example_question = question
                    st.session_state.clicked_template = None
    
    # Display templates section
    templates = get_prompt_templates()
    
    # Log templates retrieval to debug language issues
    logger.info(f"Retrieved {len(templates)} templates for language: {current_language}")
    for i, template in enumerate(templates):
        logger.info(f"Template {i+1}: {template.get('name', 'Unnamed')} (language code in data structure: {template.get('language_code', 'not specified')})")
    
    if templates:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""<h3 dir="{text_direction}" style="{section_style}">
            {get_text('prompt_templates')}
        </h3>""", unsafe_allow_html=True)
        
        # Create a single column for templates (they're larger)
        for i, template in enumerate(templates):
            template_name = template.get('name', f"Template {i+1}")
            template_desc = template.get('description', '')
            template_text = template.get('template', '')
            
            # Display a button with the template name
            button_label = f"{template_name}"
            if template_desc:
                button_label = f"{template_name} - {template_desc}"
            
            # Create expandable container for each template
            with st.expander(create_button_label(button_label), expanded=False):
                # Check if template contains HTML
                is_html_template = template_text.strip().startswith("<") and ">" in template_text
                
                # For templates with HTML, don't escape the HTML tags
                if is_html_template:
                    # Replace newlines with <br> tags but don't escape HTML
                    processed_template = template_text.replace('\n', '<br>')
                else:
                    # For regular text templates, escape HTML then convert newlines
                    safe_template = escape_html(template_text)
                    processed_template = safe_template.replace('\n', '<br>')
                
                # Show the full template with proper RTL styling
                st.markdown(f"""<div dir="{text_direction}" 
                    style="{section_style}" 
                    class="template-full-text">
                    {processed_template}
                </div>""", unsafe_allow_html=True)
                # Add button to use this template
                if st.button(
                    get_text('use_this_template'),
                    key=f"use_template_{i}",
                    use_container_width=True
                ):
                    # Set the template in session state
                    st.session_state.clicked_template = template
                    st.session_state.clicked_example_question = None
                    st.rerun()  # Rerun to update the UI with the selected template
    
    # Return selected prompt if any
    selected_prompt = st.session_state.clicked_example_question
    selected_template = st.session_state.clicked_template
    
    if selected_prompt:
        # Reset after use
        st.session_state.clicked_example_question = None
        return selected_prompt, None
    elif selected_template:
        # For templates, we return a tuple of (template_preview, template_data)
        # where template_preview is a shortened version for display in chat input
        template_text = selected_template.get('template', '')
        template_preview = template_text.split("\n\n")[0] + "..."
        return template_preview, selected_template
    
    return None
```

## Styling and Appearance
The gallery implements special styling for the prompt buttons:
- Consistent button styling across the row
- Proper RTL text alignment for Hebrew prompts
- Visual distinction from the main chat interface
- Hover effects for better user interaction

## Example Questions
The gallery pulls example questions from the i18n module, which provides:
- Language-appropriate examples
- Culturally relevant queries
- Questions optimized for the document corpus
- Topics covering main subject areas of Divrei Yoel

## Internationalization
The gallery fully supports internationalization:
- Example prompts change based on selected language
- Button texts adapt to RTL/LTR as needed
- Tooltips are properly translated
- Section heading uses translated text

## User Experience Benefits
The prompt gallery enhances user experience by:
- Providing inspiration for queries
- Demonstrating the types of questions the system can answer
- Reducing friction for new users
- Showcasing the system's Hebrew capabilities
- Allowing quick access to common questions

## Recent Enhancements
- Improved grid-based layout
- Enhanced button styling for RTL Hebrew text
- Added tooltips for better user guidance
- Optimized responsive design for various screen sizes
- Ensured proper alignment with RTL layout
- Improved example quality and relevance 