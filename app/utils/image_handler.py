import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
import uuid


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(original_filename):
    """Generate a unique filename while preserving the extension."""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


def crop_center_square(image):
    """Crop image to square from center."""
    width, height = image.size
    
    # Determine the size of the square
    size = min(width, height)
    
    # Calculate coordinates for center crop
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    
    # Crop the image
    return image.crop((left, top, right, bottom))


def crop_square_smart(image):
    """Crop image to square using smart cropping - focuses on the most important area."""
    width, height = image.size
    
    # If already square, return as is
    if width == height:
        return image
    
    # Determine the size of the square
    size = min(width, height)
    
    # Smart cropping logic
    if width > height:
        # Landscape: try to focus on center-left for portraits, or true center for landscapes
        # For faces/portraits, slightly favor left side
        left = max(0, (width - size) // 3)  # Slightly left of center
        top = 0
    else:
        # Portrait: favor upper portion for faces
        left = 0
        top = max(0, (height - size) // 4)  # Slightly above center
    
    right = left + size
    bottom = top + size
    
    # Ensure we don't go out of bounds
    if right > width:
        left = width - size
        right = width
    if bottom > height:
        top = height - size
        bottom = height
    
    return image.crop((left, top, right, bottom))


def process_and_save_image(file, upload_folder):
    """Process uploaded image and save both full size and thumbnail."""
    if not file or not allowed_file(file.filename):
        return None, None
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename)
    base_name = filename.rsplit('.', 1)[0]
    ext = filename.rsplit('.', 1)[1]
    
    # Create full path - handle static/uploads or uploads
    if upload_folder.startswith('static/'):
        upload_path = os.path.join(current_app.root_path, '..', upload_folder)
    else:
        upload_path = os.path.join(current_app.root_path, '..', 'static', upload_folder)
    
    os.makedirs(upload_path, exist_ok=True)
    print(f"DEBUG: Upload path: {upload_path}")  # Debug logging
    
    # Open and process image
    image = Image.open(file)
    
    # Convert RGBA to RGB if necessary
    if image.mode in ('RGBA', 'LA', 'P'):
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = rgb_image
    
    # Crop to square using smart cropping
    square_image = crop_square_smart(image)
    
    # Save full size (max 800x800)
    full_size = square_image.copy()
    full_size.thumbnail(current_app.config['IMAGE_SIZE'], Image.Resampling.LANCZOS)
    full_filename = f"{base_name}_full.{ext}"
    full_path = os.path.join(upload_path, full_filename)
    full_size.save(full_path, quality=90, optimize=True)
    
    # Save thumbnail
    thumbnail = square_image.copy()
    thumbnail.thumbnail(current_app.config['THUMBNAIL_SIZE'], Image.Resampling.LANCZOS)
    thumb_filename = f"{base_name}_thumb.{ext}"
    thumb_path = os.path.join(upload_path, thumb_filename)
    thumbnail.save(thumb_path, quality=85, optimize=True)
    
    # Return relative paths for database storage (relative to static folder)
    # Remove 'static/' prefix if present since url_for('static') will add it
    upload_relative = upload_folder.replace('static/', '') if upload_folder.startswith('static/') else upload_folder
    
    full_db_path = os.path.join(upload_relative, full_filename)
    thumb_db_path = os.path.join(upload_relative, thumb_filename)
    
    print(f"DEBUG: Returning paths - Full: {full_db_path}, Thumb: {thumb_db_path}")  # Debug logging
    return full_db_path, thumb_db_path


def delete_image_files(full_path, thumbnail_path):
    """Delete image files if they exist."""
    if full_path:
        full_file = os.path.join(current_app.root_path, '..', full_path)
        if os.path.exists(full_file):
            os.remove(full_file)
    
    if thumbnail_path:
        thumb_file = os.path.join(current_app.root_path, '..', thumbnail_path)
        if os.path.exists(thumb_file):
            os.remove(thumb_file) 