# Project Brief

## Project Overview
- **Name**: Divrei Yoel AI Chat (דברות קודש - חיפוש ועיון)
- **Type**: RAG-based question answering application
- **Initialization Date**: 2025-05-06
- **Focus**: Chassidic texts, specifically works of the Satmar Rebbe (Rabbi Yoel Teitelbaum)
- **Language**: Hebrew interface and content
- **Code Quality**: Rules compliance analysis completed on 2025-05-06
- **Last Documentation Update**: 2025-05-06 16:35:20

## Product Description
The Divrei Yoel AI Chat is a specialized retrieval-augmented generation (RAG) system designed to make the extensive teachings of Rabbi Yoel Teitelbaum of Satmar accessible through natural language interaction. Users can ask questions in Hebrew about various aspects of Chassidic thought, Jewish law, Biblical interpretation, and more, receiving answers that are:

1. Directly derived from the Satmar Rebbe's actual writings and teachings
2. Validated for relevance through AI analysis
3. Structured coherently with proper citations
4. Backed by expandable source text for verification and deeper study

Unlike traditional search engines, this application understands the semantic meaning behind questions, retrieves contextually relevant passages, validates their actual relevance, and synthesizes comprehensive answers while maintaining strict fidelity to the original sources.

## Project Goals
- Implement an advanced RAG (Retrieval-Augmented Generation) system for Chassidic texts
- Provide intelligent information retrieval with relevance validation
- Generate high-quality responses based strictly on retrieved content
- Maintain proper attribution to source materials
- Present information in Hebrew with appropriate RTL formatting
- Democratize access to specialized religious knowledge through modern AI technology
- Preserve the integrity and authenticity of traditional teachings
- Create an accessible research tool for scholars, students, and community members

## Technical Architecture
- **Frontend**: Streamlit web application with Hebrew RTL support
- **Backend**: Python-based RAG pipeline
- **Retrieval**: Pinecone vector database for semantic search
- **Validation**: OpenAI GPT-4o for relevance validation
- **Generation**: OpenAI GPT-4o for response synthesis
- **Monitoring**: LangSmith for observability and tracing
- **Deployment**: HuggingFace Spaces (indicated in README)

## Key Features
- Three-stage RAG pipeline (Retrieve → Validate → Generate)
- Source attribution in generated responses
- Interactive configuration of pipeline parameters
- Expandable source viewing for transparency
- Real-time processing status updates
- Streaming response generation
- Strong error handling with graceful degradation

## Core Functionality
- **Semantic Understanding**: Processes questions to identify key concepts and theological themes
- **Intelligent Retrieval**: Uses vector embeddings to find semantically related passages, not just keyword matches
- **Content Validation**: Applies GPT-4o to determine true relevance of each retrieved passage
- **Response Synthesis**: Generates cohesive, structured answers using only validated content
- **Citation Management**: Properly attributes information to original sources with AI-powered citation detection
- **Source Verification**: Provides expandable original text sections for transparency
- **Bilingual Interface**: Supports both Hebrew and English UI elements
- **Typography Optimization**: Specialized handling of Hebrew RTL text with font customization

## Current Phase
- VAN (Validation and Analysis) - Technical validation phase
- Memory Bank system initialization complete
- Rules compliance analysis completed with detailed findings
- Project assessment indicates moderate complexity (Level 2)
- 4 of 8 identified issues have been addressed
- PLAN mode completed successfully

## Compliance Status
- **Analyzed**: 19 Python files across all components
- **Rules Applied**: python.mdc, openai.mdc, asyncio.mdc, langsmith.mdc, pydantic.mdc, streamlit.mdc
- **General Assessment**: Good code quality with specific improvement areas
- **Issue Severity**: Mostly minor to medium issues, no critical vulnerabilities
- **Detailed Report**: See rules_compliance_report.md for comprehensive analysis

## Next Steps
- Complete remaining implementation tasks for identified issues
- Prioritize internationalization improvements for Hebrew text
- Address performance bottlenecks in UI rendering
- Implement service resilience mechanisms
- Consider expanding functionality with additional features

*Note: This brief has been expanded based on system analysis performed during the VAN phase.* 