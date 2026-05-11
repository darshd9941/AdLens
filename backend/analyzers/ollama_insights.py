import json
import base64
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4"


def ocr_from_image(image_bytes: bytes) -> str:
    """Use Gemma 4 vision to extract text from an image."""
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = "Extract ALL text from this image. Output only the text you see, nothing else. Preserve the original spacing and line breaks as much as possible."

    try:
        data = json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "images": [img_b64],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 1000}
        }).encode("utf-8")

        req = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "").strip()
    except Exception as e:
        return ""


def generate_insights(analysis_data: dict) -> str:
    """Use Gemma 4 to generate ad analysis insights."""
    prompt = f"""You are an expert ad creative analyst. Based on this analysis data, give 3-4 actionable insights in plain English. Be direct and specific. No fluff.

Analysis Data:
- Overall Score: {analysis_data.get('overallScore', 'N/A')}/100
- Visual Score: {analysis_data.get('visualScore', 'N/A')}/100
- Copy Score: {analysis_data.get('copyScore', 'N/A')}/100
- CTA Score: {analysis_data.get('ctaScore', 'N/A')}/100
- Sentiment: {analysis_data.get('sentiment', 'N/A')}
- Emotions: {analysis_data.get('emotions', 'None detected')}
- Power Words: {analysis_data.get('powerWords', 'None')}
- Readability: {analysis_data.get('readability', 'N/A')}
- Colors: {analysis_data.get('topColors', 'N/A')}
- Faces Detected: {analysis_data.get('faces', 'N/A')}
- Composition: {analysis_data.get('composition', 'N/A')}
- Extracted Text: {analysis_data.get('extractedText', 'None')}

Give your analysis as 3-4 short bullet points. Each should be one actionable sentence."""

    try:
        data = json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.4, "num_predict": 500}
        }).encode("utf-8")

        req = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "Could not generate insights.")
    except Exception as e:
        return f"Ollama not available ({e}). Start Ollama and try again."


def generate_video_insights(video_data: dict) -> str:
    """Use Gemma 4 to generate video analysis insights."""
    prompt = f"""You are an expert cinematic ad analyst. Based on this video analysis, give 3-4 actionable insights. Be direct.

Video Scores:
- Overall: {video_data.get('overallScore', 'N/A')}/100
- Composition: {video_data.get('compositionScore', 'N/A')}/100
- Color Grading: {video_data.get('colorScore', 'N/A')}/100
- Lighting: {video_data.get('lightingScore', 'N/A')}/100
- Motion: {video_data.get('motionScore', 'N/A')}/100
- Pacing: {video_data.get('pacingScore', 'N/A')}/100
- Detected Cuts: {video_data.get('cuts', 'N/A')}
- Pacing Type: {video_data.get('pacingType', 'N/A')}

Give 3-4 short actionable bullet points."""

    try:
        data = json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.4, "num_predict": 500}
        }).encode("utf-8")

        req = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "Could not generate insights.")
    except Exception as e:
        return f"Ollama not available ({e})."
