import cv2
import numpy as np
from pathlib import Path

CASCADE_FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
CASCADE_EYE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def compute_saliency_map(image: np.ndarray) -> np.ndarray:
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    success, saliency_map = saliency.computeSaliency(image)
    if not success:
        return np.zeros(image.shape[:2], dtype=np.float32)
    return saliency_map.astype(np.float32)


def detect_faces(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = CASCADE_FACE.detectMultiScale(gray, 1.1, 4)
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]


def detect_text_regions(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    h, w = image.shape[:2]
    min_area = (h * w) * 0.001
    max_area = (h * w) * 0.15

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch
        if min_area < area < max_area and cw > ch * 0.5:
            aspect = cw / ch
            if 0.1 < aspect < 15:
                regions.append((int(x), int(y), int(cw), int(ch)))
    return regions[:10]


def compute_contrast_map(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    contrast = np.abs(gray - blurred)
    return contrast / (contrast.max() + 1e-6)


def create_gaussian_peak(shape, regions, sigma=30) -> np.ndarray:
    heatmap = np.zeros(shape[:2], dtype=np.float32)
    for (x, y, w, h) in regions:
        cx, cy = x + w // 2, y + h // 2
        Y, X = np.ogrid[:shape[0], :shape[1]]
        gauss = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * sigma ** 2))
        heatmap += gauss
    return heatmap


def generate_heatmap(image: np.ndarray) -> np.ndarray:
    saliency = compute_saliency_map(image)
    saliency = cv2.GaussianBlur(saliency, (15, 15), 0)

    faces = detect_faces(image)
    face_map = create_gaussian_peak(image.shape, faces, sigma=40)

    text_regions = detect_text_regions(image)
    text_map = create_gaussian_peak(image.shape, text_regions, sigma=20)

    contrast_map = compute_contrast_map(image)
    contrast_map = cv2.GaussianBlur(contrast_map, (15, 15), 0)

    fused = (
        0.40 * saliency +
        0.25 * face_map +
        0.20 * text_map +
        0.15 * contrast_map
    )

    if fused.max() > 0:
        fused = fused / fused.max()

    return fused


def get_attention_description(heatmap: np.ndarray) -> str:
    h, w = heatmap.shape
    quadrants = {
        "top-left": heatmap[:h // 2, :w // 2],
        "top-right": heatmap[:h // 2, w // 2:],
        "bottom-left": heatmap[h // 2:, :w // 2],
        "bottom-right": heatmap[h // 2:, w // 2:],
    }
    avg = {k: v.mean() for k, v in quadrants.items()}
    hot = max(avg, key=avg.get)

    center = heatmap[h // 4: 3 * h // 4, w // 4: 3 * w // 4].mean()
    edge = (heatmap.mean() - center * 0.5) / 0.5 if heatmap.mean() > 0 else 0

    parts = []
    parts.append(f"Primary attention zone: {hot.replace('-', ' ')}")
    if center > 0.4:
        parts.append("Strong center focus — good for logo/CTA placement")
    if edge > 0.5:
        parts.append("Significant edge attention — check if borders distract from CTA")

    return ". ".join(parts) + "."
