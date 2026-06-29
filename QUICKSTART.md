# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/KarunaSoraganvi/AI-Product-Manager-Copilot.git
cd AI-Product-Manager-Copilot

# 2. Create .env file with your API key
echo "OPENAI_API_KEY=sk-..." > .env

# 3. Start the application
docker-compose up --build

# 4. Open in browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/KarunaSoraganvi/AI-Product-Manager-Copilot.git
cd AI-Product-Manager-Copilot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# 5. Start API server (Terminal 1)
python main.py

# 6. Start frontend (Terminal 2)
cd frontend
python -m http.server 3000

# 7. Open in browser
# Frontend: http://localhost:3000
# API: http://localhost:8000
```

## 📋 Features Overview

### 1. **Market Analysis** 📊
Analyze market trends, competitive landscape, and identify opportunities.

**Example:**
```json
{
  "market": "SaaS Project Management",
  "competitors": ["Asana", "Monday.com", "Jira"],
  "focus_areas": ["trends", "opportunities", "threats"]
}
```

### 2. **User Research** 👥
Analyze interviews, surveys, and synthesize user insights.

**Example:**
```json
{
  "transcripts": [
    "Interview 1 transcript...",
    "Interview 2 transcript..."
  ]
}
```

### 3. **Feature Prioritization** 🎯
Score features using RICE, MoSCoW, or Value vs Effort frameworks.

**Example:**
```json
{
  "features": [
    {"name": "AI Analytics", "reach": 5000, "impact": 3, "confidence": 0.8, "effort": 13},
    {"name": "Custom Reports", "reach": 3000, "impact": 2, "confidence": 0.9, "effort": 5}
  ],
  "framework": "RICE"
}
```

### 4. **Roadmap Planning** 🗺️
Generate strategic product roadmaps aligned with business goals.

**Example:**
```json
{
  "product_vision": "Become the leading AI-powered project management platform",
  "goals": ["Increase user retention", "Expand to enterprise", "Build AI features"],
  "features": [{"name": "Feature 1"}, {"name": "Feature 2"}],
  "timeline_quarters": 4
}
```

### 5. **Analytics** 📈
Interpret metrics and KPIs to drive product decisions.

**Example:**
```json
{
  "dau": 5000,
  "mau": 15000,
  "retention_day_7": 0.45,
  "retention_day_30": 0.25,
  "churn_rate": 0.05
}
```

### 6. **Strategy Development** 🎨
Develop comprehensive product and go-to-market strategies.

**Example:**
```json
{
  "context": {
    "market": "SaaS",
    "team_size": 10,
    "funding": "seed"
  },
  "objectives": [
    "Achieve product-market fit",
    "Build brand awareness",
    "Expand team"
  ]
}
```

## 🔧 Configuration

### API Keys

1. **Get OpenAI API Key**
   - Go to https://platform.openai.com
   - Create account or sign in
   - Generate API key
   - Copy to .env file

2. **Get Anthropic API Key** (Optional)
   - Go to https://console.anthropic.com
   - Create account or sign in
   - Generate API key
   - Copy to .env file

### Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
ANTHROPIC_API_KEY=sk-ant-...

# Configuration
LLM_PROVIDER=openai              # openai or anthropic
DEFAULT_MODEL=gpt-4              # Model name
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True                   # False in production
LOG_LEVEL=INFO
```

## 🎯 Common Use Cases

### Use Case 1: Launch Analysis

1. **Market Analysis**: Understand the market and competitors
2. **User Research**: Validate assumptions with user interviews
3. **Feature Prioritization**: Decide what to build first
4. **Roadmap Planning**: Create launch timeline
5. **Strategy Development**: Plan go-to-market

### Use Case 2: Feature Prioritization

1. Collect feature requests and ideas
2. Use RICE or MoSCoW framework to score
3. Get recommendations based on impact
4. Align with strategic goals
5. Plan development roadmap

### Use Case 3: Market Expansion

1. Analyze new market opportunities
2. Research competitor offerings
3. Identify market gaps
4. Plan positioning strategy
5. Develop go-to-market plan

## 📚 API Examples

### Example 1: Market Analysis

```bash
curl -X POST http://localhost:8000/analyze/market \
  -H "Content-Type: application/json" \
  -d '{
    "market": "SaaS Analytics",
    "competitors": ["Mixpanel", "Amplitude", "Segment"],
    "focus_areas": ["trends", "opportunities", "market_size"]
  }'
```

### Example 2: Feature Prioritization

```bash
curl -X POST http://localhost:8000/score/features \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {"name": "Dark Mode", "reach": 10000, "impact": 2, "confidence": 0.9, "effort": 8},
      {"name": "API Access", "reach": 2000, "impact": 3, "confidence": 0.8, "effort": 21}
    ],
    "framework": "RICE"
  }'
```

### Example 3: Roadmap Generation

```bash
curl -X POST http://localhost:8000/generate/roadmap \
  -H "Content-Type: application/json" \
  -d '{
    "product_vision": "The AI-first analytics platform",
    "goals": ["Increase user retention", "Expand enterprise"],
    "features": [{"name": "AI Insights"}, {"name": "Custom Dashboards"}],
    "timeline_quarters": 4
  }'
```

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_analyzer.py -v

# With coverage
pytest tests/ --cov=src
```

### Manual Testing

1. Open http://localhost:3000
2. Navigate to a feature (e.g., Market Analysis)
3. Fill in the form
4. Click the action button
5. View results

## 🐛 Troubleshooting

### Issue: "API Key not found"

**Solution:**
```bash
# Check .env file exists
ls .env

# Check API key is set
echo $OPENAI_API_KEY

# If not set, add it:
echo "OPENAI_API_KEY=sk-..." > .env
```

### Issue: "Connection refused on port 8000"

**Solution:**
```bash
# Check if API is running
curl http://localhost:8000/health

# Start API if not running
python main.py
```

### Issue: "CORS error in browser"

**Solution:**
- The frontend should be on http://localhost:3000
- The API should be on http://localhost:8000
- Both must be running

### Issue: "JSON parsing error"

**Solution:**
- Ensure JSON is valid
- Use a JSON validator (e.g., https://jsonlint.com)
- Check for special characters that need escaping

## 📖 Next Steps

1. **Read Documentation**
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

2. **Explore Features**
   - Try each analysis type
   - Use different frameworks
   - Experiment with different inputs

3. **Customize**
   - Add your own prompts in `src/modules/`
   - Modify the UI in `frontend/`
   - Add new API endpoints

4. **Deploy**
   - Deploy to cloud (AWS, GCP, Azure)
   - Set up CI/CD pipeline
   - Monitor in production

## 💡 Tips & Tricks

### Tip 1: Use JSON Mode
- Most endpoints expect JSON input
- Use copy-paste examples to get started

### Tip 2: API Documentation
- Visit http://localhost:8000/docs for interactive docs
- Try out endpoints directly in the browser

### Tip 3: Stream Long Results
- For large analyses, results may take time
- UI shows "Loading..." status
- Results display when ready

### Tip 4: Experiment with Frameworks
- Try different prioritization frameworks
- Compare results
- Choose best fit for your use case

## 📞 Support

- **Issues**: https://github.com/KarunaSoraganvi/AI-Product-Manager-Copilot/issues
- **Discussions**: https://github.com/KarunaSoraganvi/AI-Product-Manager-Copilot/discussions
- **Documentation**: See README.md

## 🎉 You're Ready!

You now have a fully functional AI Product Manager Copilot. Start analyzing your market, user research, and features!
