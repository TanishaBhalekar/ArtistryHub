import os
import uuid
import cv2
import numpy as np
from PIL import Image

def analyze_composition(image_source, upload_folder):
    """
    Uses OpenCV edge-detection (Canny) and focal center tracking to calculate
    composition metrics and overlay Rule-of-Thirds & focal reticles over user layout sketches.

    :param image_source: File path (str), FileStorage, or bytes
    :param upload_folder: Target directory to save analyzed composition guide image
    :return: dict with processed image URL, composition metrics, and focal alignment scores
    """
    # 1. Load Image with OpenCV
    if isinstance(image_source, str):
        img_bgr = cv2.imread(image_source)
    elif hasattr(image_source, 'read'):
        image_bytes = image_source.read()
        image_source.seek(0)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(image_source, np.ndarray):
        img_bgr = image_source
    else:
        raise ValueError("Invalid image input type.")

    if img_bgr is None:
        raise ValueError("Failed to decode image for composition analysis.")

    h, w, c = img_bgr.shape
    
    # 2. Convert to Grayscale & Apply Gaussian Blur
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. OpenCV Canny Edge Detection
    edges = cv2.Canny(blurred, 50, 150)
    edge_density = float(np.sum(edges > 0) / (h * w)) * 100.0

    # 4. Focal Point Tracking (Centroid of edge intensities)
    moments = cv2.moments(edges)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = int(w / 2), int(h / 2)

    # Calculate Rule of Thirds alignment score (distance to nearest Rule-of-Thirds intersection)
    rot_x = [int(w / 3), int(2 * w / 3)]
    rot_y = [int(h / 3), int(2 * h / 3)]
    
    min_dist = float('inf')
    nearest_intersection = (rot_x[0], rot_y[0])
    for rx in rot_x:
        for ry in rot_y:
            dist = np.sqrt((cx - rx) ** 2 + (cy - ry) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest_intersection = (rx, ry)

    max_possible_dist = np.sqrt((w / 6) ** 2 + (h / 6) ** 2)
    alignment_score = max(0, min(100, int((1.0 - (min_dist / max_possible_dist)) * 100)))

    # 5. Create Composition Guide Overlay Image
    # Convert edge map to 3-channel RGB for glowing guide lines
    overlay_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Blend original image with edge map
    guide_img = cv2.addWeighted(img_bgr, 0.55, overlay_img, 0.45, 0)

    # Draw Rule of Thirds Lines (Cyan glowing lines)
    grid_color = (212, 182, 6) # Cyan in BGR (06B6D4)
    line_thickness = max(1, int(min(h, w) / 300))

    # Vertical grid lines
    cv2.line(guide_img, (rot_x[0], 0), (rot_x[0], h), grid_color, line_thickness)
    cv2.line(guide_img, (rot_x[1], 0), (rot_x[1], h), grid_color, line_thickness)
    # Horizontal grid lines
    cv2.line(guide_img, (0, rot_y[0]), (w, rot_y[0]), grid_color, line_thickness)
    cv2.line(guide_img, (0, rot_y[1]), (w, rot_y[1]), grid_color, line_thickness)

    # Draw Focal Tracking Reticle (Purple circle & target in BGR: 8B5CF6 -> (246, 92, 139))
    focal_color = (246, 92, 139)
    reticle_radius = max(12, int(min(h, w) / 25))
    cv2.circle(guide_img, (cx, cy), reticle_radius, focal_color, line_thickness + 1)
    cv2.circle(guide_img, (cx, cy), 4, (255, 255, 255), -1)
    cv2.line(guide_img, (cx - reticle_radius - 6, cy), (cx + reticle_radius + 6, cy), focal_color, 1)
    cv2.line(guide_img, (cx, cy - reticle_radius - 6), (cx, cy + reticle_radius + 6), focal_color, 1)

    # 6. Save guide overlay image
    os.makedirs(upload_folder, exist_ok=True)
    guide_filename = f"guide_{uuid.uuid4().hex}.png"
    guide_path = os.path.join(upload_folder, guide_filename)
    cv2.imwrite(guide_path, guide_img)

    return {
        'guide_filename': guide_filename,
        'edge_density': round(edge_density, 1),
        'focal_x': cx,
        'focal_y': cy,
        'focal_ratio_x': round(cx / w, 2),
        'focal_ratio_y': round(cy / h, 2),
        'alignment_score': alignment_score,
        'dimensions': f"{w}x{h}",
        'nearest_intersection': nearest_intersection
    }
