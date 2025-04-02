from fastapi import FastAPI
import uvicorn
import logging
from config import load_config
from auth.auth_controller import router as auth_router
from files.file_controller import router as file_router
from sync.sync_controller import router as sync_router
from sharing.share_controller import router as share_router
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    try:
        # Load configuration
        config = load_config()
        
        # Create FastAPI app
        app = FastAPI(
            title="Dropbox-lite API",
            description="A lightweight file storage and sharing service",
            version="1.0.0"
        )
        
        # Register routers
        app.include_router(auth_router)
        app.include_router(file_router)
        app.include_router(sync_router)
        app.include_router(share_router)
        
        # Add startup event
        @app.on_event("startup")
        async def startup_event():
            logger.info("Starting Dropbox-lite service")
            # Initialize storage directory
            storage_path = config["STORAGE_PATH"]
            os.makedirs(storage_path, exist_ok=True)
        
        return app
        
    except Exception as e:
        logger.error("Failed to create application: %s", str(e))
        raise

def run_app():
    """Runs the FastAPI application."""
    try:
        config = load_config()
        app = create_app()
        
        uvicorn.run(
            app,
            host=config["HOST"],
            port=config["PORT"],
            log_level=config["LOG_LEVEL"].lower(),
            reload=config["DEBUG"]
        )
    except Exception as e:
        logger.error("Failed to run application: %s", str(e))
        raise

if __name__ == "__main__":
    run_app()