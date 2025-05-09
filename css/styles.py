import streamlit as st
import os

@st.cache_data(show_spinner=False)
def load_css_file(file_path):
    """
    Load a CSS file and return its contents

    Args:
        file_path (str): Path to the CSS file

    Returns:
        str: Contents of the CSS file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Failed to load CSS file: {e}")
        return ""

def apply_rtl_css():
    """
    Apply RTL CSS to the Streamlit app
    """
    # Get the path to the RTL CSS file
    css_dir = os.path.dirname(os.path.abspath(__file__))
    rtl_css_path = os.path.join(css_dir, 'assets', 'rtl.css')

    # Load the CSS file
    css = load_css_file(rtl_css_path)

    # Set the Hebrew font variable
    hebrew_font = st.session_state.get('hebrew_font', 'Noto Rashi Hebrew')
    css = css.replace('var(--hebrew-font)', hebrew_font)

    # Apply the CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def init_styles():
    """
    Initialize all styles for the app
    """
    # Set default font if not already set
    if 'hebrew_font' not in st.session_state:
        st.session_state.hebrew_font = "Noto Rashi Hebrew"

    # Apply RTL CSS
    apply_rtl_css()

    # Apply custom CSS for expandable sections
    st.markdown("""
    <style>
    /* Styles for expandable sections */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 0.9rem;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #f7f7f7;
        border-left: 4px solid #4e8cff;
        transition: background-color 0.3s, box-shadow 0.3s;
    }

    .streamlit-expanderHeader:hover {
        background-color: #eef5ff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Customize expander icon */
    .streamlit-expanderHeader svg {
        color: #4e8cff;
        transition: transform 0.2s;
    }

    .streamlit-expanderHeader[aria-expanded="true"] svg {
        transform: rotate(90deg);
    }

    /* Style expander content */
    .streamlit-expanderContent {
        padding: 10px 12px;
        border-radius: 0 0 6px 6px;
        border-left: 4px solid #e8f0fe;
        background-color: #fafafa;
        transition: all 0.3s ease;
    }

    /* Style the question and template content */
    .question-full-text, .template-full-text, .prompt-full-text {
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 4px;
        background-color: rgba(245, 245, 245, 0.6);
        white-space: pre-wrap;
        line-height: 1.6;
        overflow-wrap: break-word;
        word-wrap: break-word;
        hyphens: auto;
        max-width: 100%;
        border-left: 4px solid #e1e1e1;
    }

    /* RTL specific styling for question and template content */
    [dir="rtl"] .question-full-text, [dir="rtl"] .template-full-text, [dir="rtl"] .prompt-full-text {
        text-align: right;
        border-left: none;
        border-right: 4px solid #e1e1e1;
    }

    /* Different border colors for questions vs templates */
    .question-full-text {
        border-color: #4e8cff;
        background-color: #f5f8ff;
    }

    .template-full-text {
        border-color: #5cb85c;
        background-color: #f5fff8;
        line-height: 1.5;
    }

    /* Styling for HTML templates and code examples */
    .template-full-text div {
        max-width: 100%;
        overflow-wrap: break-word;
        word-wrap: break-word;
    }

    /* Fix for HTML tags in templates */
    .template-full-text code, .template-full-text pre {
        display: block;
        padding: 10px;
        margin-top: 8px;
        margin-bottom: 8px;
        overflow: auto;
        font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 0.9em;
        color: #333;
        background-color: #f5f5f5;
        border-radius: 3px;
        border: 1px solid #eaeaea;
    }

    /* Ensure HTML content in templates is displayed properly */
    .rtl-text, .hebrew-font {
        display: block;
        width: 100%;
    }

    /* Use button styling */
    .stButton button {
        margin-top: 10px;
        background-color: #4e8cff;
        color: white;
        font-weight: 500;
        border-radius: 4px;
        border: none;
        padding: 8px 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .stButton button:hover {
        background-color: #3a7ce8;
    }

    /* App title custom styling */
    .app-title {
        font-family: "David Libre", "David", serif !important;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_app_css(text_direction, hebrew_font):
    """
    Generate all CSS styles for the application.

    Args:
        text_direction (str): 'rtl' or 'ltr'
        hebrew_font (str): The selected Hebrew font

    Returns:
        str: Complete CSS styles as string
    """
    rtl = text_direction == "rtl"
    text_align = "right" if rtl else "left"
    font_stack = f"'{hebrew_font}', 'Alef Hebrew', 'Arial Hebrew', sans-serif"

    return f"""
/* ===== Core Styles ===== */
/* Imports */
@import url('https://fonts.googleapis.com/earlyaccess/alefhebrew.css');
@import url('https://fonts.googleapis.com/earlyaccess/notosanshebrew.css');

/* Base Layout */
html, body {{ 
    overflow-x: hidden !important; 
    margin: 0 !important;
    padding: 0 !important;
}}

body, .stApp {{ 
    font-family: {font_stack if rtl else "'Arial', sans-serif"};
    direction: {text_direction};
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    text-align: {text_align};
    direction: {text_direction};
    font-family: {font_stack if rtl else "'Arial', sans-serif"} !important;
}}

/* RTL Support */
[dir="rtl"], [lang="he"], [lang="iw"] {{
    direction: rtl !important;
    text-align: right !important;
    font-family: {font_stack} !important;
    unicode-bidi: embed;
}}

/* Source Text - Special handling for Hebrew Sources */
.hebrew-text, .source-info {{
    direction: rtl !important;
    text-align: right !important;
    font-family: {font_stack} !important;
    unicode-bidi: embed;
}}

/* UI Components */
.stButton > button {{
    font-family: {font_stack if rtl else "'Arial', sans-serif"};
    text-align: center !important;
}}

/* Chat Components */
.stChatMessage .stChatMessageContent {{ 
    font-family: inherit;
    direction: inherit;
    text-align: inherit;
}}

.stChatInputContainer textarea {{
    font-family: {font_stack};
}}

/* Prompt Gallery */
.prompt-card {{
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 10px;
    font-family: {font_stack} !important;
    direction: {text_direction};
    text-align: {text_align};
}}
.prompt-card:hover {{ 
    background-color: #f0f0f0; 
}}

/* Expandable Sections */
.streamlit-expanderHeader {{
    font-family: {font_stack if rtl else "'Arial', sans-serif"};
    direction: {text_direction};
}}

.question-full-text, .template-full-text, .prompt-full-text {{
    font-family: {font_stack} !important;
    direction: {text_direction};
    text-align: {text_align};
    line-height: 1.6;
    overflow-wrap: break-word;
    word-wrap: break-word;
    hyphens: auto;
    max-width: 100%;
}}

/* Fix for RTL-text and mixed-content classes */
.rtl-text, .mixed-content {{
    display: block; 
    direction: rtl !important;
    text-align: right !important;
    font-family: {font_stack} !important;
    unicode-bidi: embed;
}}

/* Special Fonts */
.rashi-text {{
    font-family: "Noto Rashi Hebrew", {font_stack} !important;
}}

/* Dynamic Content */
.dynamic-content {{ 
    font-family: {font_stack if rtl else "'Arial', sans-serif"};
    direction: {text_direction};
}}
"""

# Alias for backward compatibility
generate_dynamic_css = generate_app_css
```