import { useState } from 'react'
import { Loader2, RotateCcw, Shield, MessageSquare } from 'lucide-react'
import UploadZone from '../components/UploadZone'
import ScoreCard from '../components/ScoreCard'
import HeatmapOverlay from '../components/HeatmapOverlay'
import CreativeDNA from '../components/CreativeDNA'
import CopyAnalysis from '../components/CopyAnalysis'
import { uploadImage, checkCompliance } from '../utils/api'

export default function StaticAnalysis() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [preview, setPreview] = useState(null)
  const [showHeatmap, setShowHeatmap] = useState(true)
  const [compliance, setCompliance] = useState(null)
  const [copyText, setCopyText] = useState('')
  const [file, setFile] = useState(null)

  const handleFile = (f) => {
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
    setCompliance(null)
  }

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setResult(null)
    setCompliance(null)
    try {
      const res = await uploadImage(file, copyText)
      setResult(res.data)
      try {
        const comp = await checkCompliance(file)
        setCompliance(comp.data)
      } catch {}
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const handleReset = () => {
    setPreview(null)
    setResult(null)
    setCompliance(null)
    setShowHeatmap(true)
    setCopyText('')
    setFile(null)
  }

  if (!preview) {
    return (
      <div className="p-8 max-w-2xl mx-auto">
        <h2 className="text-xl font-bold mb-1">Analyze Static Ad</h2>
        <p className="text-sm text-muted mb-6">Upload an image to get AI-powered creative analysis</p>
        <UploadZone onFile={handleFile} accept="image/*" />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Analysis Results</h2>
        <div className="flex gap-2">
          {result && (
            <button
              onClick={() => setShowHeatmap(!showHeatmap)}
              className="px-3 py-1.5 text-xs bg-surface border border-border rounded-lg hover:bg-surface-2"
            >
              {showHeatmap ? 'Hide' : 'Show'} Heatmap
            </button>
          )}
          <button
            onClick={handleReset}
            className="px-3 py-1.5 text-xs bg-surface border border-border rounded-lg hover:bg-surface-2 flex items-center gap-1.5"
          >
            <RotateCcw className="w-3 h-3" /> New Upload
          </button>
        </div>
      </div>

      {!result && !loading && (
        <div className="bg-surface border border-border rounded-xl p-4 mb-6">
          <div className="flex items-start gap-4">
            <img src={preview} alt="Preview" className="w-24 h-24 object-cover rounded-lg" />
            <div className="flex-1 space-y-3">
              <div>
                <label className="text-xs text-muted uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
                  <MessageSquare className="w-3 h-3" /> Ad Copy (auto-extracted from image via OCR — edit if needed)
                </label>
                <textarea
                  value={copyText}
                  onChange={(e) => setCopyText(e.target.value)}
                  placeholder="Text will be auto-extracted from the image. Override here if needed."
                  rows={2}
                  className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent resize-none"
                />
              </div>
              <button
                onClick={handleAnalyze}
                className="px-5 py-2.5 bg-accent text-white text-sm font-medium rounded-lg hover:bg-accent-hover"
              >
                Analyze Ad
              </button>
            </div>
          </div>
        </div>
      )}

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-8 h-8 text-accent animate-spin mb-3" />
          <p className="text-sm text-muted">Analyzing your creative...</p>
        </div>
      ) : result ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-surface border border-border rounded-xl p-4 relative">
              {showHeatmap && result.heatmap ? (
                <HeatmapOverlay
                  imageUrl={preview}
                  heatmapData={result.heatmap}
                  width={result.imageWidth || 500}
                  height={result.imageHeight || 500}
                />
              ) : (
                <img src={preview} alt="Ad" className="rounded-lg max-w-full" />
              )}
              {showHeatmap && result.heatmap && (
                <div className="absolute bottom-4 right-4 flex items-center gap-1.5 bg-bg/80 backdrop-blur px-2.5 py-1 rounded-lg text-[10px]">
                  <span className="inline-block w-3 h-2 rounded bg-blue-600" /> Low
                  <span className="inline-block w-3 h-2 rounded bg-green-500" /> Med
                  <span className="inline-block w-3 h-2 rounded bg-yellow-400" /> High
                  <span className="inline-block w-3 h-2 rounded bg-red-500" /> Hot
                </div>
              )}
            </div>

            {result.attention && (
              <div className="bg-surface border border-border rounded-xl p-4">
                <h4 className="text-xs text-muted uppercase tracking-wider mb-2">Attention Flow</h4>
                <p className="text-sm">{result.attention}</p>
              </div>
            )}

            {result.extractedText && (
              <div className="bg-surface border border-border rounded-xl p-4">
                <h4 className="text-xs text-muted uppercase tracking-wider mb-2">Extracted Text (OCR)</h4>
                <p className="text-sm text-text/80 italic">"{result.extractedText}"</p>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-3">
              <ScoreCard
                label="Overall"
                score={result.overallScore}
                detail="Combined creative effectiveness"
              />
              <ScoreCard
                label="Visual Appeal"
                score={result.visualScore}
                detail="Aesthetics and design quality"
              />
              <ScoreCard
                label="Copy Strength"
                score={result.copyScore}
                detail="Messaging effectiveness"
              />
              <ScoreCard
                label="CTA Power"
                score={result.ctaScore}
                detail="Call-to-action clarity"
              />
            </div>

            <CreativeDNA data={result.creativeDNA} />
            <CopyAnalysis data={result.copyAnalysis} />

            {compliance && (
              <div className="bg-surface border border-border rounded-xl p-4">
                <h4 className="text-xs text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
                  <Shield className="w-4 h-4" /> Compliance Check
                </h4>
                <div className="space-y-2">
                  {compliance.checks?.map((c, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs">
                      <span className={c.pass ? 'text-green' : 'text-red'}>
                        {c.pass ? '✓' : '✗'}
                      </span>
                      <span className="text-muted">{c.rule}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.insights && result.insights.length > 0 && (
              <div className="bg-surface border border-border rounded-xl p-4">
                <h4 className="text-xs text-muted uppercase tracking-wider mb-2">Insights</h4>
                <ul className="space-y-2">
                  {result.insights.map((insight, i) => (
                    <li key={i} className="text-sm flex items-start gap-2">
                      <span className="text-accent mt-0.5">→</span>
                      {insight}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.aiInsights && (
              <div className="bg-surface border border-accent/30 rounded-xl p-4">
                <h4 className="text-xs text-accent uppercase tracking-wider mb-2">Gemma AI Insights</h4>
                <p className="text-sm whitespace-pre-line">{result.aiInsights}</p>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  )
}
