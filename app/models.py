from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Admin user model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Fundraiser(db.Model):
    """Fundraiser model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    grid_rows = db.Column(db.Integer, default=10, nullable=False)
    grid_columns = db.Column(db.Integer, default=10, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Configuration fields for customization
    content_type = db.Column(db.String(100), default='Item')  # e.g., 'Animal', 'Prize', 'Item', etc.
    square_label = db.Column(db.String(100), default='Square')  # What to call individual squares
    collection_name = db.Column(db.String(100), default='Collection')  # e.g., 'Playlist', 'Gallery', 'List'
    contact_text = db.Column(db.Text, default='Contact us to purchase an available square!')
    contact_url = db.Column(db.String(500), default='https://facebook.com')
    contact_button_text = db.Column(db.String(100), default='Contact us to sponsor')
    success_message = db.Column(db.Text, default='Thank you for your support!')
    enable_song_contributions = db.Column(db.Boolean, default=True)
    
    # Relationships
    squares = db.relationship('Square', backref='fundraiser', lazy='dynamic', cascade='all, delete-orphan')
    winners = db.relationship('Winner', backref='fundraiser', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def total_squares(self):
        return self.grid_rows * self.grid_columns
    
    @property
    def sold_squares(self):
        return self.squares.filter_by(is_sold=True).count()
    
    @property
    def progress_percentage(self):
        if self.total_squares == 0:
            return 0
        return int((self.sold_squares / self.total_squares) * 100)


class Square(db.Model):
    """Square model for grid positions."""
    id = db.Column(db.Integer, primary_key=True)
    fundraiser_id = db.Column(db.Integer, db.ForeignKey('fundraiser.id'), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    position_number = db.Column(db.Integer, nullable=False)  # 1-based position number
    
    # Generic content fields (renamed from animal-specific)
    content_name = db.Column(db.String(200))  # Renamed from animal_name
    content_photo_path = db.Column(db.String(500))  # Renamed from animal_photo_path
    content_thumbnail_path = db.Column(db.String(500))  # Renamed from animal_thumbnail_path
    content_description = db.Column(db.Text)  # Renamed from animal_description
    
    # Purchase/sponsor information
    is_sold = db.Column(db.Boolean, default=False)
    purchaser_name = db.Column(db.String(200))
    song_title = db.Column(db.String(200))
    song_artist = db.Column(db.String(200))
    purchase_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Legacy fields for backward compatibility (will be migrated)
    animal_name = db.Column(db.String(200))
    animal_photo_path = db.Column(db.String(500))
    animal_thumbnail_path = db.Column(db.String(500))
    animal_description = db.Column(db.Text)
    
    # Ensure unique position per fundraiser
    __table_args__ = (
        db.UniqueConstraint('fundraiser_id', 'row', 'column', name='_fundraiser_position_uc'),
        db.UniqueConstraint('fundraiser_id', 'position_number', name='_fundraiser_number_uc'),
    )
    
    def mark_as_sold(self, purchaser_name, song_title=None, song_artist=None):
        """Mark square as sold."""
        self.is_sold = True
        self.purchaser_name = purchaser_name
        self.song_title = song_title
        self.song_artist = song_artist
        self.purchase_date = datetime.utcnow()
    
    # Properties for backward compatibility and migration
    @property
    def display_name(self):
        """Get the display name, preferring new field over legacy."""
        return self.content_name or self.animal_name
    
    @property
    def display_photo_path(self):
        """Get the photo path, preferring new field over legacy."""
        return self.content_photo_path or self.animal_photo_path
    
    @property
    def display_thumbnail_path(self):
        """Get the thumbnail path, preferring new field over legacy."""
        return self.content_thumbnail_path or self.animal_thumbnail_path
    
    @property
    def display_description(self):
        """Get the description, preferring new field over legacy."""
        return self.content_description or self.animal_description


class Winner(db.Model):
    """Winner history model."""
    id = db.Column(db.Integer, primary_key=True)
    fundraiser_id = db.Column(db.Integer, db.ForeignKey('fundraiser.id'), nullable=False)
    square_id = db.Column(db.Integer, db.ForeignKey('square.id'), nullable=False)
    winner_name = db.Column(db.String(200), nullable=False)
    draw_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    square = db.relationship('Square', backref='winner_record') 