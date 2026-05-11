import os
import cv2
import numpy as np
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from analyzers.saliency import generate_heatmap, get_attention_description
from analyzers.creative_dna import (
    extract_colors, analyze_color_harmony, analyze_composition,
    detect_faces, detect_cta, analyze_visual_hierarchy,
)
from analyzers.copy_analyzer import analyze_copy
from analyzers.compliance import run_compliance_checks
from analyzers.scoring import compute_overall_score, compute_visual_score
from analyzers.video_analyzer import (
    extract_frames, compute_overall_video_score, detect_pacing,
)
from analyzers.ollama_insights import generate_insights, generate_video_insights, ocr_from_image

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
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    if isinstance(val, (np.bool_,)):
        return bool(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    return val


def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return to_native(obj)


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...), copy_text: str = ""):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)

    h, w = image.shape[:2]

    heatmap = generate_heatmap(image)
    attention_desc = get_attention_description(heatmap)
    heatmap_list = (heatmap * 255).astype(np.uint8).tolist()

    colors = extract_colors(image)
    colors_harmony = analyze_color_harmony(colors)
    composition = analyze_composition(image)
    faces = detect_faces(image)
    cta = detect_cta(image)
    visual_hierarchy = analyze_visual_hierarchy(image)

    creative_dna = {
        "colors": colors,
        "colors_harmony": colors_harmony,
        "typography": {
            "score": composition["score"],
            "style": "Detected text regions",
            "feedback": composition["feedback"],
        },
        "composition": composition,
        "faces": faces,
        "cta": cta,
        "visualHierarchy": visual_hierarchy,
    }

    compliance = run_compliance_checks(image)
    visual_score = compute_visual_score(image)

    ocr_text = ocr_from_image(contents)
    copy_input = copy_text.strip() if copy_text and copy_text.strip() else ocr_text

    if copy_input:
        copy_result = analyze_copy(headline="", body=copy_input, cta="")
    else:
        copy_result = analyze_copy(headline="", body="", cta="")

    scores = compute_overall_score(
        {"score": int(visual_score)},
        copy_result,
        creative_dna,
    )

    result = {
        "imageWidth": int(w),
        "imageHeight": int(h),
        "heatmap": heatmap_list,
        "attention": attention_desc,
        "extractedText": ocr_text,
        "creativeDNA": creative_dna,
        "copyAnalysis": copy_result,
        "compliance": compliance,
        "overallScore": scores["overallScore"],
        "visualScore": scores["visualScore"],
        "copyScore": scores["copyScore"],
        "ctaScore": scores["ctaScore"],
        "insights": scores["insights"],
    }

    ollama_context = {
        "overallScore": scores["overallScore"],
        "visualScore": scores["visualScore"],
        "copyScore": scores["copyScore"],
        "ctaScore": scores["ctaScore"],
        "sentiment": copy_result.get("sentiment"),
        "emotions": [e["emotion"] for e in copy_result.get("emotions", [])],
        "powerWords": copy_result.get("powerWords", []),
        "readability": copy_result.get("readability"),
        "topColors": [c["hex"] for c in colors[:3]],
        "faces": faces["count"] if isinstance(faces, dict) else len(faces),
        "composition": composition.get("rule"),
        "extractedText": ocr_text[:200] if ocr_text else "None",
    }
    ai_insights = generate_insights(ollama_context)
    result["aiInsights"] = ai_insights

    return sanitize(result)


@app.post("/api/analyze-copy")
async def analyze_copy_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")
    result = analyze_copy(headline=text[:100], body=text)
    return result


@app.post("/api/check-compliance")
async def check_compliance(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        return JSONResponse({"error": "Invalid image"}, status_code=400)
    return sanitize(run_compliance_checks(image))


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

        result = sanitize({
            **scores,
            "frames": frames,
            "motionData": motion_data,
            "aiInsights": ai_insights,
        })
        return result
    finally:
        tmp_path.unlink(missing_ok=True)


@app.get("/api/competitor-search")
async def competitor_search(q: str = Query(...)):
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
