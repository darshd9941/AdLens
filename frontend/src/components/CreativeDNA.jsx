import { Palette, Type, Image, MousePointerClick, User, LayoutGrid } from 'lucide-react'

function ElementCard({ icon: Icon, label, value, score, detail }) {
  const getScoreColor = (s) => {
    if (s >= 80) return 'text-green border-green/30'
    if (s >= 60) return 'text-yellow border-yellow/30'
    if (s >= 40) return 'text-orange border-orange/30'
    return 'text-red border-red/30'
  }

  return (
    <div className={`bg-surface-2 border rounded-lg p-3 ${getScoreColor(score)}`}>
      <div className="flex items-center gap-2 mb-1">
        <Icon className="w-3.5 h-3.5" />
        <span className="text-xs font-medium uppercase tracking-wider">{label}</span>
        <span className={`ml-auto text-xs font-bold ${getScoreColor(score).split(' ')[0]}`}>{score}/100</span>
      </div>
      <p className="text-sm text-text">{value}</p>
      {detail && <p className="text-xs text-muted mt-1">{detail}</p>}
    </div>
  )
}

export default function CreativeDNA({ data }) {
  if (!data) return null

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-accent uppercase tracking-wider flex items-center gap-2">
        <LayoutGrid className="w-4 h-4" /> Creative DNA
      </h3>

      {data.colors && (
        <div className="bg-surface border border-border rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <Palette className="w-4 h-4 text-muted" />
            <span className="text-xs font-medium uppercase tracking-wider">Color Palette</span>
          </div>
          <div className="flex gap-2 flex-wrap">
            {data.colors.map((c, i) => (
              <div key={i} className="flex flex-col items-center gap-1">
                <div
                  className="w-10 h-10 rounded-lg border border-border"
                  style={{ background: c.hex }}
                />
                <span className="text-[10px] text-muted">{c.hex}</span>
                <span className="text-[10px] text-muted">{c.percentage}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        {data.typography && (
          <ElementCard
            icon={Type}
            label="Typography"
            score={data.typography.score}
            value={data.typography.style}
            detail={data.typography.feedback}
          />
        )}
        {data.composition && (
          <ElementCard
            icon={LayoutGrid}
            label="Composition"
            score={data.composition.score}
            value={data.composition.rule}
            detail={data.composition.feedback}
          />
        )}
        {data.faces && (
          <ElementCard
            icon={User}
            label="Faces"
            score={data.faces.score}
            value={data.faces.count > 0 ? `${data.faces.count} detected` : 'No faces'}
            detail={data.faces.feedback}
          />
        )}
        {data.cta && (
          <ElementCard
            icon={MousePointerClick}
            label="CTA"
            score={data.cta.score}
            value={data.cta.text || 'Not detected'}
            detail={data.cta.feedback}
          />
        )}
        {data.visualHierarchy && (
          <ElementCard
            icon={Image}
            label="Visual Hierarchy"
            score={data.visualHierarchy.score}
            value={data.visualHierarchy.flow}
            detail={data.visualHierarchy.feedback}
          />
        )}
      </div>
    </div>
  )
}
