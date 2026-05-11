# AdLens — AI Creative Intelligence Platform

> Free, local-first ad creative analyzer powered by Gemma 4 vision. Analyze static ads and videos with attention heatmaps, eye tracking, copy analysis, Indian market simulations, and AI-generated insights. No signup. No API keys. Runs on your machine.

---

## What It Does

Upload any ad creative (image or video). AdLens analyzes it using **Gemma 4 multimodal AI** and gives you a complete breakdown:

- **Where eyes go** on your ad (heatmap + 5-step eye tracking path)
- **What Gemma sees** — faces, CTA, composition, colors, text, mood
- **How good your copy is** — sentiment, emotion, power words, readability
- **Performance score** — 1-100 rating before you spend a rupee
- **India market simulation** — predicted CTR, CPM, ROAS, likes, comments for your industry and budget
- **A/B test suggestions** — specific to your ad's weak spots
- **Best posting times** — IST schedule optimized for your industry

---

## Demo

### Eye Tracking Overlay
Upload an ad → Gemma 4 identifies where eyes go in order:

```
1. The woman (human element)
2. The bedding/throw blanket (the product)
3. The headline text
4. The background setting
5. The brand logo
```

Numbered circles with arrows overlaid on the image. Toggle on/off.

### Attention Heatmap
Blue (low) → Green → Yellow → Red (hot attention zones). Generated using spectral residual FFT + face detection + contrast analysis.

### India Market Simulation
Select industry (Fashion, E-commerce, Food, etc.) → set daily budget in ₹ → get:

| Metric | What You Get |
|--------|-------------|
| CTR | Predicted click-through rate |
| CPM | Cost per 1000 impressions |
| CPC | Cost per click |
| ROAS | Return on ad spend |
| Daily | Impressions, clicks, likes, comments, shares, saves, conversions, revenue |
| Monthly | Scaled to 30 days |
| Platforms | Facebook Feed vs Instagram Reels vs Stories — CTR/CPM for each |
| Best times | Peak posting hours IST with scores |

---

## Features

### Static Ad Analysis
- **Gemma 4 Vision** — reads the entire image: faces, CTA, composition, colors, text, mood
- **Eye Tracking Path** — 5-step numbered overlay showing gaze order
- **Attention Heatmap** — pixel-level saliency map overlay
- **OCR Text Extraction** — Gemma reads all text from the ad automatically
- **Copy Analysis** — VADER sentiment + textstat readability + emotion detection
- **Color Palette** — extracted dominant colors with hex codes
- **Compliance Check** — resolution, aspect ratio, text-to-image ratio
- **Performance Score** — overall, visual, copy, CTA scores (1-100)
- **AI Insights** — Gemma generates plain-English recommendations

### Cinematic Video Analysis
- Frame-by-frame composition scoring
- Color grading consistency analysis
- Lighting quality metrics
- Motion energy visualization
- Pacing and cut detection

### India Market Simulation
- 9 industry benchmarks (E-commerce, Fashion, Education, Food, SaaS, Real Estate, Health, Local Business)
- Daily budget input in ₹
- Platform-level breakdown (Facebook, Instagram, Audience Network)
- A/B test suggestions based on your ad's weaknesses
- Best posting times IST
- Daily and monthly projections

### Competitor Intelligence
- Search Meta Ads Library for competitor creatives
- View active ads by brand or domain

---

## How to Install

### Prerequisites
- **Python 3.10+** — [Download](https://python.org)
- **Node.js 18+** — [Download](https://nodejs.org)
- **Ollama** — [Download](https://ollama.ai) with `gemma4` model loaded

### 1. Install Ollama and Gemma 4

```bash
# Install Ollama from https://ollama.ai

# Pull Gemma 4 model
ollama pull gemma4
```

### 2. Clone and Start

```bash
git clone https://github.com/darshd9941/AdLens.git
cd AdLens
```

**Windows (one click):**
```cmd
start.bat
```

**Manual start:**
```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python server.py

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

### 3. Open

Go to **http://localhost:3000**

---

## How to Use

### Analyze a Static Ad
1. Go to **Analyze Ad** in the sidebar
2. Drag and drop your ad image (JPG, PNG, WebP)
3. Gemma 4 reads the image — extracts text, identifies faces, CTA, composition
4. View results:
   - **Heatmap tab** — attention zones overlaid on image
   - **Eye Tracking tab** — 5-step numbered gaze path with arrows
   - **Scores** — Overall, Visual, Copy, CTA (1-100)
   - **Creative DNA** — colors, composition, faces, CTA, typography
   - **Copy Analysis** — sentiment, emotion, power words, suggestions
   - **Gemma AI Insights** — plain-English recommendations
5. Scroll down to **India Market Simulation**:
   - Select your industry
   - Set daily budget in ₹
   - Click **Run Simulation**
   - See predicted CTR, CPM, ROAS, daily/monthly estimates, platform breakdown, A/B tests, posting schedule

### Analyze a Video
1. Go to **Video Analysis** in the sidebar
2. Upload an MP4/MOV video
3. Get frame-by-frame composition, color, lighting, motion, and pacing scores

### Competitor Spy
1. Go to **Competitor Spy** in the sidebar
2. Search for a brand name
3. View their active ads on Meta Ads Library

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React, TailwindCSS, Vite | UI, overlays, heatmaps |
| Backend | Python, FastAPI | API server |
| Vision AI | **Gemma 4** via Ollama | Image understanding, OCR, insights |
| NLP | VADER, textstat | Sentiment, readability |
| Computer Vision | OpenCV | Heatmap generation, face detection |
| Color Analysis | scikit-learn (K-Means) | Palette extraction |

### AI Models Used
- **Gemma 4** (via Ollama) — multimodal vision for ad analysis, text extraction, face/CTA detection, copy scoring, insight generation
- **Spectral Residual FFT** — attention heatmap prediction (no training data needed)
- **VADER Sentiment** — rule-based sentiment analysis tuned for social media
- **Flesch-Kincaid** (via textstat) — readability scoring
- **Haar Cascade** — face detection fallback

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/analyze-image` | POST | Full Gemma 4 vision analysis |
| `/api/simulate` | POST | India market simulation |
| `/api/analyze-video` | POST | Video analysis |
| `/api/competitor-search` | GET | Search Meta Ads Library |

---

## Project Structure

```
AdLens/
├── frontend/                    React + Tailwind + Vite
│   └── src/
│       ├── components/
│       │   ├── Layout.jsx           Sidebar + navigation
│       │   ├── UploadZone.jsx       Drag-and-drop upload
│       │   ├── ScoreCard.jsx        Score display with color coding
│       │   ├── HeatmapOverlay.jsx   Canvas-based heatmap rendering
│       │   ├── EyeTrackingOverlay.jsx   Numbered gaze path overlay
│       │   └── SimulationPanel.jsx  India market simulation UI
│       └── pages/
│           ├── Home.jsx             Landing page
│           ├── StaticAnalysis.jsx   Main ad analysis page
│           ├── VideoAnalysis.jsx    Video analysis page
│           └── CompetitorInsights.jsx   Competitor spy page
├── backend/                     FastAPI + OpenCV
│   ├── server.py                API routes
│   ├── requirements.txt         Python dependencies
│   └── analyzers/
│       ├── saliency.py          Attention heatmap (spectral residual FFT)
│       ├── ollama_insights.py   Gemma 4 integration (vision + text)
│       ├── copy_analyzer.py     VADER sentiment + textstat readability
│       ├── scoring.py           Performance scoring
│       ├── simulation.py        India market simulation
│       ├── video_analyzer.py    Video frame analysis
│       └── compliance.py        Ad compliance checks
├── start.bat                    One-click launcher (Windows)
├── stop.bat                     Stop all servers
└── README.md
```

---

## Requirements

```
# Backend (Python)
fastapi
uvicorn
python-multipart
opencv-python-headless
numpy
Pillow
scikit-learn
vaderSentiment
textstat
easyocr

# Frontend (Node.js)
react
react-dom
react-router-dom
tailwindcss
d3
axios
lucide-react

# AI (Ollama)
gemma4
```

---

## Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/new-feature`)
3. Commit (`git commit -m 'Add new feature'`)
4. Push (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## License

MIT

---

## Credits

Built with Gemma 4, OpenCV, VADER, and FastAPI. Runs 100% locally.
