import cv2
import numpy as np
from sklearn.cluster import KMeans


def extract_colors(image: np.ndarray, n_colors: int = 6) -> list:
    pixels = image.reshape(-1, 3).astype(np.float32)
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    total = counts.sum()

    colors = []
    for center, count in sorted(zip(kmeans.cluster_centers_, counts), key=lambda x: -x[1]):
        hex_color = "#{:02x}{:02x}{:02x}".format(int(center[2]), int(center[1]), int(center[0]))
        colors.append({
            "hex": hex_color,
            "rgb": [int(center[2]), int(center[1]), int(center[0])],
            "percentage": round(count / total * 100, 1)
        })
    return colors


def analyze_color_harmony(colors: list) -> dict:
    if not colors:
        return {"score": 50, "feedback": "No colors detected"}

    dominant = colors[0]["rgb"]
    r, g, b = dominant
    h, s, v = _rgb_to_hsv(r, g, b)

    analogous = sum(1 for c in colors[1:4]
                     if abs(_rgb_to_hsv(*c["rgb"])[0] - h) < 30)
    score = min(95, 50 + analogous * 15)

    if analogous >= 2:
        feedback = "Harmonious analogous palette"
    elif s < 20:
        feedback = "Low saturation — consider adding contrast"
    elif v < 50:
        feedback = "Dark dominant tones — ensure readability"
    else:
        feedback = "Diverse palette — verify brand consistency"

    return {"score": score, "feedback": feedback}


def analyze_composition(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)
    thirds_h = [h // 3, 2 * h // 3]
    thirds_w = [w // 3, 2 * w // 3]

    hotspots = 0
    for th in thirds_h:
        for tw in thirds_w:
            region = edges[max(0, th - 25):th + 25, max(0, tw - 25):tw + 25]
            if region.mean() > 20:
                hotspots += 1

    left_half = gray[:, :w // 2].astype(float)
    right_half = gray[:, w // 2:].astype(float)
    left_mean = left_half.mean()
    right_mean = right_half.mean()
    balance_lr = 1.0 - abs(left_mean - right_mean) / 255.0

    top_half = gray[:h // 2, :].astype(float)
    bot_half = gray[h // 2:, :].astype(float)
    balance_tb = 1.0 - abs(top_half.mean() - bot_half.mean()) / 255.0

    balance = (balance_lr + balance_tb) / 2.0

    center_region = gray[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    focal = center_region.std() > 35

    score = min(90, int(hotspots * 12 + balance * 35 + (15 if focal else 0) + 20))

    rules = []
    if hotspots >= 2:
        rules.append("Rule of thirds")
    elif hotspots >= 1:
        rules.append("Partial rule of thirds")
    if balance > 0.7:
        rules.append("Well-balanced")
    elif balance > 0.5:
        rules.append("Reasonably balanced")
    if focal:
        rules.append("Strong focal point")

    return {
        "score": score,
        "rule": " + ".join(rules) if rules else "Consider rule of thirds",
        "feedback": f"Found {hotspots}/4 rule-of-thirds intersections. Balance: {balance:.0%}"
    }


def detect_faces(image: np.ndarray) -> dict:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    count = len(faces)

    if count == 0:
        score = 40
        feedback = "No faces detected. Human faces increase engagement 2-3x"
    elif count == 1:
        score = 85
        feedback = "Single face — strong focal point for connection"
    elif count <= 3:
        score = 70
        feedback = f"{count} faces detected — good social proof"
    else:
        score = 50
        feedback = f"{count} faces — may dilute focus"

    return {"score": score, "count": count, "feedback": feedback}


def detect_cta(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bottom_third = gray[int(h * 0.67):, :]
    edges = cv2.Canny(bottom_third, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    button_like = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        aspect = cw / max(ch, 1)
        if 1.5 < aspect < 6 and cw > w * 0.1 and ch > 10:
            button_like.append((x, y, cw, ch))

    if button_like:
        score = 80
        feedback = f"CTA-like element detected in bottom zone"
    else:
        score = 35
        feedback = "No clear CTA detected — add a button or text in lower third"

    return {"score": score, "text": "Button detected" if button_like else None, "feedback": feedback}


def analyze_visual_hierarchy(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

    zones = {
        "top-left": gray[:h // 3, :w // 3],
        "top-center": gray[:h // 3, w // 3:2 * w // 3],
        "top-right": gray[:h // 3, 2 * w // 3:],
        "mid-left": gray[h // 3:2 * h // 3, :w // 3],
        "center": gray[h // 3:2 * h // 3, w // 3:2 * w // 3],
        "mid-right": gray[h // 3:2 * h // 3, 2 * w // 3:],
        "bottom-left": gray[2 * h // 3:, :w // 3],
        "bottom-center": gray[2 * h // 3:, w // 3:2 * w // 3],
        "bottom-right": gray[2 * h // 3:, 2 * w // 3:],
    }

    attention = {k: float(v.mean() + v.std()) for k, v in zones.items()}
    sorted_zones = sorted(attention.items(), key=lambda x: -x[1])

    flow_parts = [z[0].replace("-", " → ").title() for z in sorted_zones[:3]]
    flow = " → ".join(flow_parts)

    top_heavy = sum(attention[k] for k in attention if "top" in k)
    bottom_heavy = sum(attention[k] for k in attention if "bottom" in k)

    if top_heavy > bottom_heavy * 1.3:
        feedback = "Top-heavy layout — good for headline-first reading"
    elif bottom_heavy > top_heavy * 1.3:
        feedback = "Bottom-heavy — ensure headline is visible above fold"
    else:
        feedback = "Balanced vertical distribution"

    score = min(90, max(30, int((top_heavy / (top_heavy + bottom_heavy + 1e-6)) * 80 + 20)))

    return {"score": score, "flow": flow, "feedback": feedback}


def _rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    else:
        h = (60 * ((r - g) / df) + 240) % 360
    s = 0 if mx == 0 else (df / mx) * 100
    v = mx * 100
    return h, s, v
