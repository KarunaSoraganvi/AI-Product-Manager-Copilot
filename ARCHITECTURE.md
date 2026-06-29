# Architecture Overview

## System Design

The AI Product Manager Copilot is built with a modular, scalable architecture that separates concerns and enables easy extension.

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface (Frontend)                 │
│              (HTML/CSS/JavaScript + Nginx)                  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────────┐
│                    FastAPI Server (Port 8000)               │
│  - Request routing and validation                           │
│  - CORS and middleware handling                             │
│  - API documentation (Swagger UI)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼──────┐  ┌────▼──────┐  ┌────▼──────┐
│   Core AI  │  │  Feature   │  │ Utilities │
│   Logic    │  │  Modules   │  │           │
│            │  │            │  │           │
│ - Analyzer │  │ - Market   │  │ - LLM     │
│ - Recomm.  │  │ - Research │  │ - Data    │
│ - Scorer   │  │ - Analytics│  │ - Format  │
└────┬──────┘  └────┬──────┘  └────┬──────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
     ┌───────────────▼───────────────┐
     │    LangChain Integration      │
     │  - Chat LLM Models            │
     │  - Prompt Management          │
     │  - Chain Processing           │
     └───────────────┬───────────────┘
                     │
     ┌───────────────▼───────────────┐
     │   LLM Providers               │
     │  - OpenAI (GPT-4)             │
     │  - Anthropic (Claude)         │
     │  - Local Models (optional)    │
     └───────────────────────────────┘
```

## Component Architecture

### 1. Frontend Layer

**Location**: `frontend/`

- **index.html**: Main application shell with tabbed interface
- **styles.css**: Responsive design with modern UI
- **app.js**: Client-side logic and API integration

**Features**:
- Tab-based navigation for different features
- Form inputs for various analysis types
- Real-time result display
- Error handling and loading states
- Responsive design for mobile and desktop

### 2. API Layer (FastAPI)

**Location**: `src/api/routes.py`

**Endpoints**:
```
GET    /health                    - Health check
POST   /analyze/market            - Market analysis
POST   /analyze/competitors       - Competitor analysis
POST   /analyze/interviews        - Interview analysis
POST   /synthesize/user-research  - Research synthesis
POST   /analyze/metrics           - Metrics interpretation
POST   /generate/roadmap          - Roadmap generation
POST   /score/features            - Feature prioritization
POST   /generate/strategy         - Strategy development
POST   /generate/gtm              - Go-to-market planning
POST   /recommend/features        - Feature recommendations
POST   /recommend/positioning     - Positioning recommendations
```

**Request/Response**:
- Pydantic models for input validation
- JSON responses with consistent structure
- Error handling with HTTP status codes

### 3. Core AI Logic Layer

**Location**: `src/core/`

#### DataAnalyzer
- Sentiment analysis of text
- Theme extraction from multiple sources
- Insight synthesis and summarization

#### RecommendationEngine
- Feature recommendation based on context
- Positioning strategy recommendation
- Priority ranking based on weights

#### FeatureScorer
- RICE framework scoring (Reach × Impact × Confidence / Effort)
- MoSCoW method categorization (Must, Should, Could, Won't)
- Value vs Effort matrix analysis
- Kano model implementation

### 4. Feature Modules Layer

**Location**: `src/modules/`

#### MarketAnalyzer
```python
- analyze_market()
- analyze_competitors()
- identify_market_gaps()
```

#### UserResearchAnalyzer
```python
- analyze_interviews()
- analyze_surveys()
- synthesize_research()
```

#### AnalyticsInterpreter
```python
- interpret_metrics()
- analyze_cohort()
- forecast_trends()
```

#### RoadmapPlanner
```python
- generate_roadmap()
- plan_release_schedule()
- scenario_planning()
```

#### StrategyDeveloper
```python
- develop_strategy()
- gtm_planning()
- stakeholder_alignment()
```

### 5. Utilities Layer

**Location**: `src/utils/`

#### LLMClient
- Unified interface for multiple LLM providers
- OpenAI and Anthropic support
- Configuration management

#### DataProcessor
- JSON parsing and validation
- Text cleaning and normalization
- Sentiment analysis utilities
- Data aggregation

#### OutputFormatter
- JSON formatting
- Markdown conversion
- Table formatting
- Report generation

### 6. Configuration Layer

**Location**: `config/settings.py`

```python
# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# LLM Configuration
LLM_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4"

# Feature Flags
ENABLE_WEB_SCRAPING = False
ENABLE_MARKET_INTELLIGENCE = True
```

## Data Flow

### Typical Analysis Flow

```
1. User Input (Frontend)
   ↓
2. API Request (FastAPI)
   ↓
3. Input Validation (Pydantic)
   ↓
4. Module Processing
   - Create module instance
   - Prepare LLM prompt
   ↓
5. LLM Integration (LangChain)
   - Create chain with prompt template
   - Invoke with parameters
   ↓
6. LLM API Call
   - OpenAI/Anthropic API
   - Stream or batch processing
   ↓
7. Response Processing
   - Parse JSON response
   - Extract insights
   ↓
8. Format Output
   - Convert to desired format
   - Add metadata
   ↓
9. API Response
   - Return JSON to frontend
   ↓
10. Display Results (Frontend)
    - Parse response
    - Render in UI
```

## Integration Points

### LangChain Integration

All LLM interactions use LangChain for:
- Prompt management and templates
- Chain composition
- Model abstraction
- Token management

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(api_key=key, model="gpt-4")
prompt = PromptTemplate(template="...")
chain = prompt | llm
response = chain.invoke({"input": "..."})
```

### API Documentation

- Interactive Swagger UI at `/docs`
- ReDoc at `/redoc`
- Automatic OpenAPI schema generation

## Deployment Architecture

### Docker Deployment

```
┌─────────────────────────────────────────┐
│         Docker Host                      │
│                                          │
│  ┌────────────────┐  ┌──────────────┐  │
│  │   API Service  │  │   Frontend   │  │
│  │   (Python)     │  │   (Nginx)    │  │
│  │   Port 8000    │  │   Port 3000  │  │
│  └────────────────┘  └──────────────┘  │
│         │                   │            │
│         └───────┬───────────┘            │
│                 │                         │
│            Docker Network                 │
│                                          │
└─────────────────────────────────────────┘
```

### Environment Variables

```
OPENAI_API_KEY          - OpenAI API key
ANTHROPIC_API_KEY       - Anthropic API key
LLM_PROVIDER            - LLM provider (openai/anthropic)
DEFAULT_MODEL           - Default model name
API_HOST                - API server host
API_PORT                - API server port
API_DEBUG               - Debug mode
LOG_LEVEL               - Logging level
ENABLE_WEB_SCRAPING     - Web scraping feature
```

## Security Architecture

### API Security

1. **Input Validation**
   - Pydantic model validation
   - Type checking
   - Size limits

2. **Error Handling**
   - Generic error messages
   - Logging without exposing secrets
   - HTTP status codes

3. **Configuration Security**
   - Environment variables for secrets
   - No hardcoded credentials
   - .env files excluded from git

### Frontend Security

1. **CORS Configuration**
   - Restrict API access
   - Origin validation

2. **Input Sanitization**
   - HTML escaping
   - JSON parsing
   - Size limits

## Scalability Considerations

### Horizontal Scaling

- Stateless API design
- Load balancer support
- Database-backed session management (future)

### Vertical Scaling

- Async request handling
- Efficient LLM model selection
- Caching strategies
- Resource pooling

### Performance Optimization

1. **Caching**
   - Cache LLM responses
   - Cache common analyses
   - Browser caching for static assets

2. **Async Processing**
   - Async API endpoints
   - Batch processing
   - Queue-based processing (future)

3. **Model Optimization**
   - Use appropriate model sizes
   - Prompt optimization
   - Context window management

## Monitoring and Observability

### Metrics to Track

- API response times
- Error rates
- LLM token usage
- User engagement metrics
- Feature usage distribution

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Analysis completed: {result}")
logger.error(f"Error: {error}", exc_info=True)
```

### Health Checks

- `GET /health` endpoint
- LLM provider connectivity
- Configuration validation

## Future Architecture Enhancements

1. **Caching Layer**
   - Redis for response caching
   - Analysis result caching

2. **Message Queue**
   - Celery for async tasks
   - Task prioritization

3. **Database**
   - Store analysis history
   - User preferences
   - Audit logs

4. **Real-time Updates**
   - WebSocket support
   - Live collaboration

5. **Advanced Analytics**
   - Usage tracking
   - Performance metrics
   - Cost analysis

## Testing Architecture

```
tests/
├── test_analyzer.py          - Core analyzer tests
├── test_market_analyzer.py   - Market analysis tests
├── test_*_module.py          - Module-specific tests
└── conftest.py               - Shared test configuration
```

## Dependencies

### Core
- FastAPI: Web framework
- Pydantic: Data validation
- LangChain: LLM integration
- OpenAI: LLM provider
- Anthropic: LLM provider

### Data Processing
- Pandas: Data manipulation
- NumPy: Numerical computing
- Scikit-learn: ML utilities
- NLTK: NLP tools
- spaCy: NLP processing

### Development
- pytest: Testing framework
- black: Code formatting
- flake8: Linting
- mypy: Type checking

## Conclusion

The architecture is designed to be:
- **Modular**: Easy to add new features
- **Scalable**: Support growth in users and data
- **Maintainable**: Clear separation of concerns
- **Extensible**: Support for new LLM providers and analysis types
- **Observable**: Comprehensive logging and monitoring
