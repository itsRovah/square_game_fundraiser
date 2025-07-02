import random
from datetime import datetime
from app import db
from app.models import Square, Winner


def draw_random_winner(fundraiser, notes=None):
    """
    Draw a random winner from sold squares.
    
    Args:
        fundraiser: Fundraiser instance
        notes: Optional notes for the draw
        
    Returns:
        Winner instance or None if no sold squares
    """
    # Get all sold squares
    sold_squares = fundraiser.squares.filter_by(is_sold=True).all()
    
    if not sold_squares:
        return None
    
    # Select random winner
    winning_square = random.choice(sold_squares)
    
    # Create winner record
    winner = Winner(
        fundraiser_id=fundraiser.id,
        square_id=winning_square.id,
        winner_name=winning_square.purchaser_name,
        draw_date=datetime.utcnow(),
        notes=notes
    )
    
    db.session.add(winner)
    db.session.commit()
    
    return winner


def get_winner_history(fundraiser):
    """Get all winners for a fundraiser."""
    return fundraiser.winners.order_by(Winner.draw_date.desc()).all()


def export_playlist_csv(fundraiser):
    """
    Export collection data as CSV format.
    
    Returns:
        List of dictionaries for CSV export
    """
    squares = fundraiser.squares.filter(
        Square.is_sold == True,
        Square.song_title != None
    ).order_by(Square.position_number).all()
    
    playlist_data = []
    for square in squares:
        playlist_data.append({
            f'{fundraiser.square_label} Number': square.position_number,
            f'{fundraiser.content_type} Name': square.display_name or '',
            'Purchaser Name': square.purchaser_name or '',
            'Song Title': square.song_title or '',
            'Song Artist': square.song_artist or ''
        })
    
    return playlist_data


def export_grid_csv(fundraiser):
    """
    Export all grid data as CSV format.
    
    Returns:
        List of dictionaries for CSV export
    """
    squares = fundraiser.squares.order_by(Square.position_number).all()
    
    grid_data = []
    for square in squares:
        grid_data.append({
            f'{fundraiser.square_label} Number': square.position_number,
            'Row': square.row + 1,  # Convert to 1-based
            'Column': square.column + 1,  # Convert to 1-based
            f'{fundraiser.content_type} Name': square.display_name or '',
            'Description': square.display_description or '',
            'Status': 'Sold' if square.is_sold else 'Available',
            'Purchaser Name': square.purchaser_name or '',
            'Song Title': square.song_title or '',
            'Song Artist': square.song_artist or '',
            'Purchase Date': square.purchase_date.strftime('%Y-%m-%d %H:%M') if square.purchase_date else ''
        })
    
    return grid_data


def export_purchasers_csv(fundraiser):
    """
    Export purchasers list as CSV format.
    
    Returns:
        List of dictionaries for CSV export
    """
    squares = fundraiser.squares.filter_by(is_sold=True).order_by(Square.purchase_date).all()
    
    purchasers_data = []
    for square in squares:
        purchasers_data.append({
            f'{fundraiser.square_label} Number': square.position_number,
            f'{fundraiser.content_type} Name': square.display_name or '',
            'Purchaser Name': square.purchaser_name or '',
            'Purchase Date': square.purchase_date.strftime('%Y-%m-%d %H:%M') if square.purchase_date else '',
            'Song Provided': 'Yes' if square.song_title else 'No'
        })
    
    return purchasers_data 