# Utilities Module Guide

## Overview
The `utils/` directory contains utility functions and helper classes that support the Divrei Yoel AI Chat application. These utilities handle common tasks like logging, text processing, validation, and error handling used throughout the application.

## Key Utility Modules

### Logging Utilities (`utils/logging.py`)

#### Logger Configuration
```python
def configure_logging():
    """Configure application-wide logging with appropriate handlers and formatters."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
```
- Sets up centralized logging for the application
- Configures both console and file output
- Uses log level from configuration
- Provides consistent timestamp and context format

#### Specialized Loggers
```python
def get_service_logger(service_name):
    """Get a logger for a specific service with appropriate configuration."""
    logger = logging.getLogger(f"service.{service_name}")
    return logger
```
- Creates named loggers for different application components
- Enables filtering and specialized handling by service
- Maintains hierarchical logger organization

### Text Processing (`utils/text.py`)

#### Hebrew Text Handling
```python
def process_hebrew_text(text):
    """Process Hebrew text to ensure proper RTL handling and character encoding."""
    # Remove any BOM or invisible direction markers
    text = re.sub(r'[\u200e\u200f\u061c\ufeff]', '', text)
    return text
```
- Cleans Hebrew text for display and processing
- Removes invisible directional markers
- Ensures consistent encoding

#### HTML Sanitization
```python
def sanitize_html(html_content):
    """Sanitize HTML content to prevent XSS and ensure safe display."""
    # Allow only safe tags and attributes
    allowed_tags = ['p', 'b', 'i', 'em', 'strong', 'br', 'div', 'span']
    allowed_attrs = {'span': ['class'], 'div': ['class']}
    
    cleaner = Cleaner(
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
        remove_unknown_tags=False
    )
    
    return cleaner.clean_html(html_content)
```
- Removes dangerous HTML tags and attributes
- Preserves formatting tags needed for display
- Prevents cross-site scripting vulnerabilities

### Validation Utilities (`utils/validation.py`)

#### Input Validation
```python
def validate_query(query):
    """Validate user query meets minimum requirements."""
    if not query or len(query.strip()) < 2:
        return False, "Query is too short"
    return True, "Valid query"
```
- Ensures inputs meet minimum requirements
- Prevents empty or nonsensical queries
- Returns validation status and message

#### Document Processing
```python
def validate_documents(documents):
    """Validate document structure and content."""
    if not documents:
        return False, "No documents provided"
        
    for doc in documents:
        if 'hebrew_text' not in doc or not doc['hebrew_text']:
            return False, "Document missing required Hebrew text"
            
    return True, "Valid documents"
```
- Verifies document structures before processing
- Ensures required fields are present
- Prevents processing of invalid documents

### Error Handling (`utils/errors.py`)

#### Exception Wrappers
```python
def safe_execute(func, default_return=None, error_message="Function execution failed"):
    """Execute a function safely, capturing and logging any exceptions."""
    try:
        return func()
    except Exception as e:
        logging.error(f"{error_message}: {str(e)}")
        return default_return
```
- Provides a standard way to handle exceptions
- Logs errors consistently
- Returns safe default values
- Maintains application stability

#### User-Friendly Error Messages
```python
def get_user_friendly_error(exception):
    """Convert technical exceptions to user-friendly error messages."""
    if isinstance(exception, RequestError):
        return "Unable to reach the AI service. Please try again later."
    elif isinstance(exception, AuthenticationError):
        return "Authentication issue with AI service. Please contact support."
    elif isinstance(exception, RateLimitError):
        return "The AI service is currently busy. Please try again in a few moments."
    else:
        return "An unexpected error occurred. Please try again later."
```
- Translates technical errors into user-friendly messages
- Categorizes common error types
- Prevents exposing internal details to users

### Async Utilities (`utils/async_helpers.py`)

#### Timeout Wrapper
```python
async def with_timeout(coroutine, timeout_seconds, timeout_message="Operation timed out"):
    """Execute a coroutine with a timeout."""
    try:
        return await asyncio.wait_for(coroutine, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        logging.warning(f"Timeout after {timeout_seconds}s: {timeout_message}")
        raise TimeoutError(timeout_message)
```
- Adds timeout capability to async operations
- Prevents indefinite waiting for external services
- Provides clear error messages for timeouts

#### Parallel Processing
```python
async def parallel_process(items, process_func, max_concurrency=5):
    """Process items in parallel with controlled concurrency."""
    semaphore = asyncio.Semaphore(max_concurrency)
    
    async def process_with_semaphore(item):
        async with semaphore:
            return await process_func(item)
    
    return await asyncio.gather(*[process_with_semaphore(item) for item in items])
```
- Facilitates concurrent processing of multiple items
- Controls concurrency with semaphores
- Optimizes performance while preventing overload

## LangSmith Integration (`utils/tracing.py`)

#### Tracing Decorator
```python
def traceable(name=None):
    """Decorator to trace function execution with LangSmith."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            with trace(name=name or func.__name__) as span:
                # Add function arguments to span
                span.attributes.update({
                    f"arg_{i}": str(arg) for i, arg in enumerate(args)
                })
                span.attributes.update({
                    f"kwarg_{k}": str(v) for k, v in kwargs.items()
                })
                
                try:
                    result = await func(*args, **kwargs)
                    # Record successful result
                    span.attributes["result"] = str(result)[:200]  # Truncate long results
                    return result
                except Exception as e:
                    # Record exception
                    span.attributes["error"] = str(e)
                    span.attributes["error_type"] = e.__class__.__name__
                    raise
        return wrapper
    return decorator
```
- Provides observability for function execution
- Records function arguments and results
- Tracks errors for debugging
- Integrates with LangSmith for visualization

## Recent Enhancements
- Added HTML sanitization for security
- Improved Hebrew text processing
- Enhanced error handling with user-friendly messages
- Added async utilities for better performance
- Implemented tracing for improved observability
- Added validation utilities for input checking 