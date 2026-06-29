# Testing Guide

Comprehensive guide for testing the AI Product Manager Copilot.

## 🧪 Testing Overview

The project includes multiple levels of testing:

1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test API endpoints
3. **Manual Testing** - Test via UI and curl
4. **Load Testing** - Test performance

---

## 1. Unit Tests

### Setup

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install test dependencies
pip install -r requirements.txt
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v

# Run specific test function
pytest tests/test_analyzer.py::test_analyzer_initialization -v
```

### Test Output Example

```
============================= test session starts ==============================
tests/test_analyzer.py::test_analyzer_initialization PASSED                [ 50%]
tests/test_market_analyzer.py::test_analyzer_initialization PASSED         [100%]

============================== 2 passed in 0.42s ===============================
```

### Existing Tests

```python
# tests/test_analyzer.py
- test_analyzer_initialization()  # Check analyzer starts correctly
- test_sentiment_analysis()        # Test sentiment analysis

# tests/test_market_analyzer.py
- test_analyzer_initialization()   # Check market analyzer starts correctly
```

### Adding New Tests

```python
# tests/test_my_feature.py
import pytest
from src.modules.market_analysis import MarketAnalyzer

@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    return MarketAnalyzer()

def test_market_analysis(analyzer):
    """Test market analysis functionality."""
    result = analyzer.analyze_market(
        market="SaaS",
        competitors=["Asana", "Monday.com"],
        focus_areas=["trends"]
    )
    
    # Assertions
    assert result is not None
    assert isinstance(result, dict)
    assert "analysis" in result or "market" in result
```

---

## 2. API Integration Tests

### Start API Server

```bash
# Terminal 1: Start API
python main.py

# Should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test Health Endpoint

```bash
# Test API is running
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0", "llm_provider": "openai"}
```

### View API Documentation

```bash
# Open in browser:
# http://localhost:8000/docs     # Swagger UI (interactive)
# http://localhost:8000/redoc    # ReDoc (alternative)
```

---

## 3. Manual Testing with cURL

### Prerequisites

```bash
# Make sure API is running
curl http://localhost:8000/health

# Set your API key
export OPENAI_API_KEY="sk-your-key-here"
```

### Test 1: Market Analysis

```bash
curl -X POST http://localhost:8000/analyze/market \
  -H "Content-Type: application/json" \
  -d '{
    "market": "SaaS Project Management",
    "competitors": ["Asana", "Monday.com", "Jira"],
    "focus_areas": ["trends", "opportunities"]
  }' | python -m json.tool
```

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "market_size": "...",
    "trends": [...],
    "opportunities": [...]
  }
}
```

### Test 2: Competitor Analysis

```bash
curl -X POST http://localhost:8000/analyze/competitors \
  -H "Content-Type: application/json" \
  -d '{
    "competitors": ["Asana", "Monday.com"],
    "focus_areas": ["features", "pricing"]
  }' | python -m json.tool
```

### Test 3: Feature Prioritization (RICE)

```bash
curl -X POST http://localhost:8000/score/features \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {"name": "Dark Mode", "reach": 10000, "impact": 2, "confidence": 0.9, "effort": 8},
      {"name": "API Access", "reach": 2000, "impact": 3, "confidence": 0.8, "effort": 21},
      {"name": "Webhooks", "reach": 1500, "impact": 3, "confidence": 0.7, "effort": 13}
    ],
    "framework": "RICE"
  }' | python -m json.tool
```

**Expected Response**:
```json
{
  "success": true,
  "data": [
    {"name": "API Access", "rice_score": 10.77, "rank": 1},
    {"name": "Dark Mode", "rice_score": 2500, "rank": 2},
    {"name": "Webhooks", "rice_score": 8.05, "rank": 3}
  ]
}
```

### Test 4: Feature Prioritization (MoSCoW)

```bash
curl -X POST http://localhost:8000/score/features \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {"name": "User Authentication"},
      {"name": "Dark Mode"},
      {"name": "Analytics"},
      {"name": "Easter Egg"}
    ],
    "framework": "MOSCOW"
  }' | python -m json.tool
```

### Test 5: Roadmap Generation

```bash
curl -X POST http://localhost:8000/generate/roadmap \
  -H "Content-Type: application/json" \
  -d '{
    "product_vision": "The AI-first project management platform",
    "goals": ["Increase retention to 60%", "Expand to enterprise", "Build AI features"],
    "features": [
      {"name": "AI Suggestions"},
      {"name": "Custom Workflows"},
      {"name": "API Access"},
      {"name": "Advanced Analytics"}
    ],
    "timeline_quarters": 4
  }' | python -m json.tool
```

### Test 6: Strategy Generation

```bash
curl -X POST http://localhost:8000/generate/strategy \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "market": "SaaS Project Management",
      "team_size": 8,
      "funding_stage": "Series A",
      "current_users": 5000
    },
    "objectives": [
      "Achieve product-market fit",
      "Build sustainable GTM motion",
      "Establish market leadership"
    ]
  }' | python -m json.tool
```

### Test 7: Interview Analysis

```bash
curl -X POST http://localhost:8000/analyze/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "transcripts": [
      "Customer: We struggle with managing team workflows.\nPM: What tools do you currently use?\nCustomer: Asana, but it\'s too complex.",
      "Customer: I need better reporting features.\nPM: What reports matter most?\nCustomer: Time tracking and project progress."
    ]
  }' | python -m json.tool
```

---

## 4. Web UI Testing

### Start Application

```bash
# Terminal 1: Start API
python main.py

# Terminal 2: Start Frontend
cd frontend
python -m http.server 3000
```

### Access Web Interface

```
http://localhost:3000
```

### Test Each Feature

#### 1. Dashboard Tab
- [ ] Page loads without errors
- [ ] All feature cards display
- [ ] Quick Start button works

#### 2. Market Analysis
- [ ] Form loads correctly
- [ ] Can enter market name
- [ ] Can add competitors
- [ ] Can specify focus areas
- [ ] Submit button works
- [ ] Results display in JSON format

#### 3. User Research
- [ ] Interview tab loads
- [ ] Survey tab accessible
- [ ] Synthesis tab accessible
- [ ] Can paste interview transcripts
- [ ] Results display correctly

#### 4. Roadmap Planning
- [ ] Form fields validate
- [ ] Can enter product vision
- [ ] Can add goals (multiple lines)
- [ ] Can add features as JSON
- [ ] Can adjust timeline quarters
- [ ] Submit generates roadmap

#### 5. Feature Prioritization
- [ ] Framework dropdown works
- [ ] Can switch between RICE/MoSCoW/Value-Effort
- [ ] JSON input validates
- [ ] Results show rankings

#### 6. Strategy Development
- [ ] Product Strategy tab works
- [ ] GTM tab accessible
- [ ] Can input context JSON
- [ ] Can add objectives
- [ ] Results generate strategy

#### 7. Analytics
- [ ] Form accepts metrics JSON
- [ ] Results display interpretation
- [ ] Error handling works

### Test Error Handling

```bash
# Test 1: Invalid JSON
# In browser, go to Features tab
# Enter invalid JSON: {invalid json}
# Submit and verify error message appears

# Test 2: Missing required fields
# Leave required field empty
# Submit and verify validation error

# Test 3: API not running
# Stop API server
# Try to submit form
# Verify error message displays
```

---

## 5. Docker Testing

### Test Docker Build

```bash
# Build Docker image
docker build -t pm-copilot:test .

# Expected output:
# Successfully tagged pm-copilot:test
```

### Test Docker Compose

```bash
# Start services
docker-compose up --build

# Wait for output:
# api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000

# In another terminal, test:
curl http://localhost:8000/health
curl http://localhost:3000

# Stop services
docker-compose down
```

### Test Container Logs

```bash
# View API logs
docker-compose logs api

# View frontend logs
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

---

## 6. Performance Testing

### Test API Response Time

```bash
# Using curl with timing
time curl -X POST http://localhost:8000/analyze/market \
  -H "Content-Type: application/json" \
  -d '{"market": "SaaS"}'

# Expected: < 5 seconds for most endpoints
```

### Test with Apache Bench

```bash
# Install ab (if not installed)
sudo apt-get install apache2-utils  # Linux
brew install httpd  # macOS

# Test endpoint with 10 requests
ab -n 10 -c 1 http://localhost:8000/health

# Test with concurrent requests
ab -n 100 -c 10 http://localhost:8000/health
```

---

## 7. Test Checklist

### Pre-Launch Testing

- [ ] **Unit Tests**
  - [ ] All tests pass: `pytest tests/ -v`
  - [ ] Coverage > 80%: `pytest tests/ --cov=src`
  - [ ] No warnings or errors

- [ ] **API Testing**
  - [ ] Health check works: `curl /health`
  - [ ] All 11+ endpoints tested
  - [ ] Error responses have correct status codes
  - [ ] Swagger UI loads: `/docs`

- [ ] **Web UI Testing**
  - [ ] All 7 tabs load correctly
  - [ ] All forms validate input
  - [ ] All API calls work through UI
  - [ ] Error messages display properly
  - [ ] Loading states show correctly

- [ ] **Docker Testing**
  - [ ] Docker image builds: `docker build -t app .`
  - [ ] Docker Compose starts: `docker-compose up`
  - [ ] Services communicate
  - [ ] Logs show no errors

- [ ] **Configuration Testing**
  - [ ] API key loads from .env
  - [ ] Settings parse correctly
  - [ ] Debug mode works
  - [ ] Different providers work (if configured)

- [ ] **Error Handling**
  - [ ] Invalid JSON returns 400
  - [ ] Missing API key returns 500
  - [ ] Network errors handled
  - [ ] Timeout handled gracefully

---

## 8. Test Data

### Sample Market Data

```json
{
  "market": "SaaS Analytics",
  "competitors": ["Mixpanel", "Amplitude", "Segment"],
  "focus_areas": ["AI features", "pricing", "market gaps"]
}
```

### Sample Feature Data

```json
{
  "features": [
    {"name": "Feature A", "reach": 10000, "impact": 3, "confidence": 0.9, "effort": 8},
    {"name": "Feature B", "reach": 5000, "impact": 2, "confidence": 0.7, "effort": 13},
    {"name": "Feature C", "reach": 2000, "impact": 3, "confidence": 0.8, "effort": 5}
  ]
}
```

### Sample Interview Data

```json
{
  "transcripts": [
    "PM: What are your biggest challenges?\nUser: Manual reporting takes too long.\nPM: How long? User: 4 hours per week.",
    "PM: Do you use dashboards?\nUser: Yes, but we need real-time updates.\nPM: Why real-time?\nUser: For quick decisions."
  ]
}
```

---

## 9. Troubleshooting Tests

### Test Fails with "API Key not found"

```bash
# Check .env file
ls -la .env

# Check API key is set
echo $OPENAI_API_KEY

# Set API key if missing
export OPENAI_API_KEY="sk-..."
```

### Test Fails with "Connection refused"

```bash
# Check if API is running
curl http://localhost:8000/health

# Start API if not running
python main.py
```

### Test Fails with "Invalid JSON"

```bash
# Validate JSON using jq
echo '{"test": "data"}' | jq .

# Or use online validator
# https://jsonlint.com
```

### Test Fails with "Module not found"

```bash
# Check virtual environment is active
which python

# Should show path to venv/bin/python

# If not, activate it
source venv/bin/activate
```

---

## 10. Continuous Testing

### Watch Tests (Auto-run on file change)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw tests/
```

### GitHub Actions (CI/CD)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

---

## Summary

### Quick Test Commands

```bash
# Unit tests
pytest tests/ -v

# API health check
curl http://localhost:8000/health

# Feature test
curl -X POST http://localhost:8000/score/features \
  -H "Content-Type: application/json" \
  -d '{"features": [{"name": "Test"}], "framework": "RICE"}'

# All tests with Docker
docker-compose up --build
curl http://localhost:3000
```

### Next Steps

1. Run unit tests: `pytest tests/ -v`
2. Start API: `python main.py`
3. Test API endpoints with cURL
4. Open web UI: http://localhost:3000
5. Test all features in web interface
6. Deploy with Docker: `docker-compose up`

For more help, see [DEVELOPMENT.md](DEVELOPMENT.md) or [QUICKSTART.md](QUICKSTART.md).
