import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import db, Artwork
from services.palette import extract_dominant_colors
from services.vision import analyze_composition
from services.prompt_forge import (
    construct_prompt,
    STYLE_DATABASE,
    THEME_TEMPLATES,
    MOOD_MODIFIERS,
    STYLE_DIRECTIVES,
    LIGHTING_DIRECTIVES,
    CAMERA_DIRECTIVES
)
from services.image_processing import allowed_file

ai = Blueprint('ai', __name__, url_prefix='/ai')

# ----------------------------------------------------
# 0. AI Studio Hub Landing View (/ai-studio or /ai/studio)
# ----------------------------------------------------
@ai.route('/studio', methods=['GET'])
@ai.route('/hub', methods=['GET'])
@login_required
def hub():
    """Render the unified AI Studio Hub landing view."""
    return render_template('ai/hub.html')

# ----------------------------------------------------
# 1. Palette Lab Tool
# ----------------------------------------------------
@ai.route('/palette-lab', methods=['GET'])
@login_required
def palette_lab():
    """Render the Palette Lab tool UI."""
    user_artworks = Artwork.query.filter_by(user_id=current_user.id).order_by(Artwork.created_at.desc()).all()
    return render_template('ai/palette.html', artworks=user_artworks)


@ai.route('/extract-palette', methods=['POST'])
@login_required
def extract_palette():
    """Extract 5 dominant HEX colors using OpenCV and Scikit-Learn KMeans."""
    image_source = None
    display_image_url = None

    file = request.files.get('image')
    if file and file.filename != '':
        if not allowed_file(file.filename):
            if request.is_json:
                return jsonify({'success': False, 'error': 'Invalid image format.'}), 400
            flash('Invalid image format.', 'danger')
            return redirect(url_for('ai.palette_lab'))
        image_source = file

    if not image_source:
        artwork_id = request.form.get('artwork_id') or (request.json.get('artwork_id') if request.is_json else None)
        if artwork_id:
            art = Artwork.query.filter_by(id=artwork_id, user_id=current_user.id).first()
            if art and art.image_url:
                upload_folder = current_app.config.get('UPLOAD_FOLDER')
                file_path = os.path.join(upload_folder, art.image_url)
                if os.path.exists(file_path):
                    image_source = file_path
                    display_image_url = url_for('static', filename='uploads/' + art.image_url)

    if not image_source:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Please upload an image or select a portfolio artwork.'}), 400
        flash('Please upload an image or select a portfolio artwork.', 'warning')
        return redirect(url_for('ai.palette_lab'))

    try:
        colors = extract_dominant_colors(image_source, num_colors=5)
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'palette': colors, 'image_url': display_image_url})

        user_artworks = Artwork.query.filter_by(user_id=current_user.id).all()
        return render_template('ai/palette.html', artworks=user_artworks, palette=colors, selected_image_url=display_image_url)

    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        flash(f'Error extracting color palette: {str(e)}', 'danger')
        return redirect(url_for('ai.palette_lab'))


# ----------------------------------------------------
# 2. Prompt Forge Tool
# ----------------------------------------------------
@ai.route('/prompt-forge', methods=['GET'])
@login_required
def prompt_forge():
    """Render the Prompt Forge interactive panel."""
    initial_prompt = construct_prompt()
    return render_template(
        'ai/prompt_forge.html',
        themes=list(THEME_TEMPLATES.keys()),
        moods=list(MOOD_MODIFIERS.keys()),
        styles=list(STYLE_DIRECTIVES.keys()),
        lightings=list(LIGHTING_DIRECTIVES.keys()),
        cameras=list(CAMERA_DIRECTIVES.keys()),
        result=initial_prompt
    )


@ai.route('/forge-prompt', methods=['POST'])
@login_required
def forge_prompt():
    """Construct detailed descriptive prompt from dropdown conditions."""
    if request.is_json:
        data = request.get_json()
        theme = data.get('theme', 'Cyberpunk City')
        mood = data.get('mood', 'Ethereal & Mystical')
        style = data.get('style', 'Digital Concept Art (UE5)')
        lighting = data.get('lighting', 'Neon Rim Lighting')
        camera = data.get('camera', 'Cinematic Wide Angle')
    else:
        theme = request.form.get('theme', 'Cyberpunk City')
        mood = request.form.get('mood', 'Ethereal & Mystical')
        style = request.form.get('style', 'Digital Concept Art (UE5)')
        lighting = request.form.get('lighting', 'Neon Rim Lighting')
        camera = request.form.get('camera', 'Cinematic Wide Angle')

    result = construct_prompt(theme, mood, style, lighting, camera)

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'data': result})

    return render_template(
        'ai/prompt_forge.html',
        themes=list(THEME_TEMPLATES.keys()),
        moods=list(MOOD_MODIFIERS.keys()),
        styles=list(STYLE_DIRECTIVES.keys()),
        lightings=list(LIGHTING_DIRECTIVES.keys()),
        cameras=list(CAMERA_DIRECTIVES.keys()),
        result=result
    )


# ----------------------------------------------------
# 3. Style Explorer Tool
# ----------------------------------------------------
@ai.route('/style-explorer', methods=['GET'])
@login_required
def style_explorer():
    """Render the Style Explorer static recommendation database."""
    category_filter = request.args.get('category', 'all').strip()
    
    if category_filter and category_filter.lower() != 'all':
        filtered_styles = [s for s in STYLE_DATABASE if s['category'].lower() == category_filter.lower()]
    else:
        filtered_styles = STYLE_DATABASE

    categories = list(set([s['category'] for s in STYLE_DATABASE]))

    return render_template(
        'ai/style_explorer.html',
        styles=filtered_styles,
        categories=categories,
        selected_category=category_filter
    )


# ----------------------------------------------------
# 4. Composition Guide Tool
# ----------------------------------------------------
@ai.route('/composition-guide', methods=['GET'])
@login_required
def composition_guide():
    """Render Composition Guide tool UI."""
    user_artworks = Artwork.query.filter_by(user_id=current_user.id).order_by(Artwork.created_at.desc()).all()
    return render_template('ai/composition.html', artworks=user_artworks)


@ai.route('/analyze-composition', methods=['POST'])
@login_required
def analyze_comp():
    """Run OpenCV Canny edge detection & focal tracking over layout sketches."""
    image_source = None
    original_url = None

    file = request.files.get('image')
    if file and file.filename != '':
        if not allowed_file(file.filename):
            if request.is_json:
                return jsonify({'success': False, 'error': 'Invalid image format.'}), 400
            flash('Invalid image format.', 'danger')
            return redirect(url_for('ai.composition_guide'))
        image_source = file

    if not image_source:
        artwork_id = request.form.get('artwork_id') or (request.json.get('artwork_id') if request.is_json else None)
        if artwork_id:
            art = Artwork.query.filter_by(id=artwork_id, user_id=current_user.id).first()
            if art and art.image_url:
                upload_folder = current_app.config.get('UPLOAD_FOLDER')
                file_path = os.path.join(upload_folder, art.image_url)
                if os.path.exists(file_path):
                    image_source = file_path
                    original_url = url_for('static', filename='uploads/' + art.image_url)

    if not image_source:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Please upload a layout sketch or select a portfolio artwork.'}), 400
        flash('Please upload a layout sketch or select a portfolio artwork.', 'warning')
        return redirect(url_for('ai.composition_guide'))

    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    try:
        metrics = analyze_composition(image_source, upload_folder)
        guide_url = url_for('static', filename='uploads/' + metrics['guide_filename'])

        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'guide_url': guide_url,
                'original_url': original_url,
                'metrics': metrics
            })

        user_artworks = Artwork.query.filter_by(user_id=current_user.id).all()
        return render_template(
            'ai/composition.html',
            artworks=user_artworks,
            guide_url=guide_url,
            original_url=original_url,
            metrics=metrics
        )

    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        flash(f'Error analyzing composition: {str(e)}', 'danger')
        return redirect(url_for('ai.composition_guide'))
