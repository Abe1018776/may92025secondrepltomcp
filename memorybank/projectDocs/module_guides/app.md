# App Module Guide

## Overview
The `app.py` file is the main entry point for the Streamlit application that serves as the Divrei Yoel AI Chat interface. It coordinates all components, manages the user interface, and orchestrates the chat flow.

## Main Components

1. **Initialization and Error Handling**
   - Sets up logging
   - Gracefully handles import and initialization errors
   - Initializes services (retriever, OpenAI)
   - Sets up static resources for fonts

2. **Session State Management**
   - Initializes language settings
   - Manages Hebrew font preferences
   - Tracks chat history
   - Handles template selection

3. **UI Component Coordination**
   - Displays sidebar with settings and prompt gallery
   - Renders chat history
   - Displays chat input
   - Processes user prompts

## Execution Flow

The main function execution flow is as follows:

1. Initialize required services and handle any errors
2. Set up static resources for fonts
3. Configure Streamlit page settings
4. Initialize session state variables if not already set
5. Set up page title and subtitle
6. Display sidebar with settings and prompt gallery
7. Render chat message history
8. Process user inputs and prompt selection
9. Handle chat input and prompt processing

## Key Functions

### `main()`
- Entry point for the Streamlit application
- Orchestrates the entire application flow
- Handles service initialization and UI rendering

### `setup_static_resources()`
- Copies font files to locations accessible by Streamlit
- Creates necessary directories
- Handles font file management

## UI Organization

The UI is organized as follows:

1. **Page Header**
   - Application title
   - Subtitle with application description

2. **Sidebar**
   - Language and font settings
   - Service status indicators
   - RAG parameters
   - Sample questions and prompt gallery (moved from main UI for cleaner layout)

3. **Main Content Area**
   - Chat history display
   - Chat input field

## Component Integration

The application integrates several components:

1. `display_sidebar()` - Shows settings and prompt gallery in the sidebar
2. `display_chat_message()` - Renders individual chat messages
3. `process_prompt()` - Processes user inputs and generates responses

## Error Handling

The application includes comprehensive error handling:

1. Import errors are caught and displayed prominently
2. Service initialization failures are handled gracefully
3. Runtime errors during chat processing are captured and displayed to the user

## Prompt Processing

The application handles prompts from multiple sources:

1. Direct user input via the chat input field
2. Example questions selected from the sidebar's prompt gallery
3. Template-based inputs where the template is selected from the gallery

## Templates

Templates provide structured prompts with placeholders for user input:

1. Templates are selected from the sidebar's gallery
2. When a template is active, the user's next input is combined with the template
3. Template metadata can specify how to handle the user's input (e.g., as a standalone query)

## Internationalization

The application supports multiple languages:

1. Text elements use the `get_text()` function from the i18n module
2. Text direction is set based on the selected language
3. Font selection is offered for languages like Hebrew

## Session State Variables

Key session state variables include:

- `language`: Current language selection
- `hebrew_font`: Selected Hebrew font
- `messages`: Chat history
- `prompt_input`: Temporarily stored prompt
- `active_template`: Currently selected template (if any)

## Architecture

### Key Components
```
┌─────────────────────────────────┐
│ app.py                          │
├─────────────────────────────────┤
│ ┌─────────┐  ┌───────────────┐  │
│ │ Logging │  │ Error Handling│  │
│ └─────────┘  └───────────────┘  │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Service Initialization      │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Streamlit Page Configuration│ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Component Rendering         │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

### Flow Diagram
```
Startup → Logging Setup → Import Components → Initialize Services → 
Configure Page → Render UI Components → Process User Input → Execute RAG Pipeline
```

## Service Initialization
The application initializes two core services:
1. **Retriever Service**: Handles document retrieval from Pinecone
2. **OpenAI Service**: Manages communication with the OpenAI API

```python
retriever_ready_init, retriever_msg_init = init_retriever()
openai_ready_init, openai_msg_init = init_openai_client()
```

## CSS and Styling
The application applies dynamic CSS styling with special considerations for RTL Hebrew text:
1. Gets the current text direction based on language
2. Generates CSS with appropriate RTL/LTR settings
3. Forces browser to refresh CSS using timestamped keys
4. Adds specific styling for Hebrew fonts

## Input Processing
User input can come from two sources:
1. Prompt gallery selection
2. Direct chat input

Both are processed through the `process_prompt()` function, which handles:
- Adding the message to the history
- Calling the RAG pipeline
- Updating the UI with streaming responses
- Displaying source documents

## Recent Enhancements
- Implemented centralized logging system
- Refactored UI components into separate modules
- Enhanced error handling for service initialization
- Improved session state management
- Fixed input variable handling
- Added proper variable initialization

## Usage
To start the application, run:
```bash
streamlit run app.py
``` 