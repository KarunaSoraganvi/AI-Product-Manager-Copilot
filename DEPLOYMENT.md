# Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- OpenAI API key or Anthropic API key

## Local Development

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

### 3. Run API Server

```bash
python main.py
```

API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 4. Run Frontend (in another terminal)

```bash
# Install Node.js dependencies (optional - can run static)
cd frontend
python -m http.server 3000
```

Frontend will be available at `http://localhost:3000`

## Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Create .env file with API keys
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Build and start services
docker-compose up --build
```

Services will be available at:
- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### 2. Docker Build Only

```bash
docker build -t pm-copilot:latest .

docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  pm-copilot:latest
```

## Cloud Deployment

### AWS Deployment

1. **Push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t pm-copilot:latest .
   docker tag pm-copilot:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pm-copilot:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pm-copilot:latest
   ```

2. **Deploy to ECS:**
   - Create ECS cluster
   - Create task definition pointing to ECR image
   - Create service from task definition

### Heroku Deployment

```bash
heroku create pm-copilot
git push heroku main
```

### Google Cloud Run

```bash
gcloud run deploy pm-copilot \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=your_key
```

## Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Market analysis
curl -X POST http://localhost:8000/analyze/market \
  -H "Content-Type: application/json" \
  -d '{
    "market": "SaaS Project Management",
    "competitors": ["Asana", "Monday.com"],
    "focus_areas": ["trends", "opportunities"]
  }'
```

## Troubleshooting

### API Not Starting
- Check if port 8000 is available
- Verify Python version (3.11+)
- Check .env file for API keys

### Frontend Not Loading
- Check if API is running
- Check CORS configuration
- Verify frontend files are in `frontend/` directory

### API Key Errors
- Verify API key in .env file
- Check API key validity
- Ensure API provider is set correctly

## Performance Optimization

1. Enable caching for frequently used endpoints
2. Use pagination for large result sets
3. Implement rate limiting
4. Monitor API response times
5. Consider async processing for heavy computations

## Security Considerations

1. Never commit .env files
2. Use environment variables for secrets
3. Enable HTTPS in production
4. Implement API authentication
5. Add rate limiting
6. Validate all inputs
7. Use security headers

## Monitoring

- Monitor API response times
- Track error rates
- Monitor token usage (for LLM APIs)
- Set up alerts for failures
- Collect metrics and logs
