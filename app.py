from typing import Optional
from flask import Flask, jsonify


def create_app() -> Flask:
    """
    Configures and returns the Flask application.

    Returns:
        Flask: A configured Flask application instance.

    Raises:
        RuntimeError: If the application fails to initialize.
    """
    try:
        app = Flask(__name__)
        # TODO: Add any additional configuration or initialization here

        @app.route("/health", methods=["GET"])
        def health_check() -> str:
            """
            Health check endpoint to ensure the server is running.

            Returns:
                str: A simple JSON response indicating health status.
            """
            return jsonify({"status": "OK"})

        return app
    except Exception as e:
        # Handle errors in application creation
        raise RuntimeError(f"Failed to create Flask application: {e}")


def run_app(port: int = 5000) -> None:
    """
    Starts the server on the specified port.

    Args:
        port: The port number on which to run the Flask server.

    Raises:
        RuntimeError: If the server fails to start.
    """
    app = create_app()
    try:
        # TODO: Optionally configure advanced servers like Gunicorn or Twisted
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        # Handle errors during server startup
        raise RuntimeError(f"Failed to start Flask server: {e}")