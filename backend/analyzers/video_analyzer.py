import cv2
import numpy as np
import base64
import io


def extract_frames(video_path: str, max_frames: int = 20) -> list:
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if total_frames <= 0:
        cap.release()
        return []

    step = max(1, total_frames // max_frames)
    frames = []

    for i in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            timestamp = f"{i / fps:.1f}s"
            thumb = cv2.resize(frame, (160, 90))
            _, buf = cv2.imencode(".jpg", thumb, [cv2.IMWRITE_JPEG_QUALITY, 60])
            thumb_b64 = "data:image/jpeg;base64," + base64.b64encode(buf).decode()

            composition_score = _analyze_frame_composition(frame)
            color_score = _analyze_frame_colors(frame)
            lighting_score = _analyze_frame_lighting(frame)

            avg_score = int((composition_score + color_score + lighting_score) / 3)

            frames.append({
                "index": i,
                "timestamp": timestamp,
                "thumbnail": thumb_b64,
                "score": avg_score,
                "composition": composition_score,
                "colors": color_score,
                "lighting": lighting_score,
            })

        if len(frames) >= max_frames:
            break

    cap.release()
    return frames


def _analyze_frame_composition(frame: np.ndarray) -> int:
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    thirds_h = [h // 3, 2 * h // 3]
    thirds_w = [w // 3, 2 * w // 3]
    hotspots = 0
    for th in thirds_h:
        for tw in thirds_w:
            region = edges[max(0, th - 15):th + 15, max(0, tw - 15):tw + 15]
            if region.mean() > 25:
                hotspots += 1

    center = gray[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    center_std = center.std()
    symmetry = 1.0 - abs(float(gray[:, :w // 2].mean()) - float(gray[:, w // 2:].mean())) / 128.0
    symmetry = max(0, min(1, symmetry))

    score = min(95, max(20, int(hotspots * 12 + symmetry * 30 + center_std * 0.3 + 15)))
    return score


def _analyze_frame_colors(frame: np.ndarray) -> int:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    sat_mean = s.mean()
    val_mean = v.mean()

    hist_h = cv2.calcHist([h], [0], None, [12], [0, 180])
    hist_h = hist_h / hist_h.sum()
    diversity = -np.sum(hist_h * np.log(hist_h + 1e-10))
    diversity_norm = min(1.0, diversity / 2.0)

    score = min(95, max(20, int(
        sat_mean / 255 * 30 +
        val_mean / 255 * 25 +
        diversity_norm * 25 +
        15
    )))
    return score


def _analyze_frame_lighting(frame: np.ndarray) -> int:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist / hist.sum()

    mean_brightness = gray.mean()
    contrast = gray.std()

    shadows = hist[:85].sum()
    midtones = hist[85:170].sum()
    highlights = hist[170:].sum()

    has_full_range = shadows > 0.1 and highlights > 0.1

    score = min(95, max(20, int(
        (1 - abs(mean_brightness - 128) / 128) * 30 +
        min(contrast / 80, 1) * 30 +
        (15 if has_full_range else 5) +
        10
    )))
    return score


def compute_motion_data(frames: list) -> list:
    if len(frames) < 2:
        return [0.5] * 10

    scores = [f["score"] for f in frames]
    max_s = max(scores) if max(scores) > 0 else 1
    normalized = [s / max_s for s in scores]
    return normalized


def detect_pacing(frames: list) -> dict:
    if len(frames) < 2:
        return {"score": 50, "avgShotLength": "N/A", "cuts": 0}

    scores = [f["score"] for f in frames]
    diffs = [abs(scores[i + 1] - scores[i]) for i in range(len(scores) - 1)]
    avg_diff = np.mean(diffs)
    cuts = sum(1 for d in diffs if d > 15)

    if avg_diff > 20:
        pacing = "Dynamic — fast cuts and variety"
        score = 80
    elif avg_diff > 10:
        pacing = "Moderate — balanced transitions"
        score = 65
    else:
        pacing = "Static — minimal visual change"
        score = 40

    return {
        "score": score,
        "pacing": pacing,
        "cuts": cuts,
        "avgDiff": float(avg_diff),
    }


def compute_overall_video_score(frames: list) -> dict:
    if not frames:
        return {"overallScore": 50, "compositionScore": 50, "colorScore": 50,
                "lightingScore": 50, "motionScore": 50, "pacingScore": 50, "insights": []}

    comp = np.mean([f["composition"] for f in frames])
    colors = np.mean([f["colors"] for f in frames])
    lighting = np.mean([f["lighting"] for f in frames])
    pacing = detect_pacing(frames)
    motion = np.mean(compute_motion_data(frames)) * 100

    overall = int(comp * 0.25 + colors * 0.20 + lighting * 0.20 + pacing["score"] * 0.15 + motion * 0.20)
    overall = min(95, max(15, overall))

    insights = []
    if comp < 50:
        insights.append("Composition is weak across frames — rule-of-thirds alignment is inconsistent")
    if colors < 50:
        insights.append("Color grading lacks cohesion — consider a consistent LUT or color palette")
    if lighting < 50:
        insights.append("Lighting is flat or inconsistent — add contrast with directional light")
    if pacing["score"] < 50:
        insights.append("Pacing is too static — add more dynamic transitions or motion")
    if overall > 75:
        insights.append("Strong cinematic quality across all dimensions")
    if not insights:
        insights.append("Good baseline — focus on weakest dimension for next iteration")

    return {
        "overallScore": overall,
        "compositionScore": int(comp),
        "colorScore": int(colors),
        "lightingScore": int(lighting),
        "motionScore": int(motion),
        "pacingScore": pacing["score"],
        "insights": insights,
    }
