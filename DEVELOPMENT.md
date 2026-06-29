# Development Guide

## Project Structure

```
├── src/
│   ├── core/                 # Core AI logic
│   │   ├── analyzer.py       # Data analysis engine
│   │   ├── recommender.py    # Recommendation engine
│   │   └── framework_scorer.py  # Feature prioritization
│   ├── modules/              # Feature modules
│   │   ├── market_analysis.py   # Market research
│   │   ├── user_research.py     # User feedback analysis
│   │   ├── analytics.py         # Metrics interpretation
│   │   ├── roadmap.py           # Roadmap generation
│   │   └── strategy.py          # Strategy development
│   ├── utils/                # Utilities
│   │   ├── llm_client.py     # LLM integration
│   │   ├── data_processor.py # Data processing
│   │   └── formatters.py     # Output formatting
│   └── api/
│       └── routes.py         # FastAPI endpoints
├── config/
│   └── settings.py          # Configuration
├── tests/                    # Unit tests
├── frontend/                 # Web GUI
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── main.py                   # Entry point
└── requirements.txt          # Dependencies
```

## Adding New Features

### 1. Create a New Module

```python
# src/modules/my_feature.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings

class MyFeature:
    def __init__(self, model=None):
        self.model_name = model or settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=self.model_name,
            temperature=0.7,
        )

    def analyze(self, data):
        prompt = PromptTemplate(
            input_variables=["data"],
            template="Analyze: {data}"
        )
        chain = prompt | self.llm
        return chain.invoke({"data": data})
```

### 2. Add API Endpoint

```python
# In src/api/routes.py
class MyFeatureRequest(BaseModel):
    data: Dict[str, Any]

@app.post("/my-feature")
async def my_feature(request: MyFeatureRequest):
    try:
        feature = MyFeature()
        result = feature.analyze(request.data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. Add Frontend Form

```html
<!-- In frontend/index.html -->
<section id="my-feature" class="tab-content">
    <div class="form-container">
        <h3>My Feature</h3>
        <form onsubmit="myFeature(event)">
            <div class="form-group">
                <label>Input:</label>
                <input type="text" id="my-input" required>
            </div>
            <button type="submit" class="btn btn-primary">Analyze</button>
        </form>
        <div id="my-results" class="results-container"></div>
    </div>
</section>
```

### 4. Add Frontend Handler

```javascript
// In frontend/app.js
async function myFeature(event) {
    event.preventDefault();
    const data = document.getElementById('my-input').value;
    try {
        const result = await fetchAPI('/my-feature', { data });
        showResults('my-results', result.data);
    } catch (error) {
        showError('my-results', error.message);
    }
}
```

## Testing

### Unit Tests

```python
# tests/test_my_feature.py
import pytest
from src.modules.my_feature import MyFeature

@pytest.fixture
def feature():
    return MyFeature()

def test_feature(feature):
    result = feature.analyze("test data")
    assert result is not None
```

Run tests:
```bash
pytest tests/ -v
```

### API Tests

```bash
curl -X POST http://localhost:8000/my-feature \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

## Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small
- Use descriptive variable names

```python
def analyze_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze data and return insights.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Dictionary containing analysis results
    """
    # Implementation
    pass
```

## Debugging

### Enable Debug Mode

```bash
API_DEBUG=True python main.py
```

### View API Documentation

Visit `http://localhost:8000/docs` to see interactive API docs.

### Check Logs

```bash
# View live logs
tail -f app.log

# Or use Docker logs
docker-compose logs -f api
```

## Performance Optimization

1. **Caching**: Implement caching for repeated requests
2. **Async**: Use async/await for I/O operations
3. **Batching**: Process multiple requests together
4. **Pagination**: Return large results in pages

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -am 'Add my feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Submit a pull request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Pydantic Documentation](https://docs.pydantic.dev/)
