# Divrei Yoel AI Chat - Technical Documentation

## Project Overview
Divrei Yoel AI Chat is a RAG (Retrieval-Augmented Generation) application that provides Hebrew-language access to Chassidic texts, specifically works of the Satmar Rebbe, Rabbi Yoel Teitelbaum. The application implements a sophisticated three-stage RAG pipeline (Retrieve → Validate → Generate) with Pinecone for retrieval and OpenAI's GPT-4o for validation and generation.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                      Divrei Yoel AI Chat                        │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────┐ │
│ │   app.py    │ │ components/ │ │    css/      │ │   i18n.py  │ │
│ │  (Entrypoint)│ │ (UI Modules)│ │  (Styling)  │ │(Translation)│ │
│ └──────┬──────┘ └──────┬──────┘ └──────┬───────┘ └─────┬──────┘ │
│        │               │               │                │        │
│        └───────────────┴───────────────┴────────────────┘        │
│                               │                                  │
│                     ┌─────────┴───────────┐                      │
│                     │  rag_processor.py   │                      │
│                     │  (Pipeline Core)    │                      │
│                     └─────────┬───────────┘                      │
│                               │                                  │
│         ┌─────────────────────┼─────────────────────┐           │
│         │                     │                     │           │
│  ┌──────┴───────┐    ┌────────┴──────┐     ┌───────┴─────┐     │
│  │  services/   │    │   prompts/    │     │    utils/   │     │
│  │ (API Access) │    │ (Templates)   │     │ (Utilities) │     │
│  └──────────────┘    └───────────────┘     └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Core Modules

### Application Framework
* [**Application (app.py)**](module_guides/app.md) - Main entry point and Streamlit application setup
* [**RAG Processor**](module_guides/rag_processor.md) - Core implementation of the three-stage RAG pipeline
* [**Configuration**](module_guides/config.md) - Central configuration and environment variables

### User Interface Components
* [**Chat Component**](module_guides/components_chat.md) - Chat message display and processing
* [**Sidebar Component**](module_guides/components_sidebar.md) - Configuration sidebar with language and retrieval settings
* [**Prompt Gallery**](module_guides/components_prompt_gallery.md) - Grid-based prompt examples for quick selection

### Support Modules
* [**CSS Styling**](module_guides/css_styles.md) - Dynamic CSS generation with RTL/LTR support
* [**Internationalization (i18n)**](module_guides/i18n.md) - Language switching and translation support
* [**Utilities**](module_guides/utils.md) - Helper functions for logging, validation, and error handling
* [**API Services**](module_guides/services_api.md) - External API connections to OpenAI and Pinecone
* [**Prompts**](module_guides/prompts.md) - Templates for RAG pipeline prompts

## Code Quality

### Rules Compliance
* [**Rules Compliance Guide**](rules_compliance.md) - Guide to interpreting the rules compliance report
* [**Full Compliance Report**](../rules_compliance_report.md) - Detailed analysis of 19 Python files against coding standards

### Key Issues Identified
* **Critical**: Dynamic imports, global state management, runtime configuration modification
* **Medium**: Async/sync mixing, incomplete LangSmith tracing, unsanitized inputs, embedded HTML/CSS
* **Minor**: Print vs logging, long functions, improper configuration management

### Improvement Plan
A detailed improvement plan with 15 prioritized tasks has been created based on the rules compliance analysis. These tasks are tracked in the [**tasks.md**](../tasks.md) file in the Memory Bank.

## Technology Stack
- **Frontend**: Streamlit with custom CSS for Hebrew RTL support
- **LLM Provider**: OpenAI (GPT-4o) for text validation and generation
- **Vector Database**: Pinecone for document retrieval
- **Observability**: LangSmith for tracing and performance monitoring
- **Language Support**: Hebrew (primary) and English

## Key Features
1. **Three-Stage RAG Pipeline**:
   - Retrieval from Pinecone vector database
   - Validation of documents with GPT-4o
   - Generation of responses using validated documents

2. **Hebrew Language Optimization**:
   - RTL text display and input
   - Hebrew font selection
   - Culturally appropriate example questions
   - Citation formatting for Hebrew texts

3. **Advanced User Experience**:
   - Streaming responses for perceived responsiveness
   - Expandable source viewing for result transparency
   - Prompt gallery with one-click insertion
   - Status indicators throughout processing

4. **Technical Capabilities**:
   - Parallel processing of document validation
   - Comprehensive error handling with graceful degradation
   - Tracing and observability with LangSmith
   - Efficient context summarization for generation

## Recent Refactoring Enhancements
The codebase underwent significant refactoring to improve:

- **Modularity**: Reorganized into specialized packages with clear responsibilities
- **Internationalization**: Added comprehensive i18n framework
- **Error Handling**: Implemented centralized logging and robust error management
- **Dynamic Styling**: Created dedicated CSS management for RTL/LTR support
- **Security**: Added HTML sanitization for user-generated content
- **UI Components**: Separated UI elements into reusable components

## Development Setup
To set up the development environment:

1. **Clone the repository**:
   ```
   git clone [repository-url]
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your-api-key
   PINECONE_API_KEY=your-pinecone-key
   PINECONE_ENVIRONMENT=your-environment
   PINECONE_INDEX=your-index-name
   ```

4. **Run the application**:
   ```
   streamlit run app.py
   ```

## Future Enhancements
Planned improvements include:
- Complete internationalization for all Hebrew text
- UI rendering performance optimization
- Service initialization retry mechanisms
- Validation cost/speed optimization
- Enhanced code structure and maintainability

## Documentation
For detailed module documentation, see the individual module guides linked above.

## Development Guidelines
* [**Development Workflow Guide**](development_workflow.md) - Guidelines for development, testing, and deployment
* [**Rules Compliance Report**](rules_compliance.md) - Analysis of code quality issues and improvement opportunities 