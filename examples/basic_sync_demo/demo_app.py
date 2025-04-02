import sys
import os
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from datetime import datetime

# Use absolute imports
from mini_dropbox.auth.auth_controller import router as auth_router
from mini_dropbox.files.file_controller import router as file_router
from mini_dropbox.sync.sync_controller import router as sync_router
from mini_dropbox.sharing.share_controller import router as share_router
from mini_dropbox.config import load_config
from mini_dropbox.utils.logger import log_info, log_error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update the startup event to use lifespan context
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    log_info("Starting Dropbox-lite Demo")
    config = load_config()
    
    # Create required directories
    os.makedirs(config["STORAGE_PATH"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Log startup information
    log_info(f"Storage directory: {config['STORAGE_PATH']}")
    log_info(f"Server running on: {config['HOST']}:{config['PORT']}")
    
    yield
    
    # Shutdown
    log_info("Shutting down Dropbox-lite Demo")

def create_demo_app() -> FastAPI:
    """Creates and configures the demo FastAPI application."""
    try:
        # Load configuration
        config = load_config()
        
        # Create FastAPI app
        app = FastAPI(
            title="Dropbox-lite Demo",
            description="A demo application showcasing file upload, download, sharing, and syncing",
            version="1.0.0",
            lifespan=lifespan
        )
        
        # Configure CORS for frontend
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],  # Frontend URL
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register all routers
        app.include_router(auth_router)
        app.include_router(file_router)
        app.include_router(sync_router)
        app.include_router(share_router)
        
        # Add demo routes
        @app.get("/")
        async def demo_root():
            """Welcome endpoint with basic instructions."""
            return {
                "message": "Welcome to Dropbox-lite Demo",
                "endpoints": {
                    "auth": {
                        "signup": "POST /auth/signup",
                        "login": "POST /auth/login",
                        "logout": "POST /auth/logout"
                    },
                    "files": {
                        "upload": "POST /files/upload",
                        "download": "GET /files/download/{file_id}",
                        "list": "GET /files/list"
                    },
                    "sharing": {
                        "create_link": "POST /share/{file_id}",
                        "access_shared": "GET /share/access/{token}",
                        "list_shares": "GET /share/list"
                    },
                    "sync": {
                        "init_sync": "POST /sync/init",
                        "resolve_conflict": "POST /sync/resolve"
                    }
                }
            }
        
        return app
        
    except Exception as e:
        log_error(f"Failed to create demo application: {str(e)}")
        raise

def run_demo():
    """Runs the demo application."""
    try:
        # Create the application instance
        app = create_demo_app()
        
        # Run with uvicorn
        if __name__ == "__main__":
            uvicorn.run(
                "demo_app:app",  # Use string reference to app
                host="localhost",
                port=8000,
                reload=True,
                log_level="info"
            )
        return app
            
    except Exception as e:
        log_error(f"Failed to run demo: {str(e)}")
        raise

# Create the app instance
app = run_demo()