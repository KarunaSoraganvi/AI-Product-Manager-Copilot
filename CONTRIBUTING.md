# Contributing Guide

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/AI-Product-Manager-Copilot.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Set up development environment: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

## Development Workflow

1. Make changes in your feature branch
2. Write tests for new features
3. Run tests: `pytest tests/ -v`
4. Ensure code quality: `flake8 src/` and `mypy src/`
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Submit a pull request

## Code Standards

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for all public functions
- Keep functions focused and under 50 lines
- Use descriptive variable names
- Comment complex logic

## Testing Requirements

- Write unit tests for new features
- Aim for >80% code coverage
- Test error cases
- Test with real API calls when possible

```python
def test_feature():
    # Arrange
    feature = MyFeature()
    
    # Act
    result = feature.process("input")
    
    # Assert
    assert result is not None
    assert "expected_key" in result
```

## Documentation

- Update README.md with new features
- Add docstrings to all functions
- Update API documentation
- Add examples in comments

## Performance Considerations

- Avoid N+1 queries
- Use pagination for large datasets
- Implement caching where appropriate
- Profile code for bottlenecks
- Use async/await for I/O operations

## Security

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all inputs
- Sanitize outputs
- Follow OWASP guidelines

## Release Process

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create release notes
4. Tag release: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`

## Getting Help

- Check existing issues and discussions
- Create a new issue with detailed description
- Join our community discussions
- Check documentation

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Report issues responsibly

Thank you for contributing!
