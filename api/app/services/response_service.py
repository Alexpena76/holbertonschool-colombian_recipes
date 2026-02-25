"""
Response Service - Consistent API response formatting
"""
from flask import jsonify


def success_response(data=None, message=None, status_code=200, pagination=None):
    """Create a successful API response."""
    response = {
        'success': True,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    if pagination:
        response['pagination'] = pagination
    
    return jsonify(response), status_code


def error_response(code, message, status_code=400):
    """Create an error API response."""
    response = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    
    return jsonify(response), status_code


def paginate(query, page=1, per_page=20, max_per_page=50):
    """Paginate a SQLAlchemy query."""
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    pagination_meta = {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }
    
    return pagination.items, pagination_meta
