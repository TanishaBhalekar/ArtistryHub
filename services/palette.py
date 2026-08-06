import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def extract_dominant_colors(image_source, num_colors=5):
    """
    Parses an uploaded image using OpenCV and Scikit-Learn KMeans clustering
    to extract its N dominant HEX color profiles and their percentage distribution.
    
    :param image_source: File path (str), FileStorage, or bytes
    :param num_colors: Number of dominant colors to extract (default: 5)
    :return: List of color dicts [{'hex': '#HEX', 'rgb': (r,g,b), 'percentage': float}]
    """
    # 1. Load image into numpy array in RGB format
    if isinstance(image_source, str):
        img_bgr = cv2.imread(image_source)
        if img_bgr is None:
            raise ValueError(f"Unable to read image file at {image_source}")
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    elif hasattr(image_source, 'read'):
        # File-like object (Flask FileStorage or BytesIO)
        image_bytes = image_source.read()
        image_source.seek(0)  # Reset pointer
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_bgr is not None:
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        else:
            # Fallback to PIL
            pil_img = Image.open(image_source).convert('RGB')
            img_rgb = np.array(pil_img)
            image_source.seek(0)
    elif isinstance(image_source, np.ndarray):
        img_rgb = image_source
    else:
        raise ValueError("Invalid image input type.")

    # 2. Resize image for fast KMeans clustering performance
    max_dimension = 150
    h, w = img_rgb.shape[:2]
    if max(h, w) > max_dimension:
        scale = max_dimension / float(max(h, w))
        new_w, new_h = int(w * scale), int(h * scale)
        img_resized = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        img_resized = img_rgb

    # 3. Reshape pixel array into (N, 3) matrix
    pixels = img_resized.reshape((-1, 3))

    # Clamp num_colors if pixel count is small
    n_clusters = min(num_colors, len(pixels))
    if n_clusters <= 0:
        return []

    # 4. Perform KMeans Clustering
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_

    # 5. Count label distribution to calculate dominance percentages
    counts = np.bincount(labels)
    total_pixels = len(labels)

    # Combine centers with counts and sort descending by weight
    sorted_indices = np.argsort(counts)[::-1]

    colors_result = []
    for idx in sorted_indices:
        r, g, b = [int(np.clip(round(c), 0, 255)) for c in centers[idx]]
        hex_code = f"#{r:02X}{g:02X}{b:02X}"
        percentage = round((counts[idx] / total_pixels) * 100, 1)

        # Determine readable text contrast (Black or White)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        text_color = "#000000" if luminance > 0.5 else "#FFFFFF"

        colors_result.append({
            'hex': hex_code,
            'rgb': (r, g, b),
            'rgb_str': f"rgb({r}, {g}, {b})",
            'percentage': percentage,
            'text_color': text_color
        })

    return colors_result
