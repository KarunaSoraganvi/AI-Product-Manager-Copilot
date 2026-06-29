"""Main entry point for the AI Product Manager Copilot."""

import logging
import uvicorn
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Start the API server."""
    logger.info("Starting AI Product Manager Copilot...")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    logger.info(f"Server: {settings.API_HOST}:{settings.API_PORT}")

    uvicorn.run(
        "src.api.routes:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG,
    )


if __name__ == "__main__":
    main()
