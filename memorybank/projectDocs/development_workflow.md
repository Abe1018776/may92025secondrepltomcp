# Development Workflow Guide

## Overview
This document outlines the development workflow and patterns for the Divrei Yoel AI Chat application. It provides guidelines for code organization, contributions, testing, and deployment to ensure consistent and high-quality development.

## Branch Strategy

### Main Branch
- The `main` branch contains the stable, production-ready code
- Always deployable and passing all tests
- Protected from direct pushes

### Feature Branches
- Create feature branches from `main` for all changes
- Use descriptive names with prefix: `feature/`, `bugfix/`, `refactor/`, `docs/`
- Example: `feature/add-font-selection` or `bugfix/fix-rtl-alignment`

### Development Process
1. Create a feature branch from `main`
2. Implement changes with regular commits
3. Write or update tests for new functionality
4. Update documentation
5. Create a pull request to `main`
6. Address review feedback
7. Merge when approved and tests pass

## Code Organization

### Package Structure
```
├── app.py                  # Main application entry point
├── rag_processor.py        # Core RAG pipeline implementation
├── config.py               # Configuration and environment variables
├── i18n.py                 # Internationalization support
├── components/             # UI components
│   ├── __init__.py
│   ├── chat.py             # Chat message handling
│   ├── sidebar.py          # Sidebar configuration
│   └── prompt_gallery.py   # Example prompts display
├── css/                    # CSS styling
│   ├── __init__.py
│   └── styles.py           # Dynamic CSS generation
├── services/               # External service integrations
│   ├── __init__.py
│   └── api.py              # API client implementations
├── prompts/                # Prompt templates
│   ├── __init__.py
│   └── templates.py        # System and user prompts
└── utils/                  # Utility functions
    ├── __init__.py
    ├── logging.py          # Logging configuration
    ├── text.py             # Text processing utilities
    ├── validation.py       # Input validation
    ├── errors.py           # Error handling
    ├── async_helpers.py    # Async utilities
    └── tracing.py          # Observability integration
```

### Naming Conventions
- **Files**: Lowercase with underscores (snake_case)
- **Classes**: CapitalizedWords (PascalCase)
- **Functions/Methods**: lowercase_with_underscores (snake_case)
- **Constants**: UPPERCASE_WITH_UNDERSCORES

## Development Patterns

### Component Pattern
UI components follow a consistent pattern:
```python
def display_component(params):
    """
    Display a UI component with the given parameters.
    
    Args:
        params: Component parameters
        
    Returns:
        Any data that needs to be passed back to the parent
    """
    # Component implementation
    return result
```

### Service Pattern
External services are wrapped in client classes:
```python
class ServiceClient:
    """Client for interacting with external service."""
    
    def __init__(self, config):
        """Initialize the client with configuration."""
        self.config = config
        # Setup client
        
    async def operation(self, params):
        """
        Perform an operation on the service.
        
        Args:
            params: Operation parameters
            
        Returns:
            Operation result
            
        Raises:
            ServiceError: If the operation fails
        """
        # Implementation
```

### Error Handling Pattern
```python
try:
    # Operation that might fail
    result = await service.operation(params)
except ServiceError as e:
    # Log the technical details
    logging.error(f"Service operation failed: {e}")
    # Return user-friendly message
    return False, utils.get_user_friendly_error(e)
```

### Async Pattern
```python
@traceable(name="operation-name")
async def operation(params):
    """Perform an asynchronous operation."""
    # Break down into sub-tasks
    subtask_results = await asyncio.gather(
        subtask1(params),
        subtask2(params),
        return_exceptions=True
    )
    
    # Process results, handling any exceptions
    processed_results = []
    for result in subtask_results:
        if isinstance(result, Exception):
            logging.error(f"Subtask failed: {result}")
            continue
        processed_results.append(result)
    
    return processed_results
```

## Testing Strategy

### Test Types
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete user flows

### Test Structure
```python
def test_function_name_scenario_being_tested():
    # Arrange
    input_data = prepare_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_result
```

### Mocking External Services
```python
@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock the OpenAI client for testing."""
    class MockOpenAI:
        def __init__(self, *args, **kwargs):
            pass
            
        async def chat_completions_create(self, *args, **kwargs):
            # Return mock response
            return MockResponse()
    
    monkeypatch.setattr("openai.AsyncOpenAI", MockOpenAI)
```

## Configuration Management

### Environment Variables
- Store configuration in environment variables or `.env` file
- Never commit sensitive values to the repository
- Provide example configuration in `.env.example`

### Configuration Validation
- Validate configuration at startup
- Provide clear error messages for missing or invalid configuration
- Exit gracefully if required configuration is missing

## Documentation Standards

### Code Documentation
- Document all public functions, classes, and modules
- Use docstrings with parameter and return descriptions
- Include examples for complex functions

### Project Documentation
- Keep `README.md` up to date with setup and usage instructions
- Update technical documentation when changing functionality
- Document architectural decisions

## Deployment Process

### Prerequisites
- All tests passing
- Documentation updated
- Code reviewed and approved

### Deployment Steps
1. Merge feature branch to `main`
2. Tag the release with semantic versioning
3. Build deployment artifacts
4. Deploy to staging environment
5. Validate deployment
6. Deploy to production
7. Monitor for issues

## Continuous Integration
- Run tests on all pull requests
- Check code formatting and linting
- Generate test coverage reports
- Block merges if tests fail

## Best Practices

### Performance
- Use asynchronous operations for external services
- Implement proper caching
- Monitor and optimize slow operations
- Use streaming responses for better user experience

### Security
- Sanitize user input
- Validate API responses
- Use proper authentication
- Avoid exposing sensitive information

### Internationalization
- Use the i18n module for all user-facing strings
- Support RTL and LTR text directions
- Test with both Hebrew and English

### Accessibility
- Ensure proper contrast ratios
- Support keyboard navigation
- Add appropriate ARIA attributes
- Test with screen readers

## Troubleshooting

### Common Issues
- API key configuration problems
- Pinecone connection issues
- Streamlit session state errors
- RTL text display issues

### Debugging Tools
- Application logs
- LangSmith traces
- Streamlit debugging
- Browser developer tools

### Support Resources
- GitHub issues
- Development team contacts
- External service documentation 