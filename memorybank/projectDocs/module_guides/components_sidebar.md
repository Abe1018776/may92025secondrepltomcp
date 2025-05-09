# Sidebar Component Module Guide

## Overview
The `components/sidebar.py` module manages the sidebar UI elements in the Divrei Yoel AI Chat application. It provides configuration options, language and font settings, service status indicators, and RAG parameter controls. The sidebar also includes the prompt gallery for sample questions and templates.

## Key Function

### `display_sidebar()`
- **Purpose**: Renders the application sidebar with all settings
- **Returns**: Dictionary with RAG parameters, services status, and prompt gallery selection
- **Parameter Structure**:
  ```python
  {
      "n_retrieve": int,               # Number of documents to retrieve
      "n_validate": int,               # Number of documents to validate
      "services_ready": bool,          # Whether all required services are ready
      "prompt_gallery_result": tuple   # Selected prompt from gallery (if any)
  }
  ```
- **Process Flow**:
  1. Render language and font selection
  2. Show service status indicators
  3. Configure RAG parameters
  4. Display sample questions and prompt templates
  5. Return configuration and selections

## Sidebar Sections

### Settings Toggle
```python
with st.sidebar:
    settings_expander = st.expander(get_text('settings_title'), expanded=False)
```
- Collapsible section for settings to conserve UI space
- Clear visual indicator of expandability

### Language Selection
```python
with settings_expander:
    language_options = {code: name for code, name in LANGUAGES.items()}
    selected_language = st.selectbox(
        get_text('language_setting'),
        options=list(language_options.keys()),
        format_func=lambda x: language_options.get(x, x)
    )
```
- Dropdown with language options (Hebrew/English)
- Updates session state when changed
- Triggers a page refresh to apply changes

### Font Selection
```python
font_options = get_font_options()
selected_font = st.selectbox(
    get_text('font_setting'),
    options=list(font_options.keys()),
    format_func=lambda x: font_options.get(x, x)
)
```
- Font selection options optimized for Hebrew text
- Preview of each font style
- Updates session state and refreshes CSS when changed

### Service Status
```python
retriever_ready, _ = get_retriever_status()
openai_ready, _ = get_openai_status()
services_ready = retriever_ready and openai_ready
```
- Real-time status for Retriever and OpenAI services
- Visual indicators (✅/❌) of service health
- Combined readiness status for RAG pipeline

### RAG Parameters
```python
n_retrieve = st.slider(get_text('retrieval_count'), 1, 300, config.DEFAULT_N_RETRIEVE)
n_validate = st.slider(get_text('validation_count'), 1, max_validate, min(config.DEFAULT_N_VALIDATE, max_validate))
```
- Adjustable sliders for retrieval and validation parameters
- Tooltips with explanations of each parameter
- Default values from configuration

### Prompt Gallery
```python
# Display example questions as clickable items
for i, question in enumerate(starters):
    if st.button(
        create_button_label(question),
        key=f"question_{i}",
        use_container_width=True,
        help=question if len(question) > 40 else None  # Show tooltip for long questions
    ):
        st.session_state.clicked_example_question = question
```
- Displays example questions as one-click buttons
- Shows templates as directly clickable items
- Includes helpful tooltips for long questions and templates
- Supports proper RTL rendering for Hebrew text
- Stores selected prompts in session state for use in the main app

## State Management
The sidebar manages several session state variables:
- `st.session_state.language`: Currently selected language
- `st.session_state.hebrew_font`: Font choice for Hebrew text
- `st.session_state.css_reload_trigger`: Timestamp for forcing CSS refresh
- `st.session_state.clicked_example_question`: Selected example question from the gallery
- `st.session_state.clicked_template`: Selected template from the gallery
- `st.session_state.active_template`: Active template to be used with user input

## Internationalization
The sidebar uses the i18n module for all displayed text:
- Labels adapt based on the selected language
- Help text and tooltips are properly translated
- Selection options maintain proper ordering

## UI Styling
The sidebar implements special styling:
- Consistent with overall application theme
- Proper RTL support for Hebrew text
- Visual indicators for service status
- Font preview capabilities

## Recent Enhancements
- Added collapsible settings section
- Implemented font preview functionality
- Enhanced service status indicators
- Improved overall sidebar organization
- Relocated prompt gallery from main UI to sidebar for cleaner interface
- Streamlined question and template selection with one-click activation
- Added tooltips for better preview of long questions and templates

## Integration with Main App
The main app `app.py` uses the sidebar's return value to:
1. Get RAG parameters for query processing
2. Check if services are ready for chat input
3. Process selected example questions and templates 