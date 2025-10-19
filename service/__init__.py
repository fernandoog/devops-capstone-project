"""
Account Service with Security Headers and CORS
"""
from flask_talisman import Talisman
from flask_cors import CORS
from service.routes import create_app

# Create the Flask app
app = create_app()

# Initialize Talisman for security headers
talisman = Talisman(
    app,
    force_https=False,  # Allow HTTP for testing
    frame_options='SAMEORIGIN'
)

# Initialize CORS for cross-origin resource sharing
CORS(app, origins='*')
