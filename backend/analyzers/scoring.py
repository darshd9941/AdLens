import cv2
import numpy as np


def compute_visual_score(image: np.ndarray) -> int:
    h, w = image.shape[:2]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_ch, s_ch, v_ch = cv2.split(hsv)

    brightness = float(v_ch.mean()) / 255.0
    brightness_score = 1.0 - abs(brightness - 0.55) * 2

    saturation = float(s_ch.mean()) / 255.0
    saturation_score = min(1.0, saturation * 2.5)

    contrast = float(v_ch.std()) / 128.0
    contrast_score = min(1.0, contrast)

    hist = cv2.calcHist([v_ch], [0], None, [256], [0, 256])
    hist = hist / hist.sum()
    shadows = float(hist[:85].sum())
    midtones = float(hist[85:170].sum())
    highlights = float(hist[170:].sum())
    dynamic_range = 1.0 if (shadows > 0.05 and highlights > 0.05) else 0.5

    hsv_hist_h = cv2.calcHist([h_ch], [0], None, [12], [0, 180])
    hsv_hist_h = hsv_hist_h / (hsv_hist_h.sum() + 1e-6)
    color_diversity = -float(np.sum(hsv_hist_h * np.log(hsv_hist_h + 1e-10)))
    color_score = min(1.0, color_diversity / 2.0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = float(laplacian.var())
    sharpness_score = min(1.0, sharpness / 2000.0)

    score = int(
        brightness_score * 20 +
        saturation_score * 15 +
        contrast_score * 20 +
        dynamic_range * 15 +
        color_score * 15 +
        sharpness_score * 15
    )

    return max(15, min(95, score))


def compute_overall_score(visual: dict, copy: dict, dna: dict) -> dict:
    scores = {
        "visual": visual.get("score", 50),
        "copy": copy.get("copyScore", 50),
        "cta": dna.get("cta", {}).get("score", 50),
        "composition": dna.get("composition", {}).get("score", 50),
        "hierarchy": dna.get("visualHierarchy", {}).get("score", 50),
        "colors": dna.get("colors_harmony", {}).get("score", 50),
    }

    weights = {
        "visual": 0.25,
        "copy": 0.20,
        "cta": 0.15,
        "composition": 0.15,
        "hierarchy": 0.15,
        "colors": 0.10,
    }

    overall = sum(scores[k] * weights[k] for k in scores)
    overall = min(95, max(10, int(overall)))

    insights = []
    if scores["cta"] < 50:
        insights.append("Your CTA is weak. Add a clear button or text like 'Shop Now' or 'Get Started' in the bottom third.")
    if scores["composition"] < 50:
        insights.append("Composition could be improved. Align key elements to rule-of-thirds grid intersections.")
    if scores["colors"] < 50:
        insights.append("Color harmony is low. Use analogous colors (next to each other on the color wheel) for cohesion.")
    if scores["visual"] > 75:
        insights.append("Strong visual appeal. Your creative quality is above average.")
    if scores["copy"] > 75:
        insights.append("Excellent copy. Good use of emotion and power words.")
    if scores["hierarchy"] < 50:
        insights.append("Visual hierarchy is unclear. Guide the eye from headline → image → CTA.")
    if not insights:
        if overall >= 70:
            insights.append("Solid ad overall. Consider A/B testing minor variations to optimize further.")
        else:
            insights.append("This ad needs work. Focus on the weakest scoring elements first.")

    return {
        "overallScore": overall,
        "visualScore": scores["visual"],
        "copyScore": scores["copy"],
        "ctaScore": scores["cta"],
        "insights": insights,
        "breakdown": scores,
    }
