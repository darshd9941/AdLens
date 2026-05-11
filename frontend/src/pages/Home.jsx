import { useNavigate } from 'react-router-dom'
import { Eye, Film, Search, Zap, ArrowRight, Sparkles, Brain, Activity } from 'lucide-react'

const features = [
  {
    icon: Eye,
    title: 'Attention Heatmap',
    desc: 'AI predicts exactly where eyes go on your static ads — no eye-tracking hardware needed',
    color: 'text-accent',
    path: '/analyze'
  },
  {
    icon: Brain,
    title: 'Creative DNA',
    desc: 'Decomposes every ad into atomic elements: colors, typography, faces, CTA, composition',
    color: 'text-purple-400',
    path: '/analyze'
  },
  {
    icon: Sparkles,
    title: 'AI Copy Analysis',
    desc: 'Sentiment, emotion, power words, readability — with actionable suggestions',
    color: 'text-yellow',
    path: '/analyze'
  },
  {
    icon: Activity,
    title: 'Performance Score',
    desc: 'Predicts ad effectiveness 1-100 BEFORE you spend a dollar on ads',
    color: 'text-green',
    path: '/analyze'
  },
  {
    icon: Film,
    title: 'Cinematic Video Analysis',
    desc: 'Frame-by-frame composition, color grading, lighting, pacing, and story arc',
    color: 'text-orange',
    path: '/video'
  },
  {
    icon: Search,
    title: 'Competitor Spy',
    desc: 'Analyze competitor ads from Meta Ads Library — see what works in your niche',
    color: 'text-blue',
    path: '/competitors'
  },
]

export default function Home() {
  const nav = useNavigate()

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-accent/10 border border-accent/20 rounded-full text-accent text-xs font-medium mb-4">
          <Zap className="w-3 h-3" /> Free &bull; No signup &bull; Local-first
        </div>
        <h1 className="text-4xl font-bold mb-3">
          AI Creative Intelligence for <span className="text-accent">Ad Performance</span>
        </h1>
        <p className="text-muted max-w-xl mx-auto">
          Upload any ad creative. Get attention heatmaps, creative DNA decomposition,
          copy analysis, and a performance score — all powered by AI.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((f, i) => (
          <button
            key={i}
            onClick={() => nav(f.path)}
            className="bg-surface border border-border rounded-xl p-5 text-left hover:border-accent/40 hover:bg-surface-2 transition-all group"
          >
            <f.icon className={`w-8 h-8 ${f.color} mb-3`} />
            <h3 className="font-semibold text-sm mb-1">{f.title}</h3>
            <p className="text-xs text-muted leading-relaxed mb-3">{f.desc}</p>
            <div className="flex items-center gap-1 text-xs text-accent opacity-0 group-hover:opacity-100 transition-opacity">
              Try it <ArrowRight className="w-3 h-3" />
            </div>
          </button>
        ))}
      </div>

      <div className="mt-12 bg-surface border border-border rounded-xl p-6 text-center">
        <p className="text-sm text-muted">
          Built with <span className="text-accent">OpenCV</span>, <span className="text-accent">PyTorch</span>,{' '}
          <span className="text-accent">D3.js</span>, and <span className="text-accent">FastAPI</span>.
          Every analysis runs locally on your machine.
        </p>
      </div>
    </div>
  )
}
