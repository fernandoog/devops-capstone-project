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
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'object-src': "'none'"
    },
    referrer_policy='strict-origin-when-cross-origin',
    frame_options='SAMEORIGIN',
    content_type_nosniff=True
)

# Initialize CORS for cross-origin resource sharing
CORS(app, 
     origins='*',
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
