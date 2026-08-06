from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Artwork
from services.image_processing import process_and_save_image, allowed_file

portfolio = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio.route('/', methods=['GET'])
@login_required
def index():
    """Display current user's artwork portfolio."""
    artworks = Artwork.query.filter_by(user_id=current_user.id).order_by(Artwork.created_at.desc()).all()
    return render_template('portfolio/index.html', artworks=artworks)


@portfolio.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Handle artwork image uploads and metadata persistence."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        medium = request.form.get('medium', '').strip()
        category = request.form.get('category', '').strip()
        tags = request.form.get('tags', '').strip()
        visibility = request.form.get('visibility', 'public').strip()

        # Check title
        if not title:
            flash('Artwork title is required.', 'danger')
            return redirect(request.url)

        # Check uploaded image file
        file = request.files.get('image')
        if not file or file.filename == '':
            flash('Please select an artwork image file to upload.', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed formats: PNG, JPG, JPEG, WEBP, GIF.', 'danger')
            return redirect(request.url)

        # Process image using Pillow service
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        try:
            filename, thumb_filename = process_and_save_image(file, upload_folder)
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'danger')
            return redirect(request.url)

        # Create Artwork record
        artwork = Artwork(
            title=title,
            description=description,
            medium=medium,
            category=category,
            tags=tags,
            visibility=visibility,
            image_url=filename,
            thumbnail_url=thumb_filename,
            user_id=current_user.id
        )

        try:
            db.session.add(artwork)
            db.session.commit()
            flash(f'Artwork "{title}" uploaded successfully!', 'success')
            return redirect(url_for('portfolio.index'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to save artwork metadata to database.', 'danger')
            return redirect(request.url)

    return render_template('portfolio/upload.html')
