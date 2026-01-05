from flask import Flask

# Main API blueprint (existing)
from backend.api.routes.routes import api_bp

# ✅ NEW: candidates blueprint
from backend.api.routes.candidates import candidates_bp


def create_app():
    app = Flask(__name__)

    # Register main API routes
    app.register_blueprint(api_bp, url_prefix="/api")

    # Register candidates read API
    app.register_blueprint(candidates_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
