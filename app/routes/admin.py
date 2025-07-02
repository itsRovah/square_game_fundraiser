from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from app.models import User, Fundraiser, Square, Winner
from app.forms import LoginForm, FundraiserForm, SquareForm, DrawWinnerForm, ExportForm
from app.utils.image_handler import process_and_save_image, delete_image_files
from app.utils.winner_selector import draw_random_winner, export_playlist_csv, export_grid_csv, export_purchasers_csv
import csv
import io
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists, create default admin if not
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user and form.username.data == current_app.config['ADMIN_USERNAME']:
            # Create default admin user
            user = User(username=current_app.config['ADMIN_USERNAME'])
            user.set_password(current_app.config['ADMIN_PASSWORD'])
            db.session.add(user)
            db.session.commit()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    """Log out admin user."""
    logout_user()
    return redirect(url_for('public.index'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard showing all fundraisers."""
    fundraisers = Fundraiser.query.order_by(Fundraiser.created_at.desc()).all()
    return render_template('admin/dashboard.html', fundraisers=fundraisers)


@admin_bp.route('/fundraiser/new', methods=['GET', 'POST'])
@login_required
def create_fundraiser():
    """Create a new fundraiser."""
    form = FundraiserForm()
    
    if form.validate_on_submit():
        fundraiser = Fundraiser(
            name=form.name.data,
            description=form.description.data,
            slug=form.slug.data,
            grid_rows=form.grid_rows.data,
            grid_columns=form.grid_columns.data,
            is_active=form.is_active.data,
            content_type=form.content_type.data or 'Item',
            square_label=form.square_label.data or 'Square',
            collection_name=form.collection_name.data or 'Collection',
            contact_text=form.contact_text.data or 'Contact us to purchase an available square!',
            contact_url=form.contact_url.data or 'https://facebook.com',
            contact_button_text=form.contact_button_text.data or 'Contact us to sponsor',
            success_message=form.success_message.data or 'Thank you for your support!',
            enable_song_contributions=form.enable_song_contributions.data
        )
        db.session.add(fundraiser)
        db.session.commit()
        
        # Create squares for the grid
        for row in range(fundraiser.grid_rows):
            for col in range(fundraiser.grid_columns):
                position_number = (row * fundraiser.grid_columns) + col + 1
                square = Square(
                    fundraiser_id=fundraiser.id,
                    row=row,
                    column=col,
                    position_number=position_number
                )
                db.session.add(square)
        
        db.session.commit()
        flash(f'Fundraiser "{fundraiser.name}" created successfully!', 'success')
        return redirect(url_for('admin.manage_fundraiser', fundraiser_id=fundraiser.id))
    
    # Set default values
    form.grid_rows.data = form.grid_rows.data or current_app.config['DEFAULT_GRID_ROWS']
    form.grid_columns.data = form.grid_columns.data or current_app.config['DEFAULT_GRID_COLUMNS']
    form.is_active.data = True
    
    return render_template('admin/fundraiser_form.html', form=form, title='Create Fundraiser')


@admin_bp.route('/fundraiser/<int:fundraiser_id>')
@login_required
def manage_fundraiser(fundraiser_id):
    """Manage a specific fundraiser."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    squares = fundraiser.squares.order_by(Square.position_number).all()
    
    # Organize squares into grid
    grid = []
    for row in range(fundraiser.grid_rows):
        grid_row = []
        for col in range(fundraiser.grid_columns):
            square = next((s for s in squares if s.row == row and s.column == col), None)
            grid_row.append(square)
        grid.append(grid_row)
    
    return render_template('admin/manage_fundraiser.html', 
                         fundraiser=fundraiser, 
                         grid=grid)


@admin_bp.route('/fundraiser/<int:fundraiser_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_fundraiser(fundraiser_id):
    """Edit fundraiser details."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    form = FundraiserForm(obj=fundraiser)
    
    if form.validate_on_submit():
        # Don't allow grid size changes after creation
        fundraiser.name = form.name.data
        fundraiser.description = form.description.data
        fundraiser.slug = form.slug.data
        fundraiser.is_active = form.is_active.data
        fundraiser.content_type = form.content_type.data or 'Item'
        fundraiser.square_label = form.square_label.data or 'Square'
        fundraiser.collection_name = form.collection_name.data or 'Collection'
        fundraiser.contact_text = form.contact_text.data or 'Contact us to purchase an available square!'
        fundraiser.contact_url = form.contact_url.data or 'https://facebook.com'
        fundraiser.contact_button_text = form.contact_button_text.data or 'Contact us to sponsor'
        fundraiser.success_message = form.success_message.data or 'Thank you for your support!'
        fundraiser.enable_song_contributions = form.enable_song_contributions.data
        
        db.session.commit()
        flash('Fundraiser updated successfully!', 'success')
        return redirect(url_for('admin.manage_fundraiser', fundraiser_id=fundraiser.id))
    
    return render_template('admin/fundraiser_form.html', 
                         form=form, 
                         title='Edit Fundraiser',
                         fundraiser=fundraiser)


@admin_bp.route('/fundraiser/<int:fundraiser_id>/archive', methods=['POST'])
@login_required
def archive_fundraiser(fundraiser_id):
    """Archive a fundraiser."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    fundraiser.is_archived = True
    fundraiser.is_active = False
    db.session.commit()
    flash(f'Fundraiser "{fundraiser.name}" has been archived.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/fundraiser/<int:fundraiser_id>/delete', methods=['POST'])
@login_required
def delete_fundraiser(fundraiser_id):
    """Delete an archived fundraiser permanently."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    
    # Only allow deletion of archived fundraisers
    if not fundraiser.is_archived:
        flash('Only archived fundraisers can be deleted. Please archive it first.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    fundraiser_name = fundraiser.name
    
    # Delete associated images before deleting the fundraiser
    # The cascade will handle database deletion of squares and winners
    for square in fundraiser.squares:
        if square.display_photo_path:
            delete_image_files(square.display_photo_path, square.display_thumbnail_path)
    
    # Delete the fundraiser (cascade will delete squares and winners)
    db.session.delete(fundraiser)
    db.session.commit()
    
    flash(f'Fundraiser "{fundraiser_name}" has been permanently deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/square/<int:square_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_square(square_id):
    """Edit square details."""
    square = Square.query.get_or_404(square_id)
    form = SquareForm(obj=square)
    
    if form.validate_on_submit():
        # Handle image upload - support both new and legacy fields
        image_file = form.content_photo.data or form.animal_photo.data
        if image_file:
            # Delete old images if they exist
            if square.display_photo_path:
                delete_image_files(square.display_photo_path, square.display_thumbnail_path)
            
            # Process and save new image
            full_path, thumb_path = process_and_save_image(
                image_file,
                current_app.config['UPLOAD_FOLDER']
            )
            
            if full_path:
                square.content_photo_path = full_path
                square.content_thumbnail_path = thumb_path
                # Clear legacy fields if using new ones
                square.animal_photo_path = None
                square.animal_thumbnail_path = None
        
        # Update other fields - prefer new fields over legacy
        square.content_name = form.content_name.data or form.animal_name.data
        square.content_description = form.content_description.data or form.animal_description.data
        # Clear legacy fields if using new ones
        if form.content_name.data:
            square.animal_name = None
        if form.content_description.data:
            square.animal_description = None
        
        # Handle sold status
        if form.is_sold.data and not square.is_sold:
            square.mark_as_sold(
                form.purchaser_name.data,
                form.song_title.data,
                form.song_artist.data
            )
        elif form.is_sold.data:
            # Update sold details
            square.purchaser_name = form.purchaser_name.data
            square.song_title = form.song_title.data
            square.song_artist = form.song_artist.data
        elif not form.is_sold.data and square.is_sold:
            # Mark as unsold
            square.is_sold = False
            square.purchaser_name = None
            square.song_title = None
            square.song_artist = None
            square.purchase_date = None
        
        db.session.commit()
        flash('Square updated successfully!', 'success')
        return redirect(url_for('admin.manage_fundraiser', fundraiser_id=square.fundraiser_id))
    
    return render_template('admin/edit_square.html', form=form, square=square)


@admin_bp.route('/fundraiser/<int:fundraiser_id>/draw-winner', methods=['GET', 'POST'])
@login_required
def draw_winner(fundraiser_id):
    """Draw a random winner."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    form = DrawWinnerForm()
    
    if form.validate_on_submit():
        winner = draw_random_winner(fundraiser, form.notes.data)
        
        if winner:
            flash(f'Winner drawn! {winner.winner_name} (Square #{winner.square.position_number})', 'success')
            return redirect(url_for('admin.winner_history', fundraiser_id=fundraiser.id))
        else:
            flash('No sold squares available to draw from!', 'warning')
    
    return render_template('admin/draw_winner.html', form=form, fundraiser=fundraiser)


@admin_bp.route('/fundraiser/<int:fundraiser_id>/winners')
@login_required
def winner_history(fundraiser_id):
    """View winner history."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    winners = fundraiser.winners.order_by(Winner.draw_date.desc()).all()
    return render_template('admin/winner_history.html', fundraiser=fundraiser, winners=winners)


@admin_bp.route('/fundraiser/<int:fundraiser_id>/export', methods=['GET', 'POST'])
@login_required
def export_data(fundraiser_id):
    """Export fundraiser data."""
    fundraiser = Fundraiser.query.get_or_404(fundraiser_id)
    form = ExportForm()
    
    if form.validate_on_submit():
        export_type = form.export_type.data
        
        # Get appropriate data
        if export_type == 'playlist':
            data = export_playlist_csv(fundraiser)
            filename = f"{fundraiser.slug}_playlist_{datetime.now().strftime('%Y%m%d')}.csv"
        elif export_type == 'grid':
            data = export_grid_csv(fundraiser)
            filename = f"{fundraiser.slug}_grid_{datetime.now().strftime('%Y%m%d')}.csv"
        else:  # purchasers
            data = export_purchasers_csv(fundraiser)
            filename = f"{fundraiser.slug}_purchasers_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Create CSV
        if data:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            
            # Create response
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        else:
            flash('No data to export!', 'warning')
    
    return render_template('admin/export.html', form=form, fundraiser=fundraiser) 