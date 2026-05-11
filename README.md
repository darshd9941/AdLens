# AdLens — AI Creative Intelligence Platform

Free, local-first ad creative analyzer with AI-powered attention heatmaps, creative DNA decomposition, and cinematic video analysis. No signup required.

## Features

### Static Ad Analysis
- **AI Attention Heatmap** — Predicts where eyes go on your ad using saliency models, face detection, and text region analysis
- **Creative DNA Decomposition** — Breaks your ad into atomic elements: color palette, typography, composition, faces, CTA placement
- **Ad Copy Analysis** — Sentiment, emotion detection, power words, readability scoring, and actionable suggestions
- **Performance Score** — Predicts ad effectiveness 1-100 before you spend a dollar
- **Compliance Checker** — Text-to-image ratio, resolution, aspect ratio, forbidden words

### Cinematic Video Analysis
- Frame-by-frame composition scoring (rule of thirds, symmetry, balance)
- Color grading consistency analysis
- Lighting quality metrics
- Motion energy visualization
- Pacing and cut detection
- Story arc mapping

### Competitor Intelligence
- Search Meta Ads Library for competitor creatives
- View active ads by brand or domain
- Side-by-side comparison

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Clone
```bash
git clone https://github.com/darshd9941/AdLens.git
cd AdLens
```

### 2. Start (Windows)
```cmd
start.bat
```

### 3. Start (Manual)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python server.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TailwindCSS, D3.js, Vite |
| Backend | Python, FastAPI, OpenCV |
| AI/ML | OpenCV Saliency, Face Detection, K-Means Color Clustering |
| Video | OpenCV Frame Extraction, Motion Analysis |

## How the Heatmap Works

```
Image Input
    │
    ├── Saliency Map (Spectral Residual) → Where AI predicts eyes go
    ├── Face Detection (Haar Cascade) → Faces = high attention zones
    ├── Text Region Detection → Readable text attracts fixations
    ├── Contrast/Edge Analysis → High-contrast areas = attention magnets
    │
    └── Fusion (Weighted) → Final attention heatmap overlay
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/analyze-image` | POST | Full static ad analysis with heatmap |
| `/api/analyze-copy` | POST | Text/copy analysis |
| `/api/check-compliance` | POST | Ad compliance checks |
| `/api/analyze-video` | POST | Cinematic video analysis |
| `/api/competitor-search` | GET | Search Meta Ads Library |

## Project Structure

```
AdLens/
├── frontend/            React + Tailwind + D3
│   └── src/
│       ├── components/  HeatmapOverlay, CreativeDNA, CopyAnalysis, ScoreCard
│       └── pages/       Home, StaticAnalysis, VideoAnalysis, CompetitorInsights
├── backend/             FastAPI + OpenCV
│   ├── server.py        API routes
│   └── analyzers/       saliency, creative_dna, copy_analyzer, compliance, scoring, video
├── start.bat            One-click launcher
└── README.md
```

## License

MIT
