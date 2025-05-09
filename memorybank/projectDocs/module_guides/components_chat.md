# Chat Component Module Guide

## Overview
The `components/chat.py` module handles the display and processing of chat messages in the Divrei Yoel AI Chat application. It's responsible for rendering user and assistant messages, processing user prompts, and orchestrating the RAG pipeline execution.

## Key Functions

### `display_chat_message(message: Dict[str, Any])`
- **Purpose**: Renders an individual chat message in the Streamlit UI
- **Parameters**:
  - `message`: Dictionary containing role ("user" or "assistant"), content, and optional metadata
- **Functionality**:
  - Determines message display based on role (user/assistant)
  - Formats messages with appropriate RTL/LTR styling
  - Applies proper font styling based on the current language direction
  - Sanitizes HTML content for secure rendering
  - Renders source documents in an expandable section for assistant messages

### `display_status_updates(status_log: List[str])`
- **Purpose**: Shows processing status updates in an expandable section
- **Parameters**:
  - `status_log`: List of status update messages
- **Functionality**:
  - Creates an expandable section with appropriate styling
  - Formats each status update with proper RTL/LTR handling
  - Applies the current Hebrew font to ensure consistent styling

### `process_prompt(prompt: str, rag_params: Dict[str, Any])`
- **Purpose**: Main function to handle user input and generate responses
- **Parameters**:
  - `prompt`: User's input text
  - `rag_params`: Dictionary of RAG pipeline parameters
- **Process Flow**:
  1. Add user message to chat history and display it
  2. Create placeholder for assistant response
  3. Initialize status container for real-time updates
  4. Set up callbacks for status updates and streaming response
  5. Execute RAG pipeline asynchronously with appropriate parameters
  6. Handle citation extraction from the generated response
  7. Process and display the results, including:
     - Response text with proper styling
     - Source documents in an expandable section
     - Status updates in a separate expandable section
     - Error messages (if any)
  8. Store the assistant message in session state

## Response Streaming
The module implements a streaming mechanism to display the assistant's response in real-time:
```python
def stream_cb(c):
    chunks.append(c)
    sanitized_response = sanitize_html(''.join(chunks))
    msg_placeholder.markdown(
        f"<div dir='{text_direction}' class='{text_direction}-text' style='font-family: \"{hebrew_font}\", \"Open Sans Hebrew\", \"Alef Hebrew\", \"Arial Hebrew\", sans-serif !important;'>{sanitized_response}▌</div>",
        unsafe_allow_html=True
    )
```

## Source Document Display
The module includes an expandable section to show the source documents used in generating the response:
```python
with st.expander(f"{get_text('sources_title')} ({len(docs_to_show)})", expanded=False):
    expander_title = f"<div class='expander-title {text_direction}-text' style='font-family: \"{hebrew_font}\", \"Open Sans Hebrew\", \"Alef Hebrew\", \"Arial Hebrew\", sans-serif !important;'>{get_text('sources_text').format(len(docs_to_show))}</div>"
    st.markdown(sanitize_html(expander_title), unsafe_allow_html=True)
    
    for idx, doc in docs_to_show:
        source = doc.get('source_name', '') or get_text('unknown_source')
        source = sanitize_html(source)
        
        text = doc.get('hebrew_text', '')
        text = clean_source_text(text)
        text = sanitize_html(text)
        
        st.markdown(source_html, unsafe_allow_html=True)
        st.markdown(text_html, unsafe_allow_html=True)
```

## Error Handling
The module implements comprehensive error handling:
- Try/except blocks for asynchronous operations
- Detailed logging of errors
- User-friendly error messages displayed with Streamlit
- Fallback mechanisms when services fail
- Special handling for asyncio runtime errors

## Security Considerations
The module includes several security measures:
- HTML sanitization for all dynamic content using `sanitize_html`
- Proper text cleaning for source documents using `clean_source_text`
- Safe HTML rendering with appropriate sanitization
- Controlled error messages that don't expose sensitive information

## Integration with RAG Pipeline
The module integrates with the RAG pipeline by:
1. Setting up proper callback functions for status updates and streaming
2. Running the pipeline asynchronously using `asyncio`
3. Using `nest_asyncio` to allow nested event loops
4. Processing and displaying pipeline results with proper formatting

## Internationalization Support
The module uses the i18n system extensively:
- All user-facing text comes from the i18n system via `get_text()`
- Text direction is handled dynamically based on language via `get_direction()`
- Font selection adapts based on the current language setting

## Recent Features
- Enhanced HTML sanitization for security
- Dynamic text direction support for RTL languages
- Improved error handling for async operations
- Citation extraction to show only referenced sources
- Streaming response display with real-time updating
- Status container with state handling (complete/error)
- Font customization for Hebrew text rendering 