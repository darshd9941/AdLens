import { MessageSquare, Smile, AlertTriangle, CheckCircle, Hash, BookOpen } from 'lucide-react'

function StatBadge({ icon: Icon, label, value, type = 'neutral' }) {
  const colors = {
    good: 'bg-green/10 text-green border-green/20',
    warn: 'bg-yellow/10 text-yellow border-yellow/20',
    bad: 'bg-red/10 text-red border-red/20',
    neutral: 'bg-surface-2 text-muted border-border'
  }

  return (
    <div className={`flex items-center gap-2 px-3 py-2 rounded-lg border ${colors[type]}`}>
      <Icon className="w-3.5 h-3.5" />
      <span className="text-xs font-medium">{label}</span>
      <span className="text-xs ml-auto font-bold">{value}</span>
    </div>
  )
}

export default function CopyAnalysis({ data }) {
  if (!data) return null

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-accent uppercase tracking-wider flex items-center gap-2">
        <MessageSquare className="w-4 h-4" /> Ad Copy Analysis
      </h3>

      {data.headline && (
        <div className="bg-surface border border-border rounded-xl p-4">
          <p className="text-xs text-muted mb-1">Headline</p>
          <p className="text-sm font-medium">"{data.headline}"</p>
        </div>
      )}

      {data.bodyText && (
        <div className="bg-surface border border-border rounded-xl p-4">
          <p className="text-xs text-muted mb-1">Body Text</p>
          <p className="text-sm">"{data.bodyText}"</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-2">
        <StatBadge
          icon={Smile}
          label="Sentiment"
          value={data.sentiment || 'N/A'}
          type={data.sentimentScore >= 60 ? 'good' : data.sentimentScore >= 40 ? 'neutral' : 'bad'}
        />
        <StatBadge
          icon={AlertTriangle}
          label="Emotion"
          value={data.primaryEmotion || 'N/A'}
          type="neutral"
        />
        <StatBadge
          icon={BookOpen}
          label="Readability"
          value={data.readability || 'N/A'}
          type={data.readabilityScore >= 60 ? 'good' : 'warn'}
        />
        <StatBadge
          icon={Hash}
          label="Length"
          value={data.charCount ? `${data.charCount} chars` : 'N/A'}
          type={data.charCount <= 125 ? 'good' : data.charCount <= 200 ? 'warn' : 'bad'}
        />
      </div>

      {data.powerWords && data.powerWords.length > 0 && (
        <div className="bg-surface border border-border rounded-xl p-4">
          <p className="text-xs text-muted mb-2">Power Words Detected</p>
          <div className="flex flex-wrap gap-1.5">
            {data.powerWords.map((w, i) => (
              <span key={i} className="px-2 py-0.5 bg-accent/10 text-accent text-xs rounded-full border border-accent/20">
                {w}
              </span>
            ))}
          </div>
        </div>
      )}

      {data.suggestions && data.suggestions.length > 0 && (
        <div className="bg-surface border border-border rounded-xl p-4">
          <p className="text-xs text-muted mb-2">Suggestions</p>
          <ul className="space-y-1.5">
            {data.suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-text">
                <CheckCircle className="w-3.5 h-3.5 text-green mt-0.5 shrink-0" />
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
