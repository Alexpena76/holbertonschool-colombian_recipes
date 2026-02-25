"""
Health Check Route
"""
from flask import Blueprint
from datetime import datetime
from app.services.response_service import success_response

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return success_response(
        data={
            'status': 'healthy',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }
    )
