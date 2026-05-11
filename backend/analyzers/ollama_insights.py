import json
import base64
import urllib.request
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4"


def _call_gemma(prompt: str, image_bytes: bytes = None, timeout: int = 60) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 2000}
    }
    if image_bytes:
        payload["images"] = [base64.b64encode(image_bytes).decode("utf-8")]

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode()).get("response", "")


def _parse_json(text: str) -> dict:
    try:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
    except json.JSONDecodeError:
        pass
    return {}


def analyze_image(image_bytes: bytes) -> dict:
    prompt = """Analyze this advertisement image. Return ONLY a JSON object with these exact fields (no markdown, no explanation, just the JSON):

{
  "faces": {
    "count": <number of human faces visible>,
    "placement": "<where faces are: top-left, center, bottom-right, etc>"
  },
  "cta": {
    "present": <true/false - is there a clear call-to-action button or text like "Shop Now", "Buy Now", "Learn More", "Sign Up", "Order Now">,
    "text": "<exact CTA text if present, or empty string>",
    "placement": "<where CTA is: top, center, bottom-left, bottom-right, etc>"
  },
  "composition": {
    "rule_of_thirds": <true/false - do key elements align with rule-of-thirds grid>,
    "balance": "<left-heavy, right-heavy, top-heavy, bottom-heavy, or balanced>",
    "focal_point": "<what draws the eye first>"
  },
  "colors": {
    "dominant": ["<hex color 1>", "<hex color 2>", "<hex color 3>"],
    "mood": "<warm, cool, neutral, vibrant, muted>"
  },
  "text": {
    "headline": "<main headline text in the ad>",
    "body": "<body/description text>",
    "brand": "<brand name visible>",
    "all_text": "<all text combined>"
  },
  "copy_quality": {
    "score": <1-100>,
    "sentiment": "<positive, negative, neutral>",
    "emotion": "<primary emotion: urgency, trust, excitement, calm, luxury, value>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "weaknesses": ["<weakness 1>", "<weakness 2>"]
  },
  "overall_score": <1-100 how effective is this ad>,
  "eye_tracking": {
    "step1": "<what the eye sees first>",
    "step2": "<what the eye sees second>",
    "step3": "<what the eye sees third>",
    "step4": "<what the eye sees fourth>",
    "step5": "<what the eye sees last>"
  }
}

IMPORTANT: If there is NO call-to-action button or text like "Shop Now", "Buy", "Sign Up", set cta.present to false. Do NOT assume text overlays or headlines are CTAs. Only actual action buttons or action text count as CTAs."""

    response = _call_gemma(prompt, image_bytes)
    return _parse_json(response)


def generate_insights(analysis_data: dict) -> str:
    prompt = f"""You are an expert ad creative analyst. Based on this analysis data, give 3-4 actionable insights in plain English. Be direct and specific. No fluff.

Analysis Data:
{json.dumps(analysis_data, indent=2)}

Give your analysis as 3-4 short bullet points. Each should be one actionable sentence."""
    return _call_gemma(prompt, timeout=30)


def generate_video_insights(video_data: dict) -> str:
    prompt = f"""You are an expert cinematic ad analyst. Based on this video analysis, give 3-4 actionable insights. Be direct.

Video Scores:
{json.dumps(video_data, indent=2)}

Give 3-4 short actionable bullet points."""
    return _call_gemma(prompt, timeout=30)
