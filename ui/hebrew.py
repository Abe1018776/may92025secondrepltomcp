import re
from typing import Optional

def contains_hebrew(text: str) -> bool:
    """
    Check if text contains Hebrew characters.

    Args:
        text (str): Text to check

    Returns:
        bool: True if text contains Hebrew characters
    """
    # Hebrew Unicode range (1,424–1,535) plus some additional ranges for Hebrew characters
    hebrew_pattern = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]')
    return bool(hebrew_pattern.search(text))

def contains_english(text: str) -> bool:
    """
    Check if text contains English characters.

    Args:
        text (str): Text to check

    Returns:
        bool: True if text contains English characters
    """
    english_pattern = re.compile(r'[a-zA-Z]')
    return bool(english_pattern.search(text))

def handle_mixed_language_text(text: str, hebrew_font: str = None) -> str:
    """
    Handle mixed language text with proper RTL markers and CSS.

    Args:
        text (str): The input text to process
        hebrew_font (str, optional): The Hebrew font to use

    Returns:
        str: The processed text with proper RTL markers
    """
    # Always use David Libre font for consistency
    hebrew_font = "David Libre"

    # Check if text already contains HTML tags - if so, it may be a rendered template
    # that we should pass through without additional processing
    html_tag_pattern = re.compile(r'<[a-z]+[^>]*>')
    if html_tag_pattern.search(text):
        # If it contains HTML tags, return it as is
        # It's likely already properly formatted HTML from a template
        return text

    # Process normal text
    has_hebrew = contains_hebrew(text)
    has_english = contains_english(text)

    if has_hebrew and has_english:
        # For mixed language content, we need to identify and wrap English words
        # Split by whitespace to find words
        words = text.split()
        processed_words = []

        for word in words:
            # If word contains English but not Hebrew, wrap it in LTR span
            if contains_english(word) and not contains_hebrew(word):
                processed_words.append(f'<span dir="ltr">{word}</span>')
            else:
                processed_words.append(word)

        # Join words back with spaces
        processed_text = ' '.join(processed_words)

        # Wrap everything in RTL container
        return f"""
        <div dir="rtl" lang="he" class="rtl-text mixed-content hebrew-font">
            {processed_text}
        </div>
        """
    elif has_hebrew:
        # For Hebrew-only content, use RTL direction
        return f"""
        <div dir="rtl" lang="he" class="rtl-text hebrew-font">
            {text}
        </div>
        """
    else:
        # For English-only content, use LTR direction
        return f"""
        <div dir="ltr" lang="en" class="ltr-text hebrew-font">
            {text}
        </div>
        """