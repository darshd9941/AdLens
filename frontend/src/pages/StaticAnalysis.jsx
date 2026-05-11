import { useState } from 'react'
import { Loader2, RotateCcw, Eye, Flame, ArrowRight } from 'lucide-react'
import UploadZone from '../components/UploadZone'
import ScoreCard from '../components/ScoreCard'
import HeatmapOverlay from '../components/HeatmapOverlay'
import EyeTrackingOverlay from '../components/EyeTrackingOverlay'
import SimulationPanel from '../components/SimulationPanel'
import { uploadImage } from '../utils/api'

function EyeTrackingPath({ steps }) {
  if (!steps || steps.length === 0) return null
  const colors = ['#6366f1', '#3b82f6', '#22c55e', '#eab308', '#ef4444']
  return (
    <div className="bg-surface border border-border rounded-xl p-4">
      <h4 className="text-xs text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
        <Eye className="w-4 h-4" /> Eye Tracking Path
      </h4>
      <div className="space-y-2">
        {steps.map((step, i) => (
          <div key={i} className="flex items-center gap-3">
            <div
              className="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0"
              style={{ background: colors[i] || '#6366f1' }}
            >
              {i + 1}
            </div>
            <div className="flex-1 text-sm">{step}</div>
            {i < steps.length - 1 && (
              <ArrowRight className="w-3 h-3 text-muted shrink-0" />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default function StaticAnalysis() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState(null)
  const [overlay, setOverlay] = useState('heatmap')

  const handleFile = async (file) => {
    setPreview(URL.createObjectURL(file))
    setLoading(true)
    setResult(null)
    setError(null)
    try {
      const res = await uploadImage(file)
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Is Ollama running with gemma4?')
    }
    setLoading(false)
  }

  const handleReset = () => {
    setPreview(null)
    setResult(null)
    setError(null)
    setOverlay('heatmap')
  }

  if (!preview) {
    return (
      <div className="p-8 max-w-2xl mx-auto">
        <h2 className="text-xl font-bold mb-1">Analyze Static Ad</h2>
        <p className="text-sm text-muted mb-6">Upload an image — Gemma 4 analyzes everything automatically</p>
        <UploadZone onFile={handleFile} accept="image/*" />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Analysis Results</h2>
        <div className="flex gap-2">
          <button
            onClick={handleReset}
            className="px-3 py-1.5 text-xs bg-surface border border-border rounded-lg hover:bg-surface-2 flex items-center gap-1.5"
          >
            <RotateCcw className="w-3 h-3" /> New Upload
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-8 h-8 text-accent animate-spin mb-3" />
          <p className="text-sm text-muted">Gemma 4 is analyzing your ad...</p>
        </div>
      ) : error ? (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6 text-center">
          <p className="text-red-400 text-sm">{error}</p>
          <button onClick={handleReset} className="mt-3 px-4 py-2 bg-surface border border-border rounded-lg text-sm hover:bg-surface-2">
            Try Again
          </button>
        </div>
      ) : result ? (
        <>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            {/* Image + Overlays */}
            <div className="bg-surface border border-border rounded-xl p-4 relative">
              {overlay === 'heatmap' && result.heatmap ? (
                <HeatmapOverlay
                  imageUrl={preview}
                  heatmapData={result.heatmap}
                  width={result.imageWidth || 500}
                  height={result.imageHeight || 500}
                />
              ) : overlay === 'eye' && result.eyeTracking ? (
                <EyeTrackingOverlay
                  imageUrl={preview}
                  steps={result.eyeTracking}
                  width={result.imageWidth || 500}
                  height={result.imageHeight || 500}
                />
              ) : (
                <img src={preview} alt="Ad" className="rounded-lg w-full h-auto block" />
              )}

              {/* Heatmap legend */}
              {overlay === 'heatmap' && result.heatmap && (
                <div className="absolute bottom-4 right-4 flex items-center gap-1.5 bg-bg/90 backdrop-blur px-2.5 py-1 rounded-lg text-[10px]">
                  <span className="inline-block w-3 h-2 rounded bg-blue-600" /> Low
                  <span className="inline-block w-3 h-2 rounded bg-green-500" /> Med
                  <span className="inline-block w-3 h-2 rounded bg-yellow-400" /> High
                  <span className="inline-block w-3 h-2 rounded bg-red-500" /> Hot
                </div>
              )}
            </div>

            {/* Overlay Toggle Buttons */}
            <div className="flex gap-2">
              <button
                onClick={() => setOverlay(overlay === 'heatmap' ? 'none' : 'heatmap')}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                  overlay === 'heatmap'
                    ? 'bg-accent text-white'
                    : 'bg-surface border border-border text-muted hover:text-text'
                }`}
              >
                <Flame className="w-3.5 h-3.5" /> Heatmap
              </button>
              <button
                onClick={() => setOverlay(overlay === 'eye' ? 'none' : 'eye')}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                  overlay === 'eye'
                    ? 'bg-accent text-white'
                    : 'bg-surface border border-border text-muted hover:text-text'
                }`}
              >
                <Eye className="w-3.5 h-3.5" /> Eye Tracking
              </button>
              {overlay !== 'none' && (
                <button
                  onClick={() => setOverlay('none')}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium bg-surface border border-border text-muted hover:text-text"
                >
                  Show Original
                </button>
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
                <h4 className="text-xs text-muted uppercase tracking-wider mb-2">Extracted Text</h4>
                <p className="text-sm text-text/80 italic">"{result.extractedText}"</p>
              </div>
            )}

            <EyeTrackingPath steps={result.eyeTracking} />
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <ScoreCard label="Overall" score={result.overallScore} detail="Combined effectiveness" />
              <ScoreCard label="Visual Appeal" score={result.visualScore} detail="Aesthetics quality" />
              <ScoreCard label="Copy Strength" score={result.copyScore} detail="Messaging impact" />
              <ScoreCard label="CTA Power" score={result.ctaScore} detail="Call-to-action clarity" />
            </div>

            {result.creativeDNA && (
              <>
                {result.creativeDNA.colors && result.creativeDNA.colors.length > 0 && (
                  <div className="bg-surface border border-border rounded-xl p-4">
                    <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Color Palette</h4>
                    <div className="flex gap-2 flex-wrap">
                      {result.creativeDNA.colors.map((c, i) => (
                        <div key={i} className="flex flex-col items-center gap-1">
                          <div
                            className="w-10 h-10 rounded-lg border border-border"
                            style={{ background: c.hex }}
                          />
                          <span className="text-[10px] text-muted">{c.hex}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-3">
                  {result.creativeDNA.composition && (
                    <div className="bg-surface border border-border rounded-xl p-3">
                      <span className="text-[10px] text-muted uppercase">Composition</span>
                      <p className="text-sm font-medium mt-1">{result.creativeDNA.composition.rule}</p>
                      <p className="text-xs text-muted mt-0.5">{result.creativeDNA.composition.feedback}</p>
                    </div>
                  )}
                  {result.creativeDNA.faces && (
                    <div className="bg-surface border border-border rounded-xl p-3">
                      <span className="text-[10px] text-muted uppercase">Faces</span>
                      <p className="text-sm font-medium mt-1">{result.creativeDNA.faces.count} detected</p>
                      <p className="text-xs text-muted mt-0.5">{result.creativeDNA.faces.feedback}</p>
                    </div>
                  )}
                  {result.creativeDNA.cta && (
                    <div className="bg-surface border border-border rounded-xl p-3">
                      <span className="text-[10px] text-muted uppercase">CTA</span>
                      <p className="text-sm font-medium mt-1">{result.creativeDNA.cta.text || 'Not detected'}</p>
                      <p className="text-xs text-muted mt-0.5">{result.creativeDNA.cta.feedback}</p>
                    </div>
                  )}
                  {result.creativeDNA.typography && (
                    <div className="bg-surface border border-border rounded-xl p-3">
                      <span className="text-[10px] text-muted uppercase">Typography</span>
                      <p className="text-sm font-medium mt-1">{result.creativeDNA.typography.style}</p>
                      <p className="text-xs text-muted mt-0.5">{result.creativeDNA.typography.feedback}</p>
                    </div>
                  )}
                </div>
              </>
            )}

            {result.copyAnalysis && (
              <div className="bg-surface border border-border rounded-xl p-4 space-y-3">
                <h4 className="text-xs text-muted uppercase tracking-wider">Copy Analysis</h4>
                <div className="flex gap-3 flex-wrap">
                  <span className={`px-2 py-0.5 text-xs rounded-full ${result.copyAnalysis.sentiment === 'positive' ? 'bg-green/10 text-green' : result.copyAnalysis.sentiment === 'negative' ? 'bg-red/10 text-red' : 'bg-surface-2 text-muted'}`}>
                    {result.copyAnalysis.sentiment}
                  </span>
                  {result.copyAnalysis.primaryEmotion && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-accent/10 text-accent">
                      {result.copyAnalysis.primaryEmotion}
                    </span>
                  )}
                </div>
                {result.copyAnalysis.suggestions?.length > 0 && (
                  <ul className="space-y-1.5">
                    {result.copyAnalysis.suggestions.map((s, i) => (
                      <li key={i} className="text-xs flex items-start gap-2">
                        <span className="text-accent mt-0.5">→</span> {s}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}

            {result.aiInsights && (
              <div className="bg-surface border border-accent/30 rounded-xl p-4">
                <h4 className="text-xs text-accent uppercase tracking-wider mb-2">Gemma AI Insights</h4>
                <p className="text-sm whitespace-pre-line leading-relaxed">{result.aiInsights}</p>
              </div>
            )}
          </div>
        </div>

        {/* Full Width Simulation */}
        <SimulationPanel analysis={result} />
        </>
      ) : null}
    </div>
  )
}
