# Product Context

## Product Overview
- **Name**: Divrei Yoel AI Chat (דברות קודש - חיפוש ועיון)
- **Type**: RAG-powered question answering system
- **Focus**: Chassidic texts, specifically works of the Satmar Rebbe (Rabbi Yoel Teitelbaum)
- **Language**: Hebrew interface and content
- **Last Updated**: 2025-05-06 16:35:20

## Core Product Purpose
The Divrei Yoel AI Chat provides an accessible, intelligent interface to access, explore, and understand the extensive teachings and writings of Rabbi Yoel Teitelbaum of Satmar. It serves as a modern research assistant for scholars, students, and those interested in Chassidic philosophy, making complex religious texts more accessible through natural language interaction. Unlike traditional text search, this system understands semantic meaning and relationships between concepts, retrieving information based on understanding rather than keyword matching.

## Corpus and Knowledge Base
- **Primary Sources**: Books, essays, commentaries, and responsa by Rabbi Yoel Teitelbaum
- **Secondary Sources**: Commentary and analysis of the Satmar Rebbe's works
- **Content Categories**:
  - Biblical commentary (Torah, Nevi'im, Ketuvim)
  - Talmudic interpretations and responsa
  - Halakhic (Jewish law) rulings and discussions
  - Chassidic philosophy and moral teachings
  - Historical perspectives and communal guidance
  - Festival and holiday-related teachings
  - Contemporary issues from a traditional Chassidic viewpoint

## User Experience Workflow
1. **Question Formulation**: User enters a question in Hebrew about a Chassidic concept, Torah interpretation, or specific teaching
2. **Initial Processing**: System analyzes the question for key concepts and semantic meaning
3. **Knowledge Retrieval**: Relevant passages are retrieved from the vector database using semantic search
   - Uses OpenAI's text-embedding-3-large model for embedding generation
   - Configurable retrieval count (up to 300 passages)
4. **Validation Pipeline**: Each retrieved passage undergoes AI validation for relevance
   - Uses GPT-4o to determine the actual relevance to the question
   - Runs validation in parallel for performance optimization
   - Filters out tangentially related or irrelevant content
5. **Response Generation**: System synthesizes a comprehensive answer based solely on validated passages
   - Maintains fidelity to original sources without hallucination
   - Structures information logically and cohesively
   - Includes proper citations to source materials
6. **Source Transparency**: User can expand citations to view original source text
   - Provides context and verification of the generated answer
   - Enables deeper study of specific sources

## Value Proposition
- **Access**: Makes rare Chassidic texts accessible through natural language questions
- **Understanding**: Provides contextual explanations of complex theological concepts
- **Efficiency**: Reduces research time for scholars and students
- **Accuracy**: Combines RAG technology with validation to ensure fidelity to sources
- **Education**: Serves as a learning tool for students of Chassidic philosophy
- **Preservation**: Helps preserve and disseminate traditional teachings in a modern format

## Target Audience
- Scholars and students of Chassidic teachings
- Individuals interested in the works of the Satmar Rebbe
- Hebrew-speaking audience seeking information on Chassidic concepts
- Religious educators and community leaders
- Researchers studying Jewish theology and Chassidic thought

## Key Differentiators
- **Validation Layer**: Three-stage RAG pipeline with explicit validation step
- **Hebrew Optimization**: Specialized handling of RTL text and Hebrew typography
- **Source Transparency**: Direct access to original source texts
- **Citation Intelligence**: AI-powered extraction of citations (replacing regex)
- **Chassidic Focus**: Specialized in a specific branch of Chassidic thought
- **Configurable Pipeline**: User-adjustable parameters for retrieval and validation

## User Interface Elements
- Hebrew RTL (Right-to-Left) text display with specialized fonts
- Question input field with real-time processing
- Grid-based prompt gallery with Hebrew example questions
- Threaded chat message display with user/assistant differentiation
- Expandable source text sections with citations
- Real-time processing status indicators
- Collapsible system configuration sidebar
- Language toggle for bilingual support (Hebrew/English)

## Configuration Options
- Number of passages to retrieve (slider)
- Number of passages to validate (slider)
- Customizable system prompts for generation and validation
- Font selection for Hebrew text display
- Language selection (Hebrew/English)
- Dark/light mode toggle

## Technical Architecture Highlights
- **Retrieval**: Vector similarity search using Pinecone
- **Validation**: AI-powered relevance assessment with OpenAI GPT-4o
- **Generation**: Context-aware response synthesis with OpenAI GPT-4o
- **Observability**: Request tracking and performance monitoring with LangSmith
- **Streaming**: Real-time token delivery for improved perceived responsiveness

## Limitations
- Relies on external API services (OpenAI, Pinecone)
- Requires appropriate API keys in environment
- Limited to content available in the vector database
- Responses strictly limited to information in retrieved passages
- Current implementation focuses exclusively on Satmar Chassidic texts
- Requires Hebrew language knowledge for optimal experience 