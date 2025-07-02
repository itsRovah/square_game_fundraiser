from flask import Blueprint, jsonify, url_for
from app.models import Fundraiser, Square

api_bp = Blueprint('api', __name__)


def clean_image_path(path):
    """Clean image path for proper URL construction."""
    if not path:
        return None
    # Remove 'static/' prefix if present
    return path.replace('static/', '') if path.startswith('static/') else path


@api_bp.route('/fundraiser/<int:fundraiser_id>/progress')
def get_progress(fundraiser_id):
    """Get fundraiser progress data."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    
    return jsonify({
        'total_squares': fundraiser.total_squares,
        'sold_squares': fundraiser.sold_squares,
        'progress_percentage': fundraiser.progress_percentage,
        'available_squares': fundraiser.total_squares - fundraiser.sold_squares
    })


@api_bp.route('/square/<int:square_id>')
def get_square_details(square_id):
    """Get details for a specific square."""
    square = Square.query.get_or_404(square_id)
    
    # Clean image paths and create full URLs - use display properties for backward compatibility
    photo_path = clean_image_path(square.display_photo_path)
    thumb_path = clean_image_path(square.display_thumbnail_path)
    
    return jsonify({
        'id': square.id,
        'position_number': square.position_number,
        'content_name': square.display_name,
        'content_description': square.display_description,
        'is_sold': square.is_sold,
        'purchaser_name': square.purchaser_name,
        'song_title': square.song_title,
        'song_artist': square.song_artist,
        'has_image': bool(square.display_photo_path),
        'content_photo_path': photo_path,
        'content_thumbnail_path': thumb_path,
        'content_photo_url': url_for('static', filename=photo_path) if photo_path else None,
        'content_thumbnail_url': url_for('static', filename=thumb_path) if thumb_path else None,
        # Legacy fields for backward compatibility
        'animal_name': square.display_name,
        'animal_description': square.display_description,
        'animal_photo_path': photo_path,
        'animal_thumbnail_path': thumb_path,
        'animal_photo_url': url_for('static', filename=photo_path) if photo_path else None,
        'animal_thumbnail_url': url_for('static', filename=thumb_path) if thumb_path else None
    }) 