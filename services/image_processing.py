import os
import uuid
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_and_save_image(file_storage, upload_folder, max_dim=1920, thumb_size=300):
    """
    Processes an uploaded image file using Pillow:
    1. Validates and generates a secure, unique filename.
    2. Compresses the original artwork (max dimension 1920px, JPEG quality 85 or optimized PNG).
    3. Creates a 300px thumbnail version.
    4. Saves both files in upload_folder and returns (filename, thumbnail_filename).
    """
    if not file_storage or file_storage.filename == '':
        raise ValueError("No file selected for upload.")

    if not allowed_file(file_storage.filename):
        raise ValueError("Unsupported file format. Please upload PNG, JPG, JPEG, WEBP, or GIF.")

    # Extract extension and generate unique filename
    original_name = secure_filename(file_storage.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    unique_id = uuid.uuid4().hex
    
    filename = f"{unique_id}.{ext}"
    thumb_filename = f"thumb_{unique_id}.{ext}"

    # Ensure target directory structure exists
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    thumb_path = os.path.join(upload_folder, thumb_filename)

    # Open image with Pillow
    image = Image.open(file_storage)

    # Preserve orientation metadata if present (EXIF)
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    # Standardize color mode for JPEG conversion if needed
    save_format = 'JPEG' if ext in ['jpg', 'jpeg'] else ext.upper()
    if save_format == 'JPEG' and image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')

    # 1. Save Compressed Original Artwork
    orig_copy = image.copy()
    orig_copy.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    
    save_kwargs = {'optimize': True}
    if save_format == 'JPEG':
        save_kwargs['quality'] = 85

    orig_copy.save(file_path, **save_kwargs)

    # 2. Generate 300px Thumbnail
    thumb_copy = image.copy()
    # Fit into a 300x300 bounding box keeping aspect ratio
    thumb_copy.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
    thumb_copy.save(thumb_path, **save_kwargs)

    return filename, thumb_filename
