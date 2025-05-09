import bleach  # For HTML sanitization
from bleach.css_sanitizer import CSSSanitizer
import re

def sanitize_html(html_content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks while preserving Hebrew text and RTL support.
    """
    if not isinstance(html_content, str):
        return str(html_content)
    
    # Check if this is raw HTML that might be showing up as code
    # Look for unescaped HTML tags that might be part of UI display issues
    raw_html_pattern = re.compile(r'^<div dir="(rtl|ltr)" lang="(he|en)" class="[^"]+">')
    if raw_html_pattern.search(html_content.strip()):
        # This might be raw HTML we need to render properly
        # Make sure it's properly structured
        if not html_content.strip().endswith('</div>'):
            html_content = html_content.strip() + '</div>'
    
    # Allowed HTML tags organized by purpose
    allowed_tags = [
        # Structure elements
        'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'pre',
        
        # Inline formatting
        'span', 'strong', 'em', 'b', 'i', 'u', 'code', 'sup', 'sub',
        
        # Interactive elements
        'a', 'img', 'button',
        
        # Layout elements
        'br', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
        
        # Style
        'style'
    ]
    
    # Allowed HTML attributes
    allowed_attributes = {
        # Global attributes
        '*': ['class', 'style', 'dir', 'lang'],
        
        # Specific elements
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'width', 'height'],
        'div': ['data-testid'],
        'button': ['kind']
    }
    
    # Essential CSS properties for proper text direction and sidebar positioning
    allowed_css_properties = [
        # Text formatting
        'font-family', 'font-size', 'font-weight', 'font-style',
        'text-align', 'direction', 'line-height', 'color',
        
        # Basic layout
        'display', 'margin', 'padding', 'width', 'height', 
        'border', 'border-radius', 'background-color',
        
        # Positioning (needed for sidebar)
        'position', 'top', 'right', 'bottom', 'left', 'z-index'
    ]
    
    # Create CSS sanitizer
    css_sanitizer = CSSSanitizer(allowed_css_properties=allowed_css_properties)
    
    # Sanitize and return the HTML
    return bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=css_sanitizer,
        strip=True
    )

def escape_html(text: str) -> str:
    """
    Escape HTML characters in a string to safely embed it within HTML.
    This is used for user inputs that should not contain HTML.
    
    Args:
        text (str): Text that might contain HTML characters
        
    Returns:
        str: Text with HTML characters escaped
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Replace HTML special characters with their entities
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;') 