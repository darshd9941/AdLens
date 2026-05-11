import { useEffect, useRef, useState } from 'react'

const STEP_COLORS = ['#6366f1', '#3b82f6', '#22c55e', '#eab308', '#ef4444']

export default function EyeTrackingOverlay({ imageUrl, steps, width, height }) {
  const canvasRef = useRef(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!steps || steps.length === 0 || !canvasRef.current || !imageUrl) return
    setReady(false)

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const img = new Image()
    img.crossOrigin = 'anonymous'

    img.onload = () => {
      const iw = img.naturalWidth || width
      const ih = img.naturalHeight || height
      canvas.width = iw
      canvas.height = ih

      ctx.clearRect(0, 0, iw, ih)
      ctx.drawImage(img, 0, 0, iw, ih)

      const positions = generatePositions(steps.length, iw, ih)

      for (let i = 0; i < steps.length && i < 5; i++) {
        const pos = positions[i]
        const color = STEP_COLORS[i]
        const radius = 20

        ctx.globalAlpha = 0.3
        ctx.beginPath()
        ctx.arc(pos.x, pos.y, radius + 10, 0, Math.PI * 2)
        ctx.fillStyle = color
        ctx.fill()

        ctx.globalAlpha = 0.9
        ctx.beginPath()
        ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2)
        ctx.fillStyle = color
        ctx.fill()
        ctx.strokeStyle = '#ffffff'
        ctx.lineWidth = 2
        ctx.stroke()

        ctx.fillStyle = '#ffffff'
        ctx.font = 'bold 16px -apple-system, sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(String(i + 1), pos.x, pos.y)

        if (i < steps.length - 1 && i < 4) {
          const nextPos = positions[i + 1]
          ctx.globalAlpha = 0.6
          ctx.beginPath()
          ctx.moveTo(pos.x, pos.y)
          ctx.lineTo(nextPos.x, nextPos.y)
          ctx.strokeStyle = color
          ctx.lineWidth = 3
          ctx.setLineDash([8, 6])
          ctx.stroke()
          ctx.setLineDash([])

          const angle = Math.atan2(nextPos.y - pos.y, nextPos.x - pos.x)
          const arrowLen = 12
          const mx = (pos.x + nextPos.x) / 2
          const my = (pos.y + nextPos.y) / 2
          ctx.beginPath()
          ctx.moveTo(mx, my)
          ctx.lineTo(mx - arrowLen * Math.cos(angle - 0.4), my - arrowLen * Math.sin(angle - 0.4))
          ctx.moveTo(mx, my)
          ctx.lineTo(mx - arrowLen * Math.cos(angle + 0.4), my - arrowLen * Math.sin(angle + 0.4))
          ctx.strokeStyle = color
          ctx.lineWidth = 3
          ctx.setLineDash([])
          ctx.stroke()
        }
      }

      ctx.globalAlpha = 1.0
      setReady(true)
    }

    img.onerror = () => setReady(true)
    img.src = imageUrl
  }, [steps, imageUrl, width, height])

  if (!steps || steps.length === 0) return null

  return (
    <div className="relative inline-block w-full">
      <canvas
        ref={canvasRef}
        className="rounded-lg w-full h-auto block"
      />
      <div className="absolute bottom-3 left-3 bg-bg/90 backdrop-blur rounded-lg p-2 space-y-1 max-w-xs">
        {steps.slice(0, 5).map((step, i) => (
          <div key={i} className="flex items-center gap-2 text-[11px]">
            <span
              className="w-5 h-5 rounded-full flex items-center justify-center text-white text-[10px] font-bold shrink-0"
              style={{ background: STEP_COLORS[i] }}
            >
              {i + 1}
            </span>
            <span className="text-text/80">{step}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function generatePositions(count, w, h) {
  const positions = [
    { x: w * 0.35, y: h * 0.3 },
    { x: w * 0.65, y: h * 0.25 },
    { x: w * 0.5, y: h * 0.55 },
    { x: w * 0.3, y: h * 0.75 },
    { x: w * 0.7, y: h * 0.8 },
  ]
  return positions.slice(0, count)
}
