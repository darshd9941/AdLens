import cv2
import numpy as np
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from analyzers.saliency import generate_heatmap, get_attention_description
from analyzers.ollama_insights import analyze_image, generate_insights, generate_video_insights
from analyzers.video_analyzer import extract_frames, compute_overall_video_score, detect_pacing
from analyzers.simulation import simulate_india_performance, generate_ab_tests, get_best_posting_times, generate_report

app = FastAPI(title="AdLens API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def to_native(val):
    if hasattr(val, 'item'):
        return val.item()
    if isinstance(val, dict):
        return {k: to_native(v) for k, v in val.items()}
    if isinstance(val, list):
        return [to_native(v) for v in val]
    return val


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)

    h, w = image.shape[:2]

    heatmap = generate_heatmap(image)
    attention_desc = get_attention_description(heatmap)
    heatmap_list = (heatmap * 255).astype(np.uint8).tolist()

    gemma_result = analyze_image(contents)

    if not gemma_result:
        return JSONResponse({"error": "Gemma could not analyze this image. Make sure Ollama is running with gemma4 loaded."}, status_code=500)

    faces_data = gemma_result.get("faces", {"count": 0, "placement": "unknown"})
    cta_data = gemma_result.get("cta", {"present": False, "text": "", "placement": "none"})
    composition = gemma_result.get("composition", {})
    colors = gemma_result.get("colors", {})
    text_data = gemma_result.get("text", {})
    copy_quality = gemma_result.get("copy_quality", {})
    eye_tracking = gemma_result.get("eye_tracking", {})

    face_count = faces_data.get("count", 0)
    if face_count == 0:
        face_score = 40
        face_feedback = "No faces detected"
    elif face_count == 1:
        face_score = 85
        face_feedback = f"1 face at {faces_data.get('placement', 'unknown')} — strong focal point"
    elif face_count <= 3:
        face_score = 70
        face_feedback = f"{face_count} faces — good social proof"
    else:
        face_score = 50
        face_feedback = f"{face_count} faces — may dilute focus"

    cta_present = cta_data.get("present", False)
    cta_score = 75 if cta_present else 20
    cta_feedback = f"CTA: \"{cta_data.get('text', '')}\" at {cta_data.get('placement', 'none')}" if cta_present else "No clear CTA detected — add a button or action text"

    overall_score = gemma_result.get("overall_score", 50)
    copy_score = copy_quality.get("score", 50)

    creative_dna = {
        "colors": [
            {"hex": c, "percentage": round(100 / max(len(colors.get("dominant", ["#888888"])), 1), 1)}
            for c in colors.get("dominant", ["#888888"])
        ],
        "colors_harmony": {
            "score": 70 if colors.get("mood") in ["warm", "cool", "vibrant"] else 40,
            "feedback": f"Color mood: {colors.get('mood', 'unknown')}"
        },
        "typography": {
            "score": 70 if text_data.get("headline") else 30,
            "style": text_data.get("headline", "No headline detected"),
            "feedback": f"Brand: {text_data.get('brand', 'Unknown')}"
        },
        "composition": {
            "score": 75 if composition.get("rule_of_thirds") else 45,
            "rule": f"{'Rule of thirds' if composition.get('rule_of_thirds') else 'No rule of thirds'} + {composition.get('balance', 'unknown')}",
            "feedback": f"Focal point: {composition.get('focal_point', 'unknown')}"
        },
        "faces": {
            "score": face_score,
            "count": face_count,
            "feedback": face_feedback
        },
        "cta": {
            "score": cta_score,
            "text": cta_data.get("text"),
            "feedback": cta_feedback
        },
        "visualHierarchy": {
            "score": 60,
            "flow": " → ".join([eye_tracking.get(f"step{i}", "") for i in range(1, 6) if eye_tracking.get(f"step{i}")]),
            "feedback": f"Balance: {composition.get('balance', 'unknown')}"
        },
    }

    copy_result = {
        "headline": text_data.get("headline", ""),
        "bodyText": text_data.get("body", "") or text_data.get("all_text", ""),
        "charCount": len(text_data.get("all_text", "")),
        "sentiment": copy_quality.get("sentiment", "Neutral"),
        "sentimentScore": 70 if copy_quality.get("sentiment") == "positive" else 30 if copy_quality.get("sentiment") == "negative" else 50,
        "primaryEmotion": copy_quality.get("emotion", "Neutral"),
        "emotions": [{"emotion": copy_quality.get("emotion", "neutral"), "triggers": [], "strength": 1}] if copy_quality.get("emotion") else [],
        "powerWords": [],
        "readability": "Auto-analyzed by Gemma 4",
        "readabilityScore": copy_quality.get("score", 50),
        "suggestions": copy_quality.get("strengths", []) + [f"Fix: {w}" for w in copy_quality.get("weaknesses", [])],
        "copyScore": copy_score,
    }

    eye_path = []
    for i in range(1, 6):
        step = eye_tracking.get(f"step{i}")
        if step:
            eye_path.append(step)

    result = to_native({
        "imageWidth": w,
        "imageHeight": h,
        "heatmap": heatmap_list,
        "attention": attention_desc,
        "extractedText": text_data.get("all_text", ""),
        "creativeDNA": creative_dna,
        "copyAnalysis": copy_result,
        "overallScore": overall_score,
        "visualScore": copy_score,
        "copyScore": copy_score,
        "ctaScore": cta_score,
        "eyeTracking": eye_path,
        "insights": copy_quality.get("strengths", []),
    })

    ollama_context = {
        "overallScore": overall_score,
        "visualScore": copy_score,
        "copyScore": copy_score,
        "ctaScore": cta_score,
        "sentiment": copy_quality.get("sentiment"),
        "emotion": copy_quality.get("emotion"),
        "colors": colors.get("dominant"),
        "faces": face_count,
        "composition": composition.get("balance"),
        "cta": cta_data.get("text") if cta_present else "None",
        "extractedText": text_data.get("all_text", "")[:200],
    }
    result["aiInsights"] = generate_insights(ollama_context)

    return result


@app.post("/api/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    contents = await file.read()
    ext = Path(file.filename).suffix or ".mp4"
    tmp_path = UPLOAD_DIR / f"tmp{ext}"
    tmp_path.write_bytes(contents)

    try:
        frames = extract_frames(str(tmp_path), max_frames=15)
        scores = compute_overall_video_score(frames)
        pacing = detect_pacing(frames)
        motion_data = [float(f["score"]) / 100.0 for f in frames]

        video_context = {
            **scores,
            "cuts": pacing.get("cuts", 0),
            "pacingType": pacing.get("pacing", "N/A"),
        }
        ai_insights = generate_video_insights(video_context)

        result = to_native({
            **scores,
            "frames": frames,
            "motionData": motion_data,
            "aiInsights": ai_insights,
        })
        return result
    finally:
        tmp_path.unlink(missing_ok=True)


@app.post("/api/simulate")
async def simulate(
    overallScore: int = 50,
    copyScore: int = 50,
    ctaScore: int = 50,
    visualScore: int = 50,
    industry: str = "default",
    dailyBudget: int = 1000,
    extractedText: str = "",
):
    analysis = {
        "overallScore": overallScore,
        "copyScore": copyScore,
        "ctaScore": ctaScore,
        "visualScore": visualScore,
        "extractedText": extractedText,
    }
    simulation = simulate_india_performance(analysis, industry, dailyBudget)
    ab_tests = generate_ab_tests(analysis)
    posting = get_best_posting_times(industry)
    report = generate_report(simulation, simulation, ab_tests, posting)
    return to_native({
        "simulation": simulation,
        "abTests": ab_tests,
        "postingSchedule": posting,
        "report": report,
    })


@app.get("/api/competitor-search")
async def competitor_search(q: str = ""):
    page_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={q}"
    ads = [{
        "pageName": f"Results for '{q}'",
        "headline": "View on Meta Ads Library",
        "body": f"Click to see all active ads for '{q}' on Meta's public Ads Library.",
        "libraryUrl": page_url,
        "startDate": "Active",
        "platforms": ["Facebook", "Instagram"],
        "thumbnail": None,
    }]
    return {"query": q, "ads": ads}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
