export default function ScoreCard({ label, score, color = 'accent', icon: Icon, detail }) {
  const getColor = (s) => {
    if (s >= 80) return 'text-green'
    if (s >= 60) return 'text-yellow'
    if (s >= 40) return 'text-orange'
    return 'text-red'
  }

  const getBarColor = (s) => {
    if (s >= 80) return 'bg-green'
    if (s >= 60) return 'bg-yellow'
    if (s >= 40) return 'bg-orange'
    return 'bg-red'
  }

  return (
    <div className="bg-surface border border-border rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {Icon && <Icon className="w-4 h-4 text-muted" />}
          <span className="text-xs text-muted uppercase tracking-wider">{label}</span>
        </div>
        <span className={`text-2xl font-bold ${getColor(score)}`}>{score}</span>
      </div>
      <div className="w-full h-1.5 bg-surface-2 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${getBarColor(score)}`}
          style={{ width: `${score}%` }}
        />
      </div>
      {detail && <p className="text-xs text-muted mt-2">{detail}</p>}
    </div>
  )
}
