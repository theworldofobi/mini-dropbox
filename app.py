from fastapi import FastAPI
import uvicorn
import logging
from config import load_config
from auth.auth_controller import router as auth_router
from files.file_controller import router as file_router
from sync.sync_controller import router as sync_router
from sharing.share_controller import router as share_router
import os
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add this lifespan context manager
@asynccontextmanager
async def lifespan(app):
    logger.info("Starting Dropbox-lite service")
    # Initialize storage directory
    config = load_config()
    storage_path = config["STORAGE_PATH"]
    os.makedirs(storage_path, exist_ok=True)
    yield
    # Shutdown logic (if any)

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    try:
        # Load configuration
        config = load_config()
        
        # Create FastAPI app
        app = FastAPI(
            title="Dropbox-lite API",
            description="A lightweight file storage and sharing service",
            version="1.0.0",
            lifespan=lifespan
        )
        
        # Register routers
        app.include_router(auth_router)
        app.include_router(file_router)
        app.include_router(sync_router)
        app.include_router(share_router)
        
        return app
        
    except Exception as e:
        logger.error("Failed to create application: %s", str(e))
        raise

def run_app(host=None, port=None, log_level=None, reload=None):
    """Runs the FastAPI application."""
    try:
        config = load_config()
        app = create_app()
        
        uvicorn.run(
            app,
            host=host or config["HOST"],
            port=port or config["PORT"],
            log_level=log_level or config["LOG_LEVEL"].lower(),
            reload=reload if reload is not None else config["DEBUG"]
        )
    except Exception as e:
        logger.error("Failed to run application: %s", str(e))
        raise

if __name__ == "__main__":
    run_app()