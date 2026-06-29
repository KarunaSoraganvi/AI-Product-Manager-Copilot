"""FastAPI routes for the copilot."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from src.modules.market_analysis import MarketAnalyzer
from src.modules.roadmap import RoadmapPlanner
from src.modules.user_research import UserResearchAnalyzer
from src.modules.strategy import StrategyDeveloper
from src.modules.analytics import AnalyticsInterpreter
from src.core.framework_scorer import FeatureScorer

# Initialize app
app = FastAPI(
    title="AI Product Manager Copilot",
    description="AI-powered assistant for product managers",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
market_analyzer = MarketAnalyzer()
roadmap_planner = RoadmapPlanner()
research_analyzer = UserResearchAnalyzer()
strategy_developer = StrategyDeveloper()
analytics_interpreter = AnalyticsInterpreter()
feature_scorer = FeatureScorer()


# Request models
class MarketAnalysisRequest(BaseModel):
    market: str
    competitors: Optional[List[str]] = None
    trends: Optional[List[str]] = None
    focus_areas: Optional[List[str]] = None


class RoadmapRequest(BaseModel):
    product_vision: str
    goals: List[str]
    features: List[Dict[str, Any]]
    timeline_quarters: int = 4
    constraints: Optional[Dict[str, Any]] = None


class FeatureRequest(BaseModel):
    features: List[Dict[str, Any]]
    framework: str = "RICE"


class InterviewRequest(BaseModel):
    interviews: List[Dict[str, str]]


class FeedbackRequest(BaseModel):
    feedback_items: List[str]


class StrategyRequest(BaseModel):
    company_vision: str
    market_opportunity: str
    competitive_landscape: str
    internal_capabilities: List[str]


# Market Analysis Endpoints
@app.post("/api/analyze/market")
async def analyze_market(request: MarketAnalysisRequest):
    """Analyze market opportunity and trends."""
    try:
        result = market_analyzer.analyze_market(
            market=request.market,
            competitors=request.competitors,
            trends=request.trends,
            focus_areas=request.focus_areas,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/competitors")
async def analyze_competitors(competitors: List[Dict[str, Any]]):
    """Analyze competitive landscape."""
    try:
        result = market_analyzer.analyze_competitors(competitors=competitors)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/market-gaps")
async def identify_gaps(market: str, existing_solutions: Optional[List[str]] = None):
    """Identify market gaps and opportunities."""
    try:
        result = market_analyzer.identify_market_gaps(
            market=market, existing_solutions=existing_solutions
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Roadmap Endpoints
@app.post("/api/generate/roadmap")
async def generate_roadmap(request: RoadmapRequest):
    """Generate product roadmap."""
    try:
        result = roadmap_planner.generate_roadmap(
            product_vision=request.product_vision,
            goals=request.goals,
            features=request.features,
            timeline_quarters=request.timeline_quarters,
            constraints=request.constraints,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# User Research Endpoints
@app.post("/api/synthesize/interviews")
async def synthesize_interviews(request: InterviewRequest):
    """Synthesize user interview data."""
    try:
        result = research_analyzer.synthesize_interviews(
            interviews=request.interviews
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/feedback")
async def analyze_feedback(request: FeedbackRequest):
    """Analyze user feedback."""
    try:
        result = research_analyzer.analyze_feedback(
            feedback_items=request.feedback_items
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Feature Prioritization Endpoints
@app.post("/api/score/features")
async def score_features(request: FeatureRequest):
    """Score and rank features using prioritization framework."""
    try:
        result = feature_scorer.score_by_framework(
            features=request.features, framework=request.framework
        )
        return {
            "framework": request.framework,
            "scored_features": result,
            "count": len(result),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Strategy Endpoints
@app.post("/api/generate/strategy")
async def generate_strategy(request: StrategyRequest):
    """Generate product strategy."""
    try:
        result = strategy_developer.develop_product_strategy(
            company_vision=request.company_vision,
            market_opportunity=request.market_opportunity,
            competitive_landscape=request.competitive_landscape,
            internal_capabilities=request.internal_capabilities,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analytics Endpoints
@app.post("/api/interpret/metrics")
async def interpret_metrics(metrics: Dict[str, Any]):
    """Interpret product metrics."""
    try:
        result = analytics_interpreter.interpret_metrics(metrics=metrics)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Product Manager Copilot",
        "version": "0.1.0",
        "description": "AI-powered assistant for product managers",
        "docs": "/docs",
        "endpoints": {
            "market_analysis": "/api/analyze/market",
            "competitive_analysis": "/api/analyze/competitors",
            "market_gaps": "/api/analyze/market-gaps",
            "roadmap": "/api/generate/roadmap",
            "interview_synthesis": "/api/synthesize/interviews",
            "feedback_analysis": "/api/analyze/feedback",
            "feature_scoring": "/api/score/features",
            "strategy": "/api/generate/strategy",
            "metrics": "/api/interpret/metrics",
        },
    }
