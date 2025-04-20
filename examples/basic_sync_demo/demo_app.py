import sys
import os
from pathlib import Path

# Add root directory to Python path (if needed)
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from datetime import datetime
from contextlib import asynccontextmanager

# Routers from mini_dropbox.* still work the same
from mini_dropbox.auth.auth_controller import router as auth_router
from mini_dropbox.files.file_controller import router as file_router
from mini_dropbox.sync.sync_controller import router as sync_router
from mini_dropbox.sharing.share_controller import router as share_router

# Updated to use your new config file
from demo_config import load_demo_config

# If you have a custom logger in mini_dropbox.utils, keep using it
from mini_dropbox.utils.logger import log_info, log_error

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Console handler
        logging.StreamHandler(),
        # File handler
        logging.FileHandler('logs/dropbox_lite.log')
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    config = load_demo_config()

    # Startup
    log_info("Starting Dropbox-lite Demo")

    # Create required directories
    os.makedirs(config["STORAGE_PATH"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Log startup info
    log_info(f"Storage directory: {config['STORAGE_PATH']}")
    log_info(f"Server running on: {config['HOST']}:{config['PORT']}")

    yield

    # Shutdown
    log_info("Shutting down Dropbox-lite Demo")


def create_demo_app() -> FastAPI:
    """Creates and configures the FastAPI app."""
    try:
        config = load_demo_config()

        app = FastAPI(
            title="Dropbox-lite Demo",
            description="A demo showcasing file upload, download, sharing, and syncing",
            version="1.0.0",
            lifespan=lifespan
        )

        # Configure CORS (adjust the frontend URL if needed)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",  # Local development
                "https://basic-demo-app-frontend.onrender.com"  # Production frontend
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routers
        app.include_router(auth_router)
        app.include_router(file_router)
        app.include_router(share_router)
        app.include_router(sync_router)

        @app.get("/")
        async def demo_root():
            """Welcome endpoint with basic instructions."""
            return {
                "message": "Welcome to Dropbox-lite Demo",
                "notes": "Try /auth, /files, /share, /sync"
            }

        return app

    except Exception as e:
        log_error(f"Failed to create demo application: {str(e)}")
        raise


def run_demo():
    """Runs the app with uvicorn, binding to 0.0.0.0 and reading PORT."""
    try:
        app = create_demo_app()

        if __name__ == "__main__":  # Only if run via python demo_app.py
            config = load_demo_config()

            # Pull Render's PORT or fallback to what's in config["PORT"]
            port = int(os.environ.get("PORT", config["PORT"]))
            # Always bind 0.0.0.0 so external traffic can reach it
            host = os.environ.get("HOST", config["HOST"])

            uvicorn.run(
                "demo_app:app",
                host=host,
                port=port,
                reload=True,
                log_level="debug"  # Change from info to debug
            )

        return app

    except Exception as e:
        log_error(f"Failed to run demo: {str(e)}")
        raise


# Create the global FastAPI app
app = run_demo()
