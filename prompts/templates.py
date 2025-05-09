"""
Prompt templates module for the DivreiYoel app.
Provides structured templates for common query patterns.
"""
from typing import Dict, Any, List
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Template structure:
# - id: Unique identifier for the template
# - name: Display name for the template (localized)
# - template: The template text that prefixes user input
# - isolate_query: Whether to isolate the user's query when searching Pinecone
# - description: Optional description of what the template does
# - language_code: The language code this template belongs to (added for verification)

PROMPT_TEMPLATES = {
    "he": [
        {
            "id": "dvar_torah_support",
            "name": "גיבוי לרעיון לדבר תורה",
            "template": """תפקידך הוא לעזור לי לגבות את רעיונות דברי התורה שלי ולתמוך בהם עם מקורות שיכולים לתמוך במושג או במושגים שאני מבסס עליהם את דבר התורה שלי.

עליך להעריך בקפידה כל דבר תורה כדי לראות אם וכיצד הוא יכול לעזור לגבות את דבר התורה שלי, עליך להשתמש ביצירתיות והיגיון כדי להגיע לכך.

הנה הרעיון שאני מחפש לגבות:
""",
            "isolate_query": True,
            "description": "מציאת מקורות לתמיכה ברעיון דבר תורה",
            "language_code": "he"
        }
    ],
    "en": [
        {
            "id": "dvar_torah_support",
            "name": "Dvar Torah Support",
            "template": """Your job is to help me back up my dvar torah ideas that I come up with and back it up with sources that can support the concept or concepts that I'm basing my dvar torah on.

You have to carefully evaluate each dvar torah to see if and how it can help back up this dvar torah of mine and how, you have to use some creativity and reasoning in order to get to that.

Here's the idea that I'm looking to backup:
""",
            "isolate_query": True,
            "description": "Find sources to support a dvar torah concept",
            "language_code": "en"
        }
    
    ]
}

def get_templates_for_language(language_code: str) -> List[Dict[str, Any]]:
    """
    Get all prompt templates for a specific language.
    
    Args:
        language_code (str): Language code ('he' or 'en')
        
    Returns:
        List[Dict[str, Any]]: List of template objects for the language
    """
    # Log the requested language code to help debug
    logger.info(f"Getting templates for language code: {language_code}")
    
    # Strict language matching - only return templates for the exact language
    templates = PROMPT_TEMPLATES.get(language_code, [])
    
    # Fallback to English if no templates found for the requested language
    if not templates and language_code != "en":
        logger.warning(f"No templates found for {language_code}, falling back to English templates")
        templates = PROMPT_TEMPLATES.get("en", [])
    
    # Add language_code to each template if not already present
    for template in templates:
        if "language_code" not in template:
            template["language_code"] = language_code
    
    # Log the number of templates found
    logger.info(f"Found {len(templates)} templates for language: {language_code}")
    
    return templates

def get_template_by_id(template_id: str, language_code: str) -> Dict[str, Any]:
    """
    Get a specific template by ID for a language.
    
    Args:
        template_id (str): Template identifier
        language_code (str): Language code ('he' or 'en')
        
    Returns:
        Dict[str, Any]: Template object or empty dict if not found
    """
    # Log the requested template lookup
    logger.info(f"Looking up template ID '{template_id}' for language: {language_code}")
    
    templates = get_templates_for_language(language_code)
    for template in templates:
        if template.get("id") == template_id:
            logger.info(f"Found template: {template.get('name', 'Unnamed')}")
            return template
    
    logger.warning(f"Template with ID '{template_id}' not found for language: {language_code}")
    return {} 