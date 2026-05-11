import numpy as np
from PIL import Image


def check_text_to_image_ratio(image: np.ndarray) -> dict:
    gray = __import__("cv2").cvtColor(image, __import__("cv2").COLOR_BGR2GRAY)
    _, binary = __import__("cv2").threshold(gray, 200, 255, __import__("cv2").THRESH_BINARY)

    total_pixels = binary.shape[0] * binary.shape[1]
    text_pixels = int(np.sum(binary == 255))
    ratio = (text_pixels / total_pixels) * 100

    return {
        "rule": "Text-to-image ratio (20% rule)",
        "pass": bool(ratio <= 20),
        "detail": f"{ratio:.1f}% text coverage",
        "warning": f"Text covers {ratio:.1f}% — exceeds Meta's 20% guideline" if ratio > 20 else None
    }


def check_resolution(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    min_dim = min(h, w)

    if min_dim < 600:
        return {
            "rule": "Minimum resolution",
            "pass": False,
            "detail": f"{w}x{h} — below 600px minimum"
        }
    return {
        "rule": "Minimum resolution",
        "pass": True,
        "detail": f"{w}x{h}"
    }


def check_aspect_ratio(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    ratio = w / h
    valid_ratios = [1.0, 4 / 3, 16 / 9, 9 / 16, 4 / 5]

    closest = min(valid_ratios, key=lambda r: abs(r - ratio))
    is_valid = abs(ratio - closest) < 0.1

    labels = {1.0: "1:1", 4/3: "4:3", 16/9: "16:9", 9/16: "9:16", 4/5: "4:5"}

    return {
        "rule": "Aspect ratio check",
        "pass": is_valid,
        "detail": f"Detected {ratio:.2f}:1 (closest standard: {labels.get(closest, 'N/A')})"
    }


def check_forbidden_words(text: str) -> dict:
    forbidden = [
        "guaranteed", "cure", "miracle", "instant weight loss",
        "clickbait", "act now or miss", "you've been selected",
    ]
    lower = text.lower()
    found = [w for w in forbidden if w in lower]

    return {
        "rule": "Forbidden/clickbait words",
        "pass": bool(len(found) == 0),
        "detail": f"Found: {', '.join(found)}" if found else "None detected"
    }


def check_brand_elements(image: np.ndarray) -> dict:
    h, w = image.shape[:2]
    gray = __import__("cv2").cvtColor(image, __import__("cv2").COLOR_BGR2GRAY)

    lower_region = gray[int(h * 0.7):, :]
    upper_region = gray[:int(h * 0.3), :]

    lower_edge = float(__import__("cv2").Canny(lower_region, 50, 150).mean())
    upper_edge = float(__import__("cv2").Canny(upper_region, 50, 150).mean())

    has_lower_focal = lower_edge > 10
    has_upper_content = upper_edge > 10

    return {
        "rule": "Layout structure",
        "pass": bool(has_lower_focal or has_upper_content),
        "detail": "Content distributed across zones" if (has_lower_focal and has_upper_content)
                   else "Consider adding content to " + ("upper" if not has_upper_content else "lower") + " zone"
    }


def run_compliance_checks(image: np.ndarray, text: str = "") -> dict:
    checks = [
        check_text_to_image_ratio(image),
        check_resolution(image),
        check_aspect_ratio(image),
        check_brand_elements(image),
    ]

    if text:
        checks.append(check_forbidden_words(text))

    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "score": int(passed / total * 100),
    }
