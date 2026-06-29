"""FastAPI routes for the AI Product Manager Copilot."""

import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config.settings import settings
from src.core.analyzer import DataAnalyzer
from src.core.recommender import RecommendationEngine
from src.core.framework_scorer import FeatureScorer
from src.modules.market_analysis import MarketAnalyzer
from src.modules.user_research import UserResearchAnalyzer
from src.modules.analytics import AnalyticsInterpreter
from src.modules.roadmap import RoadmapPlanner
from src.modules.strategy import StrategyDeveloper

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Product Manager Copilot",
    description="AI-powered assistant for product managers",
    version="1.0.0",
)

# Request/Response models
class TextInput(BaseModel):
    """Input for text analysis."""
    text: str

class MarketAnalysisRequest(BaseModel):
    """Request for market analysis."""
    market: str
    competitors: Optional[List[str]] = None
    focus_areas: Optional[List[str]] = None

class CompetitorAnalysisRequest(BaseModel):
    """Request for competitor analysis."""
    competitors: List[str]
    focus_areas: Optional[List[str]] = None

class FeaturePrioritizationRequest(BaseModel):
    """Request for feature prioritization."""
    features: List[Dict[str, Any]]
    framework: str = "RICE"
    weights: Optional[Dict[str, float]] = None

class RoadmapGenerationRequest(BaseModel):
    """Request for roadmap generation."""
    product_vision: str
    goals: List[str]
    features: List[Dict[str, Any]]
    timeline_quarters: int = 4

class InterviewAnalysisRequest(BaseModel):
    """Request for interview analysis."""
    transcripts: List[str]

class MetricsAnalysisRequest(BaseModel):
    """Request for metrics analysis."""
    metrics: Dict[str, Any]

class StrategyRequest(BaseModel):
    """Request for strategy development."""
    context: Dict[str, Any]
    objectives: List[str]


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "llm_provider": settings.LLM_PROVIDER,
    }


# Analysis endpoints
@app.post("/analyze/market")
async def analyze_market(request: MarketAnalysisRequest):
    """Analyze market trends and opportunities."""
    try:
        analyzer = MarketAnalyzer()
        result = analyzer.analyze_market(
            market=request.market,
            competitors=request.competitors,
            focus_areas=request.focus_areas,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Market analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/competitors")
async def analyze_competitors(request: CompetitorAnalysisRequest):
    """Analyze competitive landscape."""
    try:
        analyzer = MarketAnalyzer()
        result = analyzer.analyze_competitors(
            competitors=request.competitors,
            focus_areas=request.focus_areas,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Competitor analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/interviews")
async def analyze_interviews(request: InterviewAnalysisRequest):
    """Analyze user interview transcripts."""
    try:
        analyzer = UserResearchAnalyzer()
        result = analyzer.analyze_interviews(request.transcripts)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Interview analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/synthesize/user-research")
async def synthesize_research(request: Dict[str, Any]):
    """Synthesize user research data."""
    try:
        analyzer = UserResearchAnalyzer()
        result = analyzer.synthesize_research(request)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Research synthesis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/metrics")
async def analyze_metrics(request: MetricsAnalysisRequest):
    """Interpret product metrics."""
    try:
        interpreter = AnalyticsInterpreter()
        result = interpreter.interpret_metrics(request.metrics)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Metrics analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Generation endpoints
@app.post("/generate/roadmap")
async def generate_roadmap(request: RoadmapGenerationRequest):
    """Generate product roadmap."""
    try:
        planner = RoadmapPlanner()
        result = planner.generate_roadmap(
            product_vision=request.product_vision,
            goals=request.goals,
            features=request.features,
            timeline_quarters=request.timeline_quarters,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Roadmap generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/score/features")
async def score_features(request: FeaturePrioritizationRequest):
    """Score and prioritize features."""
    try:
        scorer = FeatureScorer()
        result = scorer.score_by_framework(
            features=request.features,
            framework=request.framework,
            weights=request.weights,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Feature scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/strategy")
async def generate_strategy(request: StrategyRequest):
    """Generate product strategy."""
    try:
        developer = StrategyDeveloper()
        result = developer.develop_strategy(
            context=request.context,
            objectives=request.objectives,
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Strategy generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/gtm")
async def generate_gtm(request: Dict[str, Any]):
    """Generate go-to-market strategy."""
    try:
        developer = StrategyDeveloper()
        result = developer.gtm_planning(
            product_info=request.get("product_info", {}),
            market_info=request.get("market_info", {}),
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"GTM generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Recommendation endpoints
@app.post("/recommend/features")
async def recommend_features(request: Dict[str, Any]):
    """Recommend features."""
    try:
        engine = RecommendationEngine()
        result = engine.recommend_features(
            context=request.get("context", {}),
            constraints=request.get("constraints", {}),
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Feature recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommend/positioning")
async def recommend_positioning(request: Dict[str, Any]):
    """Recommend product positioning."""
    try:
        engine = RecommendationEngine()
        result = engine.recommend_positioning(
            market_analysis=request.get("market_analysis", {}),
            competitive_analysis=request.get("competitive_analysis", {}),
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Positioning recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
