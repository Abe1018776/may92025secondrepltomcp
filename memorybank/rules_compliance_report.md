# AI Code Rules Compliance Report

This report documents the evaluation of Python files in the `april28ragdivreyyoel` project against the provided coding rules and best practices.

## Evaluated Files:

*   `april28ragdivreyyoel/app.py`
*   `april28ragdivreyyoel/config.py`
*   `april28ragdivreyyoel/i18n.py`
*   `april28ragdivreyyoel/rag_processor.py`
*   `april28ragdivreyyoel/__init__.py`
*   `april28ragdivreyyoel/components/chat.py`
*   `april28ragdivreyyoel/components/prompt_gallery.py`
*   `april28ragdivreyyoel/components/sidebar.py`
*   `april28ragdivreyyoel/components/__init__.py`
*   `april28ragdivreyyoel/css/styles.py`
*   `april28ragdivreyyoel/css/__init__.py`
*   `april28ragdivreyyoel/prompts/system_prompt.py`
*   `april28ragdivreyyoel/prompts/validation_prompt.py`
*   `april28ragdivreyyoel/prompts/__init__.py`
*   `april28ragdivreyyoel/services/openai_service.py`
*   `april28ragdivreyyoel/services/retriever.py`
*   `april28ragdivreyyoel/services/__init__.py`
*   `april28ragdivreyyoel/utils/sanitization.py`
*   `april28ragdivreyyoel/utils/__init__.py`

---

## Findings for `april28ragdivreyyoel/app.py`

**Overall:** This file initializes and orchestrates a Streamlit application. It handles imports, logging, service initialization, page configuration, CSS styling, and chat interaction. It generally follows good practices for a Streamlit entry point.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Imports**: Well-organized.
    *   **Logging**: `logging` module is used appropriately.
    *   **Error Handling**: Good use of `try...except` for critical sections.
*   **`streamlit.mdc`**:
    *   **State Management**: Correct use of `st.session_state`.
    *   **Error Display**: `st.error()` used for user-facing errors.
    *   **CSS Handling**:
        *   **Issue ID**: APP-CSS-HACK
        *   **File**: `april28ragdivreyyoel/app.py`
        *   **Lines**: ~75-80, ~99-102
        *   **Description**: Uses `st.markdown` with `<style>` tags and a timestamp-based key to force CSS refresh. This is a common workaround but not the cleanest method. Consider static CSS files if possible.
        *   **Rule Violation**: `streamlit.mdc` (General best practices, maintainability).
        *   **Severity**: Minor.
    *   **`st.stop()` Usage**:
        *   **Issue ID**: APP-ST-STOP
        *   **File**: `april28ragdivreyyoel/app.py`
        *   **Lines**: 33, 38, 50
        *   **Description**: `st.stop()` is used appropriately to halt execution on fatal initialization errors. Logging appears adequate.
        *   **Rule Violation**: None (Informational, acceptable practice under `streamlit.mdc` Error Handling).
        *   **Severity**: Informational.
    *   **Caching**: No direct use of `@st.cache_data` or `@st.cache_resource` in `app.py`. This is likely acceptable as its role is orchestration. Caching should be implemented in the services/components it calls if they perform expensive operations.
*   **`openai.mdc` / `asyncio.mdc` / `langsmith.mdc` / `langchain.mdc` / `pydantic.mdc`**:
    *   No direct usage in this file. Evaluation for these rules will focus on other relevant modules (e.g., services, processing logic).

---

## Findings for `april28ragdivreyyoel/config.py`

**Overall:** This file manages application configuration, primarily by loading settings from environment variables using `python-dotenv`. It defines configurations for LangSmith, OpenAI, Pinecone, and RAG pipeline parameters.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Constants**: Configuration variables are correctly in uppercase.
    *   **Configuration Management**: Good use of `python-dotenv` and `os.environ.get`.
    *   **Secrets Handling**: API keys are loaded from environment variables, not hardcoded (Good).
    *   **Logging vs. Print**:
        *   **Issue ID**: CFG-PRINT-LOGGING
        *   **File**: `april28ragdivreyyoel/config.py`
        *   **Lines**: 15, 50, 54, 56
        *   **Description**: Uses `print()` for warnings and informational messages. It's recommended to use the `logging` module for consistency and better control, especially since logging is set up in `app.py`.
        *   **Rule Violation**: `python.mdc` (2.2 Logging).
        *   **Severity**: Minor.
*   **`openai.mdc`**:
    *   **Configuration**: `OPENAI_API_KEY` and model names are loaded from environment variables, aligning with best practices.
*   **`langsmith.mdc`**:
    *   **Configuration**: LangSmith environment variables are correctly handled and set for SDK consumption.
*   **`pydantic.mdc`**:
    *   **Configuration Validation**: 
        *   **Issue ID**: CFG-PYDANTIC-SETTINGS
        *   **File**: `april28ragdivreyyoel/config.py`
        *   **Lines**: Entire file, specifically `check_env_vars` (lines 41-45) and `os.environ.get` calls.
        *   **Description**: The file manually retrieves and checks environment variables. Pydantic's `BaseSettings` provides a more robust way to manage settings, including type casting, validation, and default values.
        *   **Rule Violation**: `pydantic.mdc` (Recommended Approaches - "Use BaseSettings for managing application settings.").
        *   **Suggestion**: Consider refactoring to use Pydantic `BaseSettings` for enhanced configuration management.
        *   **Severity**: Minor/Improvement.
*   **`asyncio.mdc`, `streamlit.mdc`, `langchain.mdc`**: Not directly applicable.

---

## Findings for `april28ragdivreyyoel/i18n.py`

**Overall:** This module handles internationalization (i18n) by storing translations and language-specific settings (fonts, example questions, system prompts) for Hebrew and English. It provides utility functions to access these based on the language selected in `st.session_state`.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Constants**: Language codes, translations, and other static data are correctly defined as uppercase constants.
    *   **Docstrings & Type Hinting**: Functions are generally well-documented with docstrings and type hints.
    *   **Maintainability (Translations)**:
        *   **Issue ID**: I18N-HARDCODED-TRANSLATIONS
        *   **File**: `april28ragdivreyyoel/i18n.py`
        *   **Lines**: `TRANSLATIONS` dictionary (lines 58-228).
        *   **Description**: Translations are embedded directly in the Python code. For easier management and scalability, especially if more languages or translators are involved, consider externalizing translations to dedicated files (e.g., JSON, YAML, .po).
        *   **Rule Adherence**: While not a direct violation of a listed rule, this relates to general maintainability principles in `python.mdc`.
        *   **Severity**: Informational/Improvement.
*   **`streamlit.mdc`**:
    *   **State Management**: Correctly uses `st.session_state` to retrieve the current language setting.
    *   **Internationalization**: Provides necessary i18n utilities for a Streamlit application.
    *   **Default Fonts for Non-Hebrew**:
        *   **Issue ID**: I18N-DEFAULT-FONTS
        *   **File**: `april28ragdivreyyoel/i18n.py`
        *   **Lines**: `get_font_options()` function (lines 245-248).
        *   **Description**: Defaults to Arial and Times New Roman for non-Hebrew. This is generally fine but could be made more configurable if support for more languages with specific font preferences is planned.
        *   **Rule Violation**: None.
        *   **Severity**: Informational.
*   **`openai.mdc`, `asyncio.mdc`, `langsmith.mdc`, `langchain.mdc`, `pydantic.mdc`**: Not directly applicable. System prompts for OpenAI are defined here, but the file does not interact with the API itself.

---

## Findings for `april28ragdivreyyoel/rag_processor.py`

**Overall:** This file implements the core RAG pipeline, including retrieval, validation, and generation steps. It utilizes `asyncio` for concurrent validation and `langsmith` for tracing.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Type Hinting**: Good usage.
    *   **Error Handling**: Generally good, with `traceback` for critical errors.
    *   **Docstrings**: Present for some functions; could be more comprehensive for pipeline steps and the main orchestrator.
    *   **Logging vs. Print**:
        *   **Issue ID**: RAG-PRINT-LOGGING
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Lines**: Multiple (e.g., 37, 46, 132, 143, 152, 184).
        *   **Description**: Uses `print()` for status updates, warnings, and errors. The `logging` module is preferred for consistency and better control.
        *   **Rule Violation**: `python.mdc` (2.2 Logging).
        *   **Severity**: Minor.
    *   **Long Orchestration Function**:
        *   **Issue ID**: RAG-LONG-FUNCTION
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Lines**: `execute_validate_generate_pipeline` function (lines 107-202).
        *   **Description**: The main pipeline function is long. Consider refactoring parts (e.g., query extraction, document simplification) into smaller helper functions for better readability.
        *   **Rule Adherence**: Relates to `python.mdc` (2.3 Anti-patterns - Long Methods).
        *   **Severity**: Minor/Improvement.
    *   **HTML in Responses**:
        *   **Issue ID**: RAG-HTML-IN-RESPONSE
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Lines**: e.g., 129, 161, 190, 193, 199.
        *   **Description**: The processor returns strings with HTML tags. It's cleaner for backend logic to return raw data, letting the presentation layer handle HTML formatting.
        *   **Rule Adherence**: Relates to `python.mdc` (1.4 Component Architecture - separation of concerns).
        *   **Severity**: Minor/Improvement.

*   **`asyncio.mdc`**:
    *   **`asyncio.gather`**: Correctly used for concurrent validation with `return_exceptions=True`.
    *   **Blocking Retriever Call**:
        *   **Issue ID**: RAG-ASYNC-SYNC-RETRIEVER
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Lines**: `run_retrieval_step` function, line 20: `retrieved_docs = retriever.retrieve_documents(...)`.
        *   **Description**: An `async` function calls a synchronous `retriever.retrieve_documents()`. If this performs blocking I/O, it will block the event loop.
        *   **Rule Violation**: `asyncio.mdc` (2.3 Anti-patterns - Blocking Calls, Mixing Synchronous and Asynchronous Code).
        *   **Suggestion**: `retrieve_documents` should be async or run in a thread pool executor (`asyncio.to_thread`).
        *   **Severity**: Medium.

*   **`langsmith.mdc`**:
    *   **Tracing Decorators**: `@traceable` is used on key pipeline functions.
    *   **Missing Tags & Metadata in Traces**:
        *   **Issue ID**: RAG-LS-MISSING-TAGS-META
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Lines**: `@traceable` decorators (e.g., 16, 26, 61, 106).
        *   **Description**: `@traceable` calls lack `tags` (e.g., `model:gpt-4o`) and `metadata` (e.g., `version:v1`, `sanitized:True`) as per `langsmith.mdc` guidelines.
        *   **Rule Violation**: `langsmith.mdc` (Tracing Requirements, Tagging & Metadata).
        *   **Severity**: Medium.
    *   **Input Sanitization for Tracing**:
        *   **Issue ID**: RAG-LS-INPUT-SANITIZATION
        *   **File**: `april28ragdivreyyoel/rag_processor.py`
        *   **Description**: Inputs like `query` and `history` are passed to traceable functions. Ensure these are sanitized *before* tracing if they contain sensitive information, and add `"sanitized": True` to metadata.
        *   **Rule Violation**: `langsmith.mdc` (Sanitation & Security).
        *   **Severity**: Medium.

*   **`openai.mdc`**, **`langchain.mdc`**, **`pydantic.mdc`**: Primarily orchestrates calls to other services; direct violations or applicability are limited in this file. Detailed OpenAI interactions are in `openai_service.py`.

---

## Findings for `april28ragdivreyyoel/__init__.py`

**Overall:** This is the top-level `__init__.py` for the `april28ragdivreyyoel` package. It currently only contains a comment.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Package Definition**: Correctly makes the directory a Python package.
    *   **Missing `__all__` and Docstring**:
        *   **Issue ID**: INIT-TOPLEVEL-METADATA
        *   **File**: `april28ragdivreyyoel/__init__.py`
        *   **Description**: The file lacks a module-level docstring and an `__all__` definition. While not critical for functionality if wildcard imports aren't used, adding these improves package clarity and explicitness of the public API.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - Dunder names).
        *   **Severity**: Minor/Informational.
*   Other rules are not applicable to this simple `__init__.py`.

---

## Findings for `april28ragdivreyyoel/components/__init__.py`

**Overall:** This `__init__.py` file marks the `components` directory as a Python package. It currently only contains a comment.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Package Definition**: Correctly makes the `components` directory a package.
    *   **Missing `__all__` and Docstring**:
        *   **Issue ID**: INIT-COMPONENTS-METADATA
        *   **File**: `april28ragdivreyyoel/components/__init__.py`
        *   **Description**: The file lacks a module-level docstring. Defining `__all__` would be beneficial to explicitly list the public components exported by this package (e.g., specific UI functions from `chat.py`, `sidebar.py`).
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - Dunder names).
        *   **Severity**: Minor/Informational.
*   Other rules are not applicable to this simple `__init__.py`.

---

## Findings for `april28ragdivreyyoel/components/chat.py`

**Overall:** This module provides Streamlit components for the chat interface, including message display, status updates, and prompt processing logic. It integrates asynchronous RAG pipeline execution.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Type Hinting & Docstrings**: Generally good.
    *   **Error Handling**: `try...except` blocks used in `process_prompt`.
    *   **Local Imports**:
        *   **Issue ID**: CHAT-LOCAL-IMPORTS
        *   **File**: `april28ragdivreyyoel/components/chat.py`
        *   **Lines**: e.g., 13-15, 60-61, 87-92.
        *   **Description**: Imports are performed inside functions to avoid circular dependencies. While a valid workaround, top-level imports are generally preferred. Refactoring dependencies might be a better long-term solution.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization).
        *   **Severity**: Minor/Improvement.
    *   **HTML in Python Strings**:
        *   **Issue ID**: CHAT-HTML-IN-PYTHON
        *   **File**: `april28ragdivreyyoel/components/chat.py`
        *   **Description**: Extensive use of f-strings to generate HTML with inline styles for `st.markdown`. This can make style maintenance difficult.
        *   **Rule Adherence**: Relates to `python.mdc` (Readability, Maintainability) and `streamlit.mdc` (Component Architecture).
        *   **Severity**: Minor/Improvement.
    *   **Repeated Font Styling Strings**:
        *   **Issue ID**: CHAT-REPEATED-FONT-STYLE
        *   **File**: `april28ragdivreyyoel/components/chat.py`
        *   **Description**: The CSS `font-family` string is duplicated multiple times. Centralize this to a constant or helper.
        *   **Rule Adherence**: `python.mdc` (2.3 Anti-patterns - Duplicate Code).
        *   **Severity**: Minor.

*   **`streamlit.mdc`**:
    *   **Component Design**: Defines logical UI components for chat.
    *   **State Management**: Uses `st.session_state` appropriately.
    *   **`unsafe_allow_html=True`**: Used with `st.markdown`. Sanitization (`sanitize_html`) is applied, which is crucial.

*   **`asyncio.mdc`**:
    *   **`nest_asyncio.apply()` Usage**:
        *   **Issue ID**: CHAT-NEST-ASYNCIO
        *   **File**: `april28ragdivreyyoel/components/chat.py`
        *   **Line**: 95.
        *   **Description**: `nest_asyncio.apply()` is used. This is a common workaround in Streamlit for running async code but can have subtle implications.
        *   **Rule Adherence**: `asyncio.mdc` (General best practices - event loop management).
        *   **Severity**: Informational.
    *   **`loop.run_until_complete()`**: Correctly used to bridge async calls into Streamlit's synchronous flow.

*   **`openai.mdc`**: Calls `extract_citations_with_openai` from `openai_service.py`. Direct compliance is in the service.

*   **`langsmith.mdc` / `langchain.mdc` / `pydantic.mdc`**: Not directly used in this file, but it orchestrates calls to traceable functions in `rag_processor.py`.

---

## Findings for `april28ragdivreyyoel/components/prompt_gallery.py`

**Overall:** This module defines a Streamlit component that displays a gallery of example prompts as buttons, allowing users to select one.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Docstrings**: The main function has a clear docstring.
    *   **Local Imports**:
        *   **Issue ID**: PGALLERY-LOCAL-IMPORTS
        *   **File**: `april28ragdivreyyoel/components/prompt_gallery.py`
        *   **Line**: 9.
        *   **Description**: `i18n` is imported locally within the function. See CHAT-LOCAL-IMPORTS for similar context.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization).
        *   **Severity**: Minor/Improvement.
    *   **Magic Number for Truncation**:
        *   **Issue ID**: PGALLERY-MAGIC-NUMBER
        *   **File**: `april28ragdivreyyoel/components/prompt_gallery.py`
        *   **Lines**: 30, 40.
        *   **Description**: Uses the literal `50` for truncating button text. This should be a named constant (e.g., `MAX_BUTTON_TEXT_LENGTH = 50`).
        *   **Rule Violation**: `python.mdc` (2.3 Anti-patterns - Magic Numbers/Strings).
        *   **Severity**: Minor.

*   **`streamlit.mdc`**:
    *   **Component Design**: A well-defined UI component.
    *   **State Management**: Uses `st.session_state` for the clicked question.
    *   **Layout**: Uses `st.columns` effectively.
    *   **HTML in Python String for Title**:
        *   **Issue ID**: PGALLERY-HTML-IN-PYTHON
        *   **File**: `april28ragdivreyyoel/components/prompt_gallery.py`
        *   **Line**: 13.
        *   **Description**: The `<h3>` title with inline styles is generated via an f-string.
        *   **Rule Adherence**: Relates to `python.mdc` (Readability, Maintainability) and `streamlit.mdc` (Component Architecture).
        *   **Severity**: Minor/Improvement.

*   **`openai.mdc`, `asyncio.mdc`, `langsmith.mdc`, `langchain.mdc`, `pydantic.mdc`**: Not directly applicable to this UI component.

---

## Findings for `april28ragdivreyyoel/components/sidebar.py`

**Overall:** This module defines the Streamlit sidebar, including settings for display (language, font), RAG parameters, and system/validation prompt editing. It also shows service status.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Docstrings & Type Hinting**: Good.
    *   **Local Imports**:
        *   **Issue ID**: SBAR-LOCAL-IMPORTS
        *   **File**: `april28ragdivreyyoel/components/sidebar.py`
        *   **Lines**: 10-13.
        *   **Description**: Imports are local to the main function. See CHAT-LOCAL-IMPORTS.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization).
        *   **Severity**: Minor/Improvement.
    *   **Runtime Modification of `config` Module**:
        *   **Issue ID**: SBAR-CONFIG-MODIFICATION
        *   **File**: `april28ragdivreyyoel/components/sidebar.py`
        *   **Lines**: 128-129.
        *   **Description**: Directly modifies `config.OPENAI_SYSTEM_PROMPT` and `config.VALIDATION_PROMPT_TEMPLATE`. This is an anti-pattern; configuration should generally be immutable after load or managed via a dedicated object/session state.
        *   **Rule Violation**: `python.mdc` (2.4 State Management, 2.3 Anti-patterns).
        *   **Severity**: Medium.
    *   **Magic Number for Max Validation**:
        *   **Issue ID**: SBAR-MAGIC-NUMBER-VALIDATE
        *   **File**: `april28ragdivreyyoel/components/sidebar.py`
        *   **Line**: 96 (`max_validate = min(n_retrieve, 100)`).
        *   **Description**: `100` is a hardcoded limit. Use a named constant.
        *   **Rule Violation**: `python.mdc` (2.3 Anti-patterns - Magic Numbers/Strings).
        *   **Severity**: Minor.

*   **`streamlit.mdc`**:
    *   **Component Design**: Clear sidebar component.
    *   **State Management**: Uses `st.session_state` and `st.rerun()` appropriately.
    *   **HTML/CSS in Python Strings**:
        *   **Issue ID**: SBAR-HTML-IN-PYTHON
        *   **File**: `april28ragdivreyyoel/components/sidebar.py`
        *   **Description**: Similar to other components, uses `st.markdown(unsafe_allow_html=True)` with dynamically generated HTML and inline styles.
        *   **Rule Adherence**: `python.mdc` (Readability, Maintainability), `streamlit.mdc` (Component Architecture).
        *   **Severity**: Minor/Improvement.
    *   **`st.stop()` Usage**:
        *   **Issue ID**: SBAR-ST-STOP
        *   **File**: `april28ragdivreyyoel/components/sidebar.py`
        *   **Line**: 83.
        *   **Description**: `st.stop()` is used if the retriever service is unavailable. This is an explicit design choice to halt further rendering/interaction if a key service is down.
        *   **Rule Adherence**: `streamlit.mdc` (Error Handling).
        *   **Severity**: Informational.

*   **`openai.mdc`, `asyncio.mdc`, `langsmith.mdc`, `langchain.mdc`, `pydantic.mdc`**: Not directly applicable beyond reading config values.

---

## Findings for `april28ragdivreyyoel/css/__init__.py`

**Overall:** This `__init__.py` file marks the `css` directory as a Python package. It currently only contains a comment.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Package Definition**: Correctly makes the `css` directory a package.
    *   **Missing `__all__` and Docstring**:
        *   **Issue ID**: INIT-CSS-METADATA
        *   **File**: `april28ragdivreyyoel/css/__init__.py`
        *   **Description**: The file lacks a module-level docstring. Defining `__all__` could be beneficial to explicitly list the public functions exported by this package (e.g., `generate_app_css` from `styles.py`).
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - Dunder names).
        *   **Severity**: Minor/Informational.
*   Other rules are not applicable to this simple `__init__.py`.

---

## Findings for `april28ragdivreyyoel/css/styles.py`

**Overall:** This module contains functions that generate CSS strings. These strings are then injected into the Streamlit app to customize its appearance, particularly for handling RTL text and Hebrew fonts.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Docstrings & Type Hinting**: Functions are documented and type-hinted.
    *   **CSS as Python Strings (Maintainability)**:
        *   **Issue ID**: CSS-IN-PYTHON
        *   **File**: `april28ragdivreyyoel/css/styles.py`
        *   **Description**: Large blocks of CSS are generated as Python f-strings. This makes CSS editing, linting, and maintenance difficult compared to using separate `.css` files.
        *   **Rule Adherence**: `python.mdc` (Readability, Maintainability).
        *   **Severity**: Medium.

*   **`streamlit.mdc` / CSS Best Practices**:
    *   **Overuse of `!important`**:
        *   **Issue ID**: CSS-IMPORTANT-OVERUSE
        *   **File**: `april28ragdivreyyoel/css/styles.py`
        *   **Description**: Numerous CSS rules use `!important`. This can lead to difficulties in managing CSS specificity and future overrides.
        *   **Rule Adherence**: General CSS best practice (relates to `streamlit.mdc` styling maintainability).
        *   **Severity**: Minor/Improvement.
    *   **Duplicated CSS `@import` Rules**:
        *   **Issue ID**: CSS-DUPLICATE-IMPORTS
        *   **File**: `april28ragdivreyyoel/css/styles.py`
        *   **Lines**: In `generate_app_css` (12-15) and `generate_dynamic_css` (225-228).
        *   **Description**: The same Google Font `@import` rules are present in both CSS generation functions, which is inefficient.
        *   **Rule Adherence**: General CSS best practice.
        *   **Severity**: Minor.
    *   **Aggressive CSS Selectors**:
        *   **Issue ID**: CSS-AGGRESSIVE-SELECTORS
        *   **File**: `april28ragdivreyyoel/css/styles.py`
        *   **Description**: Broad selectors like `[dir="rtl"] *` combined with `!important` are used. This is very aggressive and can have side effects or performance costs.
        *   **Rule Adherence**: General CSS best practice.
        *   **Severity**: Minor.

*   **`openai.mdc`, `asyncio.mdc`, `langsmith.mdc`, `langchain.mdc`, `pydantic.mdc`**: Not applicable.

---

## Findings for `april28ragdivreyyoel/prompts/__init__.py`

**Overall:** This `__init__.py` file initializes the `prompts` package. It re-exports constants from its submodules (`system_prompt.py` and `validation_prompt.py`) and includes a module docstring.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Package Definition & API Export**: Correctly defines `prompts` as a package and exports key constants. This is a good pattern.
    *   **Module Docstring**: Present and informative.
    *   **Missing `__all__` Definition**:
        *   **Issue ID**: INIT-PROMPTS-ALL
        *   **File**: `april28ragdivreyyoel/prompts/__init__.py`
        *   **Description**: While the file effectively defines a public API by re-exporting constants, explicitly defining `__all__ = ["OPENAI_SYSTEM_PROMPT", "VALIDATION_PROMPT_TEMPLATE"]` would align more closely with the `python.mdc` guideline to use `__all__` for public API definition.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - Dunder names).
        *   **Severity**: Minor/Informational.

*   Other rules are not directly applicable.

---

## Findings for `april28ragdivreyyoel/prompts/system_prompt.py`

**Overall:** This file defines the main system prompt (`OPENAI_SYSTEM_PROMPT`) used for OpenAI RAG generation. The prompt is a multi-line string with detailed instructions for the AI.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Constants**: The prompt is stored in an uppercase constant, which is good practice.
    *   **Docstring**: A module-level docstring is present.

*   **`openai.mdc`**:
    *   **Prompt Engineering**: The prompt itself is well-structured and detailed, adhering to good prompt engineering principles by providing clear instructions, role definition, constraints, and output requirements. This aligns with the recommendations in `openai.mdc` (2.2 Recommended Approaches).

*   No violations or significant issues noted against other rules for this file.

---

## Findings for `april28ragdivreyyoel/prompts/validation_prompt.py`

**Overall:** This file defines `VALIDATION_PROMPT_TEMPLATE`, an f-string template used to instruct an LLM (GPT-4o) to determine the relevance of a text paragraph to a user's question and respond in a specific JSON format.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Constants**: The prompt template is stored in an uppercase constant.
    *   **Docstring**: A module-level docstring is present.

*   **`openai.mdc`**:
    *   **Prompt Engineering**: The prompt is well-structured for its task. It uses placeholders for dynamic content and clearly specifies the expected JSON output format, which is a good practice for reliable, structured data extraction from LLMs, aligning with `openai.mdc` (2.2 Recommended Approaches).

*   No violations or significant issues noted against other rules for this file.

---

## Findings for `april28ragdivreyyoel/services/__init__.py`

**Overall:** This `__init__.py` file initializes the `services` package and re-exports key functions from its submodules (`retriever.py`, `openai_service.py`) to provide a unified API for the services.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Package Definition & API Export**: Correctly defines `services` as a package and exports a clear set of functions. This is a good pattern.
    *   **Missing `__all__` and Docstring**:
        *   **Issue ID**: INIT-SERVICES-METADATA
        *   **File**: `april28ragdivreyyoel/services/__init__.py`
        *   **Description**: The file lacks a module-level docstring. Explicitly defining `__all__` with the names of the re-exported functions (e.g., `"init_retriever"`, `"retrieve_documents"`, etc.) would fully align with `python.mdc` guidelines for public API definition.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - Dunder names).
        *   **Severity**: Minor/Informational.

*   Other rules are not directly applicable.

---

## Findings for `april28ragdivreyyoel/services/openai_service.py`

**Overall:** This module is responsible for all interactions with the OpenAI API. It initializes and uses an `AsyncOpenAI` client for validation, generation (streaming), and citation extraction tasks. It integrates with LangSmith for tracing.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Type Hinting & Docstrings**: Generally good.
    *   **Global Client State**:
        *   **Issue ID**: OPENAI-GLOBAL-CLIENT
        *   **File**: `april28ragdivreyyoel/services/openai_service.py`
        *   **Lines**: 15-17.
        *   **Description**: Manages the OpenAI client and its status using global variables. This can make testing and configuration management less flexible.
        *   **Rule Violation**: `python.mdc` (2.4 State Management - "Avoid Global State").
        *   **Suggestion**: Consider a class-based service or dependency injection.
        *   **Severity**: Medium.
    *   **Logging vs. Print**:
        *   **Issue ID**: OPENAI-PRINT-LOGGING
        *   **File**: `april28ragdivreyyoel/services/openai_service.py`
        *   **Description**: Uses `print()` extensively for logging. The `logging` module is preferred.
        *   **Rule Violation**: `python.mdc` (2.2 Logging).
        *   **Severity**: Minor.

*   **`openai.mdc`**:
    *   **Async Usage**: Correctly uses `AsyncOpenAI` client and `await`.
    *   **Configuration**: API key loaded from `config`.
    *   **JSON Mode**: `response_format={"type": "json_object"}` used effectively.
    *   **Missing Explicit Retries**:
        *   **Issue ID**: OPENAI-NO-RETRIES
        *   **File**: `april28ragdivreyyoel/services/openai_service.py`
        *   **Description**: Lacks explicit application-level retry logic with exponential backoff for API calls, as recommended by `openai.mdc` (2.2).
        *   **Rule Violation**: `openai.mdc` (2.2 Recommended Approaches).
        *   **Severity**: Minor/Improvement.

*   **`asyncio.mdc`**:
    *   **Correct Async Operations**: API calls are properly `async` and `await`ed.

*   **`langsmith.mdc`**:
    *   **Tracing Decorators**: Key functions are traced with `@traceable`.
    *   **Missing Tags & Metadata in Traces**:
        *   **Issue ID**: OPENAI-LS-MISSING-TAGS-META
        *   **File**: `april28ragdivreyyoel/services/openai_service.py`
        *   **Lines**: `@traceable` decorators (lines 51, 96, 183).
        *   **Description**: `@traceable` calls lack `tags` (e.g., `model:gpt-4o`) and `metadata` as per `langsmith.mdc` guidelines.
        *   **Rule Violation**: `langsmith.mdc` (Tracing Requirements, Tagging & Metadata).
        *   **Severity**: Medium.
    *   **Input Sanitization for Tracing**:
        *   **Issue ID**: OPENAI-LS-INPUT-SANITIZATION
        *   **File**: `april28ragdivreyyoel/services/openai_service.py`
        *   **Description**: Ensure inputs (questions, history, text for prompts) are sanitized *before* LangSmith tracing if they contain sensitive data, and add `"sanitized": True` metadata.
        *   **Rule Violation**: `langsmith.mdc` (Sanitation & Security).
        *   **Severity**: Medium.

*   **`pydantic.mdc`**, **`langchain.mdc`**, **`streamlit.mdc`**: Not directly applicable.

---

## Findings for `april28ragdivreyyoel/services/retriever.py`

**Overall:** This module handles document retrieval from Pinecone. It includes initialization of the Pinecone client and index, and a function to retrieve documents based on query embeddings.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Problematic Dynamic Imports**:
        *   **Issue ID**: RET-DYNAMIC-IMPORTS
        *   **File**: `april28ragdivreyyoel/services/retriever.py`
        *   **Lines**: 13-22.
        *   **Description**: Uses `sys.path.insert` and `importlib.util` for importing `config` and `utils`. This is a major anti-pattern, breaking static analysis and standard Python import behaviors. Project structure or PYTHONPATH should be corrected to allow standard imports.
        *   **Rule Violation**: `python.mdc` (1.3 Module Organization, maintainability).
        *   **Severity**: Critical.
    *   **Global Client State**:
        *   **Issue ID**: RET-GLOBAL-CLIENT
        *   **File**: `april28ragdivreyyoel/services/retriever.py`
        *   **Lines**: 28-31.
        *   **Description**: Pinecone client/index and status are global variables.
        *   **Rule Violation**: `python.mdc` (2.4 State Management).
        *   **Severity**: Medium.
    *   **Logging vs. Print**:
        *   **Issue ID**: RET-PRINT-LOGGING
        *   **File**: `april28ragdivreyyoel/services/retriever.py`
        *   **Description**: Uses `print()` for logging throughout.
        *   **Rule Violation**: `python.mdc` (2.2 Logging).
        *   **Severity**: Minor.

*   **`langsmith.mdc`**:
    *   **Tracing Decorator**: `retrieve_documents` is traced.
    *   **Missing Tags & Metadata in Traces**:
        *   **Issue ID**: RET-LS-MISSING-TAGS-META
        *   **File**: `april28ragdivreyyoel/services/retriever.py`
        *   **Line**: 71.
        *   **Description**: `@traceable` call lacks `tags` and `metadata`.
        *   **Rule Violation**: `langsmith.mdc` (Tracing Requirements, Tagging & Metadata).
        *   **Severity**: Medium.
    *   **Input Sanitization for Tracing (Query)**:
        *   **Issue ID**: RET-LS-QUERY-SANITIZATION
        *   **File**: `april28ragdivreyyoel/services/retriever.py`
        *   **Description**: `query_text` is traced. Ensure sanitization if it's raw user input.
        *   **Rule Violation**: `langsmith.mdc` (Sanitation & Security).
        *   **Severity**: Medium.

*   **`asyncio.mdc`**:
    *   **Synchronous Operations**: The `retrieve_documents` function and its dependency `get_embedding` are synchronous. If `get_embedding` (from `utils`) performs blocking I/O for embeddings (e.g., to OpenAI), this chain can block. This is particularly relevant given `rag_processor.py` calls `retrieve_documents` from an async path (see RAG-ASYNC-SYNC-RETRIEVER).
        *   **Issue ID**: RET-SYNC-EMBEDDING
        *   **File**: `april28ragdivreyyoel/services/retriever.py` (and its usage of `utils.get_embedding`).
        *   **Description**: Potential blocking I/O in a synchronous function called from an async context.
        *   **Rule Violation**: `asyncio.mdc` (Blocking Calls).
        *   **Severity**: Medium (dependent on `get_embedding` implementation).

*   **`openai.mdc`**: Interacts via `get_embedding`, presumably using OpenAI. API key is checked.

*   Other rules not directly applicable or covered by points above.

---

## Findings for `april28ragdivreyyoel/utils/__init__.py`

**Overall:** This file serves as the `__init__.py` for the `utils` package and also directly contains utility function implementations for text cleaning, OpenAI embeddings, and context formatting.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Problematic Dynamic `config` Import**:
        *   **Issue ID**: UTIL-DYNAMIC-CONFIG-IMPORT
        *   **File**: `april28ragdivreyyoel/utils/__init__.py`
        *   **Lines**: 9-13.
        *   **Description**: Uses `sys.path.append` and manual import for `config`. This is a major anti-pattern. Standard Python imports should be used.
        *   **Rule Violation**: `python.mdc` (1.3 Module Organization, maintainability).
        *   **Severity**: Critical.
    *   **Implementation in `__init__.py`**:
        *   **Issue ID**: UTIL-INIT-IMPLEMENTATION
        *   **File**: `april28ragdivreyyoel/utils/__init__.py`
        *   **Description**: Contains utility function definitions directly. It's cleaner to place these in separate modules within `utils` and use `__init__.py` for re-exporting.
        *   **Rule Adherence**: `python.mdc` (1.3 Module Organization - for clarity).
        *   **Severity**: Minor/Improvement.
    *   **Logging vs. Print**:
        *   **Issue ID**: UTIL-PRINT-LOGGING
        *   **File**: `april28ragdivreyyoel/utils/__init__.py`
        *   **Description**: Uses `print()` for error/warning messages.
        *   **Rule Violation**: `python.mdc` (2.2 Logging).
        *   **Severity**: Minor.
    *   **Missing `__all__`**:
        *   **Issue ID**: UTIL-INIT-ALL
        *   **File**: `april28ragdivreyyoel/utils/__init__.py`
        *   **Description**: Does not define `__all__` to declare its public API.
        *   **Rule Violation**: `python.mdc` (1.3 Module Organization).
        *   **Severity**: Minor/Informational.

*   **`openai.mdc` & `asyncio.mdc`**:
    *   **Synchronous `get_embedding` with Blocking Calls**:
        *   **Issue ID**: UTIL-SYNC-EMBEDDING
        *   **File**: `april28ragdivreyyoel/utils/__init__.py`
        *   **Function**: `get_embedding`.
        *   **Description**: Uses the synchronous `openai.OpenAI` client and `time.sleep()`, making it blocking. This impacts async performance if called from an async path.
        *   **Rule Violation**: `asyncio.mdc` (Blocking Calls), `openai.mdc` (Async recommended).
        *   **Suggestion**: Convert to `async` using `openai.AsyncOpenAI` and `asyncio.sleep()`.
        *   **Severity**: Medium/High.
    *   **Retry Logic**: `get_embedding` includes retry logic for OpenAI calls, which is good, but uses blocking `time.sleep()`.

*   Other rules not directly applicable.

---

## Findings for `april28ragdivreyyoel/utils/sanitization.py`

**Overall:** This module provides an HTML sanitization function (`sanitize_html`) using the `bleach` library. It defines allowed HTML tags and attributes to prevent XSS vulnerabilities while permitting necessary formatting.

**Rule-Specific Observations & Potential Issues:**

*   **`python.mdc`**:
    *   **Docstrings & Type Hinting**: The function is well-documented and type-hinted.
    *   **Security**: Implements HTML sanitization using `bleach`, which is a good security practice.

*   **`streamlit.mdc`**:
    *   **Security (Input Validation)**: This utility is crucial for safely using `unsafe_allow_html=True` in Streamlit components, aligning with security best practices.

*   **`langsmith.mdc`**:
    *   **Sanitization Utility**: This module provides the sanitization mechanism mentioned in the `langsmith.mdc` rule. The correct application of this function *before* data is traced by LangSmith in other modules (like `rag_processor.py` or `openai_service.py`) is key for compliance with that rule's data safety aspects.

*   No specific violations noted for this utility file itself against other rules. Its effectiveness depends on its proper use elsewhere.

--- 