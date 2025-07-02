from flask import Blueprint, render_template, abort
from app.models import Fundraiser, Square

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    """Homepage showing active fundraisers."""
    active_fundraisers = Fundraiser.query.filter_by(
        is_active=True, 
        is_archived=False
    ).order_by(Fundraiser.created_at.desc()).all()
    
    return render_template('public/index.html', fundraisers=active_fundraisers)


@public_bp.route('/fundraiser/<slug>')
def view_fundraiser(slug):
    """View a specific fundraiser grid."""
    fundraiser = Fundraiser.query.filter_by(slug=slug).first_or_404()
    
    # Check if fundraiser is viewable
    if fundraiser.is_archived and not fundraiser.is_active:
        abort(404)
    
    # Get all squares
    squares = fundraiser.squares.order_by(Square.position_number).all()
    
    # Organize squares into grid
    grid = []
    for row in range(fundraiser.grid_rows):
        grid_row = []
        for col in range(fundraiser.grid_columns):
            square = next((s for s in squares if s.row == row and s.column == col), None)
            grid_row.append(square)
        grid.append(grid_row)
    
    return render_template('public/grid.html', 
                         fundraiser=fundraiser, 
                         grid=grid)


@public_bp.route('/fundraiser/<slug>/playlist')
def view_playlist(slug):
    """View the playlist for a fundraiser."""
    fundraiser = Fundraiser.query.filter_by(slug=slug).first_or_404()
    
    # Check if fundraiser is viewable
    if fundraiser.is_archived and not fundraiser.is_active:
        abort(404)
    
    # Get all squares with songs
    songs = fundraiser.squares.filter(
        Square.is_sold == True,
        Square.song_title != None
    ).order_by(Square.purchase_date).all()
    
    return render_template('public/playlist.html', 
                         fundraiser=fundraiser, 
                         songs=songs) 