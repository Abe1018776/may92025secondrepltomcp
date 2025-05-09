---
title: April28ragdivreyyoel
emoji: 🌍
colorFrom: purple
colorTo: purple
sdk: streamlit
sdk_version: 1.45.0
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Divrey Yoel AI Chat Application

A Streamlit-based chat application for interacting with the teachings of Rabbi Yoel Teitelbaum of Satmar using Retrieval Augmented Generation (RAG) technology.

## Features

- Bilingual support (Hebrew/English)
- Customizable fonts for Hebrew text
- Retrieval-augmented generation for accurate responses
- Source citation and display
- Text validation with GPT-4o

## Project Structure

The application has been modularized into the following components:

```
april28ragdivreyyoel/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── i18n.py                # Internationalization helpers
├── rag_processor.py       # RAG pipeline processing
├── utils.py               # Utility functions
├── components/            # UI components
│   ├── __init__.py
│   ├── chat.py            # Chat message display and processing
│   ├── prompt_gallery.py  # Example questions gallery
│   └── sidebar.py         # Settings sidebar
├── css/                   # CSS styling
│   ├── __init__.py
│   └── styles.py          # CSS generation functions
├── services/              # External services
│   ├── __init__.py
│   ├── openai_service.py  # OpenAI API integration
│   └── retriever.py       # Document retrieval service
└── utils/                 # Utility modules
    ├── __init__.py
    └── sanitization.py    # HTML sanitization utilities
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Installation Steps

1. Clone the repository (or download the ZIP file):
   ```
   git clone https://github.com/yourusername/april28ragdivreyyoel.git
   cd april28ragdivreyyoel
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Environment Configuration

1. Create a `.env` file by copying the example file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file and fill in the required API keys:
   ```
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   
   # Optional LangSmith Configuration (for tracing and debugging)
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=DivreyYoel-RAG-GPT4-Gen
   LANGSMITH_TRACING=true
   
   # Model Configuration (optional, default values shown)
   OPENAI_EMBEDDING_MODEL=text-embedding-3-large
   OPENAI_VALIDATION_MODEL=gpt-4o
   OPENAI_GENERATION_MODEL=o3
   
   # Pinecone Configuration (optional, default values shown)
   PINECONE_INDEX_NAME=chassidus-index
   ```

3. Save the file with your changes.

## Running the Application

1. Ensure your virtual environment is activated.

2. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

3. The application will start and open in your default web browser (typically at http://localhost:8501).

## Troubleshooting

- If you encounter errors related to missing API keys, check your `.env` file and ensure all required keys are present.
- For service initialization errors, verify your internet connection and API key validity.
- If the application fails to start, check the console output for specific error messages.

## Customization

- Adjust model settings in `config.py`
- Add new languages in `i18n.py`
- Modify UI components in the `components/` directory

## Technology Stack

- Streamlit for UI
- OpenAI GPT-4o for text generation and validation
- Pinecone for vector search
- Support for RTL languages and special Hebrew fonts

## License

[Add license information here]