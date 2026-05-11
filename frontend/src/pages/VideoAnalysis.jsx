import { useState } from 'react'
import { Loader2, Play, RotateCcw } from 'lucide-react'
import UploadZone from '../components/UploadZone'
import ScoreCard from '../components/ScoreCard'
import { uploadVideo } from '../utils/api'

function FrameTimeline({ frames }) {
  if (!frames || frames.length === 0) return null
  return (
    <div className="bg-surface border border-border rounded-xl p-4">
      <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Frame Timeline</h4>
      <div className="flex gap-1 overflow-x-auto pb-2">
        {frames.map((f, i) => (
          <div key={i} className="shrink-0 text-center">
            <div className="w-20 h-14 bg-surface-2 rounded-lg border border-border overflow-hidden mb-1">
              {f.thumbnail && (
                <img src={f.thumbnail} alt={`Frame ${i}`} className="w-full h-full object-cover" />
              )}
            </div>
            <span className="text-[10px] text-muted">{f.timestamp}</span>
            <div className="mt-0.5">
              <span className={`text-[10px] font-bold ${f.score >= 70 ? 'text-green' : f.score >= 50 ? 'text-yellow' : 'text-red'}`}>
                {f.score}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function MotionGraph({ data }) {
  if (!data) return null
  return (
    <div className="bg-surface border border-border rounded-xl p-4">
      <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Motion Energy</h4>
      <svg viewBox="0 0 400 80" className="w-full h-20">
        <defs>
          <linearGradient id="motionGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6366f1" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
          </linearGradient>
        </defs>
        {data.length > 1 && (
          <>
            <path
              d={`M0,80 ${data.map((v, i) => `L${(i / (data.length - 1)) * 400},${80 - v * 70}`).join(' ')} L400,80 Z`}
              fill="url(#motionGrad)"
            />
            <polyline
              points={data.map((v, i) => `${(i / (data.length - 1)) * 400},${80 - v * 70}`).join(' ')}
              fill="none"
              stroke="#6366f1"
              strokeWidth="2"
            />
          </>
        )}
      </svg>
    </div>
  )
}

export default function VideoAnalysis() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [preview, setPreview] = useState(null)

  const handleFile = async (file) => {
    setPreview(URL.createObjectURL(file))
    setLoading(true)
    setResult(null)
    try {
      const res = await uploadVideo(file)
      setResult(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  if (!preview) {
    return (
      <div className="p-8 max-w-2xl mx-auto">
        <h2 className="text-xl font-bold mb-1">Cinematic Video Analysis</h2>
        <p className="text-sm text-muted mb-6">Upload a video ad for frame-by-frame cinematic analysis</p>
        <UploadZone onFile={handleFile} accept="video/*" label="Drop your video ad here" />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Video Analysis Results</h2>
        <button
          onClick={() => { setPreview(null); setResult(null) }}
          className="px-3 py-1.5 text-xs bg-surface border border-border rounded-lg hover:bg-surface-2 flex items-center gap-1.5"
        >
          <RotateCcw className="w-3 h-3" /> New Upload
        </button>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-8 h-8 text-accent animate-spin mb-3" />
          <p className="text-sm text-muted">Analyzing video frames...</p>
        </div>
      ) : result ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-surface border border-border rounded-xl p-4">
              <video src={preview} controls className="w-full rounded-lg" />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <ScoreCard label="Overall" score={result.overallScore} />
              <ScoreCard label="Composition" score={result.compositionScore} />
              <ScoreCard label="Color Grading" score={result.colorScore} />
              <ScoreCard label="Lighting" score={result.lightingScore} />
              <ScoreCard label="Motion Quality" score={result.motionScore} />
              <ScoreCard label="Pacing" score={result.pacingScore} />
            </div>
          </div>

          <FrameTimeline frames={result.frames} />
          <MotionGraph data={result.motionData} />

          {result.insights && (
            <div className="bg-surface border border-border rounded-xl p-4">
              <h4 className="text-xs text-muted uppercase tracking-wider mb-2">Cinematic Insights</h4>
              <ul className="space-y-2">
                {result.insights.map((insight, i) => (
                  <li key={i} className="text-sm flex items-start gap-2">
                    <span className="text-accent">→</span> {insight}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : null}
    </div>
  )
}
