# Prompts Module Guide

## Overview
The `prompts/templates.py` module centralizes prompt templates for the RAG pipeline in the Divrei Yoel AI Chat application. It defines structured prompts for the validation and generation phases, ensuring consistent interactions with the language model.

## Key Template Categories

### Validation Prompts
```python
VALIDATE_DOCUMENT_SYSTEM_PROMPT = """
You are an expert system for determining whether a document is relevant to a query.
Your task is to analyze the provided Hebrew text and determine if it contains information that would help answer the user's query.
You should focus on semantic relevance, not just keyword matching.
"""
```
- System prompt for the GPT-4o validation step
- Establishes the role and purpose of the model
- Emphasizes semantic relevance over keyword matching
- Optimized for Hebrew text analysis

### Validation User Prompt Template
```python
VALIDATE_DOCUMENT_USER_PROMPT_TEMPLATE = """
Query: {query}
Hebrew Document: {document}

Is this document relevant to answering the query? Analyze the content and determine relevance.
Output your assessment as a JSON object with the following structure:
{{"is_relevant": true or false, "relevance_score": number from 0 to 10, "explanation": "brief explanation of your reasoning"}}
"""
```
- Template for constructing the user prompt in validation
- Includes placeholders for query and document
- Requests structured JSON output for programmatic processing
- Requires both binary relevance and a numeric score

### Generation System Prompt
```python
GENERATION_SYSTEM_PROMPT = """
You are a knowledgeable assistant specializing in the teachings of the Satmar Rebbe, Rabbi Yoel Teitelbaum.
Your responses should be accurate, respectful, and based solely on the provided context documents.
Use a scholarly yet accessible tone, and respond in the same language as the user's query (Hebrew or English).
"""
```
- System prompt for the GPT-4o generation step
- Defines the assistant's identity and expertise
- Sets expectations for tone and style
- Specifies language mirroring behavior
- Emphasizes reliance on provided context

### Generation User Prompt Template
```python
GENERATION_USER_PROMPT_TEMPLATE = """
Context Documents:
{context_documents}

Conversation History:
{conversation_history}

Based on the context documents provided, please answer the query respectfully and accurately.
If the context doesn't contain sufficient information to answer the query, acknowledge this limitation.
When quoting or referencing specific passages, include citation numbers like [1], [2], etc.
"""
```
- Template for constructing the user prompt in generation
- Includes placeholders for context documents and conversation history
- Provides clear instructions on citation format
- Guides the model to acknowledge knowledge limitations

## Dynamic System Prompts
The module supports dynamic system prompts that can be customized at runtime:
```python
def get_dynamic_system_prompt(custom_prompt=None):
    """
    Returns either the custom prompt if provided, or the default system prompt.
    
    Args:
        custom_prompt: Optional custom system prompt
        
    Returns:
        The system prompt to use for generation
    """
    if custom_prompt:
        return custom_prompt
    return GENERATION_SYSTEM_PROMPT
```
- Allows runtime customization of system instructions
- Maintains fallback to default templates
- Enables specialized behavior for different use cases

## Helper Functions

### Context Formatting
```python
def format_context_documents(documents):
    """
    Formats a list of context documents for inclusion in a prompt.
    
    Args:
        documents: List of document dictionaries
        
    Returns:
        Formatted string of numbered documents
    """
    formatted_docs = []
    for i, doc in enumerate(documents):
        formatted_docs.append(f"[{i+1}] {doc['hebrew_text']}")
    return "\n\n".join(formatted_docs)
```
- Prepares documents for inclusion in prompts
- Adds citation numbers for reference
- Ensures consistent formatting

### Conversation History Formatting
```python
def format_conversation_history(history):
    """
    Formats conversation history for inclusion in a prompt.
    
    Args:
        history: List of message dictionaries
        
    Returns:
        Formatted string of conversation turns
    """
    formatted_history = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted_history.append(f"{role}: {msg['content']}")
    return "\n\n".join(formatted_history)
```
- Converts the internal message history format for prompts
- Clearly labels user and assistant messages
- Preserves conversation flow

## Internationalization
The prompts module integrates with the i18n system:
```python
def get_system_prompt(lang=None):
    """Get the appropriate system prompt based on language."""
    return i18n.get_system_prompt(lang)
```
- Retrieves language-specific system prompts
- Allows seamless switching between languages
- Maintains prompt structure across languages

## Recent Enhancements
- Added support for dynamic system prompts
- Enhanced Hebrew-specific instructions
- Improved citation formatting guidance
- Added better context document formatting
- Optimized prompts for GPT-4o compatibility
- Added language-aware response guidance 