"""
Internationalization module for the DivreiYoel app.
Provides translations and language-specific settings.
"""
from typing import Dict, Any, Optional, List
import streamlit as st

# Constants
LANGUAGES = {
    "he": "עברית",  # Hebrew
    "en": "English"
}

DEFAULT_LANGUAGE = "he"  # Default language is Hebrew

# Hebrew font options
HEBREW_FONTS = {
    "David": "דוד",
    "Miriam": "מרים",
    "Narkisim": "נרקיסים",
    "Taamey Frank CLM": "טעמי פרנק",
    "Noto Rashi Hebrew": 'נוטו רש"י'  # Added Noto Rashi Hebrew
}

# Generic RTL languages
RTL_LANGUAGES = ["he", "ar"]

# Example questions/prompt starters for each language
EXAMPLE_QUESTIONS = {
    "he": [
        "כל הקושי והצער שיש להאדם הוא רק בשביל התפילה, אבל צעקה שבאה מבלבול ויאוש, ומבלי שום תקוה שישועתו קרובה לבא - אין לה שם תפילה, אלא מאי? במצב כזה של קושי, צריך היהודי להודות על כל הטוב שהיטיב עמו הקב״ה עד היום, ולבקש בקשה ותפילה גדולה על העתיד, ומיד לקום ולעשות איזה מעשה של השתדלות, בכדי להראות שאינו נכנס למצב של יאוש וחוסר אונים, אלא אדרבה הוא מלא אמונה ותקוה שהעתיד יהא בעז״ה כולו טוב ורחמים. וצריך השתדלות מבלי להבין איך תתצמח להם הישועה, והקב״ה כבר יפתח להם שערי ישועה.",
        "יותר קל להוציא את היהודי מן הגלות מאשר להוציא את הגלות מן היהודי",
        "איך היהודים עשו צדקה במדבר, בהנחה שלכולם היה מן (צרכים בסיסיים)?",
        "למה הים לא נבקע מיד כשהיהודים עמדו מולו, ורק נבקע אחרי שזעקו להשם?"
    ],
    "en": [
        "\"ויקחו לי תרומה\" teaches that if a person commits and yearns to give charity, then Hashem will definitely make sure that he gets the money to give even if he doesn't have the money yet.",
        "Why didn't the sea split immediately when the Jews were standing in front of it, and only split after they cried out to Hashem?",
        "Money and riches in itself is not a good thing rather if a person prays for it with the intent of good deeds he merits abundance.",
        "How did the Jews practice charity in the desert, given that everyone had manna (basic needs met)?"
    ]
}

# System prompts for each language
SYSTEM_PROMPTS = {
    "he": "אתה עוזר חכם שמתמחה בפירוש דברי רבי יואל. השתמש בטקסטים שסופקו ואל תמציא מידע שאינו קיים.",
    "en": "You are a helpful assistant specializing in interpreting Rabbi Yoel's teachings. Use the provided texts and do not fabricate information."
}

# Translation dictionaries
TRANSLATIONS = {
    "he": {
        # App title and headings
        "app_title": "דברות קודש - חיפוש ועיון",
        "app_subtitle": "מבוסס על ספרי דברי יואל מסאטמאר זצוק'ל",
        
        # Settings
        "settings_title": "הגדרות מערכת",
        "display_settings": "הגדרות תצוגה",
        "language_setting": "שפה",
        "font_setting": "גופן עברי",
        "retriever_status": "מאחזר (Pinecone):",
        "retriever_error": "מאחזר אינו זמין.",
        "openai_status": "OpenAI:",
        "openai_error": "OpenAI אינו זמין.",
        
        # RAG settings
        "retrieval_count": "מספר פסקאות לאחזור",
        "validation_count": "פסקאות לאימות (GPT-4o)",
        "validation_info": "התשובות מבוססות רק על המקורות שאומתו.",
        "edit_prompts": "עריכת פרומפטים",
        "system_prompt": "פרומפט מערכת (מחולל)",
        "validation_prompt": "פרומפט אימות (GPT-4o)",
        
        # Chat interface
        "chat_placeholder": "שאל שאלה על תורת החסידות...",
        "example_questions": "שאלות לדוגמה",
        "prompt_templates": "תבניות שאלות",
        "template_active_message": "תבנית פעילה. הקלד את השאלה שלך והקש על שלח.",
        "processing": "מעבד שאלה...",
        "processing_step": "מעבד:",
        "processing_complete": "עיבוד הושלם!",
        "sources_title": "מקורות",
        "sources_text": "מציג {} קטעי מקור שנשלחו ליצירת התשובה",
        "source_label": "מקור {}:",
        "unknown_source": "מקור לא ידוע",
        "processing_details": "פרטי העיבוד",
        "processing_log": "יומן עיבוד מפורט",
        "no_response": "לא התקבלה תשובה מהמחולל.",
        "use_this_question": "השתמש בשאלה זו",
        "use_this_template": "השתמש בתבנית זו",
        "show_full_prompt": "הצג את השאלה המלאה",
        
        # Errors
        "error": "שגיאה",
        "critical_error": "שגיאה קריטית!",
        "request_error": "שגיאה בטיפול בבקשה!",
        "communication_error": "שגיאה בלתי צפויה בתקשורת.",
        "reload": "נסה לרענן.",
        "details": "פרטים",
        "error_async": "שגיאה בתהליך הטיפול האסינכרוני:",
        
        # RAG pipeline status messages
        "retrieving_docs": "1. מאחזר עד {} פסקאות מ-Pinecone...",
        "retrieved_docs": "1. אוחזרו {} פסקאות ב-{} שניות.",
        "no_docs_found": "1. לא אותרו מסמכים.",
        "validating_docs": "2. [GPT-4o] מתחיל אימות מקבילי ({} / {} פסקאות)...",
        "skipping_validation": "2. [GPT-4o] דילוג על אימות - אין פסקאות.",
        "filtering_docs": "3. [GPT-4o] סינון פסקאות לפי תוצאות אימות...",
        "validation_complete": "2. אימות GPT-4o הושלם ({} עברו, {} נדחו, {} שגיאות) ב-{} שניות.",
        "filtered_docs": "3. נאספו {} פסקאות רלוונטיות לאחר אימות GPT-4o.",
        "generating_response": "4. [{}] מחולל תשובה סופית מ-{} קטעי הקשר...",
        "skipping_generation": "4. [{}] דילוג על יצירה - אין פסקאות להקשר.",
        "generation_error": "4. שגיאה ביצירת התשובה ({}) ב-{} שניות.",
        "generation_complete": "4. יצירת התשובה ({}) הושלמה ב-{} שניות.",
        "generation_critical_error": "4. שגיאה קריטית ביצירת התשובה ({}) ב-{} שניות.",
        "no_relevant_passages": "לא נמצאו פסקאות רלוונטיות.",
        "no_sources_for_response": "לא סופקו פסקאות רלוונטיות ליצירת התשובה.",
        
        # Font preview
        "font_preview": "דוגמה לטקסט בגופן {}",
    },
    
    "en": {
        # App title and headings
        "app_title": "Sacred Discourses - Search and Study",
        "app_subtitle": "Based on the books of Divrei Yoel of Satmar zt\"l",
        
        # Settings
        "settings_title": "System Settings",
        "display_settings": "Display Settings",
        "language_setting": "Language",
        "font_setting": "Hebrew Font",
        "retriever_status": "Retriever (Pinecone):",
        "retriever_error": "Retriever unavailable.",
        "openai_status": "OpenAI:",
        "openai_error": "OpenAI unavailable.",
        
        # RAG settings
        "retrieval_count": "Passages to retrieve",
        "validation_count": "Passages to validate (GPT-4o)",
        "validation_info": "Answers are based only on validated sources.",
        "edit_prompts": "Edit Prompts",
        "system_prompt": "System prompt (generator)",
        "validation_prompt": "Validation prompt (GPT-4o)",
        
        # Chat interface
        "chat_placeholder": "Ask a question about Chassidic teachings...",
        "example_questions": "Example Questions",
        "prompt_templates": "Prompt Templates",
        "template_active_message": "Template is active. Type your question and hit Send.",
        "processing": "Processing question...",
        "processing_step": "Processing:",
        "processing_complete": "Processing complete!",
        "sources_title": "Sources",
        "sources_text": "Showing {} source passages sent to the generator",
        "source_label": "Source {}:",
        "unknown_source": "Unknown source",
        "processing_details": "Processing Details",
        "processing_log": "Detailed processing log",
        "no_response": "No response received from the generator.",
        "use_this_question": "Use this question",
        "use_this_template": "Use this template",
        "show_full_prompt": "Show Full Prompt",
        
        # Errors
        "error": "Error",
        "critical_error": "Critical Error!",
        "request_error": "Error processing request!",
        "communication_error": "Unexpected communication error.",
        "reload": "Try refreshing.",
        "details": "Details",
        "error_async": "Error in asynchronous process:",
        
        # RAG pipeline status messages
        "retrieving_docs": "1. Retrieving up to {} paragraphs from Pinecone...",
        "retrieved_docs": "1. Retrieved {} paragraphs in {} seconds.",
        "no_docs_found": "1. No documents found.",
        "validating_docs": "2. [GPT-4o] Starting parallel validation ({} / {} paragraphs)...",
        "skipping_validation": "2. [GPT-4o] Skipping validation - no paragraphs.",
        "filtering_docs": "3. [GPT-4o] Filtering paragraphs based on validation results...",
        "validation_complete": "2. GPT-4o validation complete ({} passed, {} rejected, {} errors) in {} seconds.",
        "filtered_docs": "3. Collected {} relevant paragraphs after GPT-4o validation.",
        "generating_response": "4. [{}] Generating final response from {} context passages...",
        "skipping_generation": "4. [{}] Skipping generation - no paragraphs for context.",
        "generation_error": "4. Error generating response ({}) in {} seconds.",
        "generation_complete": "4. Response generation ({}) completed in {} seconds.",
        "generation_critical_error": "4. Critical error in response generation ({}) in {} seconds.",
        "no_relevant_passages": "No relevant passages found.",
        "no_sources_for_response": "No relevant passages were provided to generate the response.",
        
        # Font preview
        "font_preview": "Sample text in {} font",
    }
}

# Get the current language from session state
def get_current_language() -> str:
    """
    Get the current language from session state.
    
    Returns:
        str: Current language code
    """
    return st.session_state.get("language", DEFAULT_LANGUAGE)

# Get text direction (RTL or LTR) based on the current language
def get_direction() -> str:
    """
    Get the text direction (RTL or LTR) based on the current language.
    
    Returns:
        str: "rtl" for Right-to-Left languages, "ltr" otherwise
    """
    current_lang = get_current_language()
    return "rtl" if current_lang in RTL_LANGUAGES else "ltr"

# Get the display name of the current language
def get_language_name() -> str:
    """
    Get the display name of the current language.
    
    Returns:
        str: Language name
    """
    current_lang = get_current_language()
    return LANGUAGES.get(current_lang, LANGUAGES[DEFAULT_LANGUAGE])

# Get font options for the current language
def get_font_options() -> Dict[str, str]:
    """
    Get font options for the current language.
    
    Returns:
        Dict[str, str]: Font options mapping
    """
    current_lang = get_current_language()
    if current_lang == "he":
        return HEBREW_FONTS
    else:
        return {"Arial": "Arial", "Times New Roman": "Times New Roman"}

# Get example questions for the current language
def get_example_questions() -> List[str]:
    """
    Get example questions for the current language.
    
    Returns:
        List[str]: List of example questions
    """
    current_lang = get_current_language()
    return EXAMPLE_QUESTIONS.get(current_lang, EXAMPLE_QUESTIONS[DEFAULT_LANGUAGE])

# Get prompt templates for the current language
def get_prompt_templates() -> List[Dict[str, Any]]:
    """
    Get prompt templates for the current language.
    
    Returns:
        List[Dict[str, Any]]: List of prompt templates
    """
    from prompts.templates import get_templates_for_language
    current_lang = get_current_language()
    return get_templates_for_language(current_lang)

# Get system prompts for the current language
def get_system_prompts() -> str:
    """
    Get system prompts for the current language.
    
    Returns:
        str: System prompt
    """
    current_lang = get_current_language()
    return SYSTEM_PROMPTS.get(current_lang, SYSTEM_PROMPTS[DEFAULT_LANGUAGE])

# Get translated text by key
def get_text(key: str) -> str:
    """
    Get translated text for a given key.
    
    Args:
        key (str): Translation key
        
    Returns:
        str: Translated text for the current language
    """
    current_lang = get_current_language()
    
    # Get translation for current language, fallback to English or key itself
    if key in TRANSLATIONS.get(current_lang, {}):
        return TRANSLATIONS[current_lang][key]
    elif key in TRANSLATIONS.get("en", {}):
        return TRANSLATIONS["en"][key]
    elif key in TRANSLATIONS.get(DEFAULT_LANGUAGE, {}):
        return TRANSLATIONS[DEFAULT_LANGUAGE][key]
    else:
        return key

# Get current user prompt starters
def get_current_user_prompt_starters() -> List[str]:
    """
    Get prompt starters for the current language.
    
    Returns:
        List[str]: List of prompt starters
    """
    return get_example_questions() 