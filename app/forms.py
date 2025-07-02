from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError
import re


def validate_slug(form, field):
    """Validate slug format."""
    if not re.match(r'^[a-z0-9-]+$', field.data):
        raise ValidationError('Slug must contain only lowercase letters, numbers, and hyphens.')


def validate_url(form, field):
    """Validate URL format - allows domain names and full URLs."""
    if not field.data:
        return  # Optional field
    
    url = field.data.strip()
    # Allow common URL patterns
    url_patterns = [
        r'^https?://',  # Full URLs with protocol
        r'^[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]*\.', # Domain names
        r'^mailto:',    # Email links
        r'^tel:',       # Phone links
    ]
    
    if not any(re.match(pattern, url) for pattern in url_patterns):
        raise ValidationError('Please enter a valid URL or domain name (e.g., facebook.com or https://facebook.com)')


class LoginForm(FlaskForm):
    """Admin login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class FundraiserForm(FlaskForm):
    """Form for creating/editing fundraisers."""
    name = StringField('Fundraiser Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=200), validate_slug])
    grid_rows = IntegerField('Grid Rows', validators=[DataRequired(), NumberRange(min=1, max=20)])
    grid_columns = IntegerField('Grid Columns', validators=[DataRequired(), NumberRange(min=1, max=20)])
    is_active = BooleanField('Active')
    
    # Configuration fields
    content_type = StringField('Content Type', 
                             validators=[Optional(), Length(max=100)],
                             default='Item',
                             description='What type of content each square represents (e.g., Animal, Prize, Item)')
    square_label = StringField('Square Label', 
                             validators=[Optional(), Length(max=100)],
                             default='Square',
                             description='What to call individual squares (e.g., Square, Spot, Space)')
    collection_name = StringField('Collection Name', 
                                validators=[Optional(), Length(max=100)],
                                default='Collection',
                                description='What to call the collection (e.g., Playlist, Gallery, List)')
    contact_text = TextAreaField('Contact Text', 
                               validators=[Optional()],
                               default='Contact us to purchase an available square!',
                               description='Text shown to encourage participation')
    contact_url = StringField('Contact URL', 
                            validators=[Optional(), Length(max=500), validate_url],
                            default='https://facebook.com',
                            description='URL for contact button (e.g., facebook.com, https://facebook.com, mailto:email@example.com)')
    contact_button_text = StringField('Contact Button Text', 
                                    validators=[Optional(), Length(max=100)],
                                    default='Contact us to sponsor',
                                    description='Text shown on contact button')
    success_message = TextAreaField('Success Message', 
                                  validators=[Optional()],
                                  default='Thank you for your support!',
                                  description='Message shown after successful participation')
    enable_song_contributions = BooleanField('Enable Song/Content Contributions', 
                                           default=True,
                                           description='Allow sponsors to contribute songs or other content items')


class SquareForm(FlaskForm):
    """Form for editing square details."""
    content_name = StringField('Content Name', validators=[Optional(), Length(max=200)])
    content_photo = FileField('Content Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    content_description = TextAreaField('Description/Details', validators=[Optional()])
    is_sold = BooleanField('Mark as Sold')
    purchaser_name = StringField('Purchaser Name', validators=[Optional(), Length(max=200)])
    song_title = StringField('Song/Content Title', validators=[Optional(), Length(max=200)])
    song_artist = StringField('Artist/Creator', validators=[Optional(), Length(max=200)])
    
    # Legacy fields for backward compatibility
    animal_name = StringField('Animal Name', validators=[Optional(), Length(max=200)])
    animal_photo = FileField('Animal Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    animal_description = TextAreaField('Animal Description', validators=[Optional()])


class DrawWinnerForm(FlaskForm):
    """Form for drawing a winner."""
    notes = TextAreaField('Notes', validators=[Optional()])


class ExportForm(FlaskForm):
    """Form for export options."""
    export_type = SelectField('Export Type', 
                            choices=[('playlist', 'Collection Data (CSV)'), 
                                   ('grid', 'Grid Data (CSV)'),
                                   ('purchasers', 'Purchasers List (CSV)')],
                            validators=[DataRequired()]) 