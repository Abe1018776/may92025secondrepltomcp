"""
Prompt module initialization.
Provides access to system and validation prompts.
"""

from .system_prompt import OPENAI_SYSTEM_PROMPT
from .validation_prompt import VALIDATION_PROMPT_TEMPLATE
from .templates import get_templates_for_language, get_template_by_id 