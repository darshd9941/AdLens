import { useEffect, useRef, useState } from 'react'

export default function HeatmapOverlay({ imageUrl, heatmapData, width, height }) {
  const canvasRef = useRef(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!heatmapData || !canvasRef.current || !imageUrl) return
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

      const rows = heatmapData.length
      const cols = heatmapData[0]?.length || 0
      if (rows === 0 || cols === 0) { setReady(true); return }

      const heatCanvas = document.createElement('canvas')
      heatCanvas.width = cols
      heatCanvas.height = rows
      const heatCtx = heatCanvas.getContext('2d')
      const imgData = heatCtx.createImageData(cols, rows)

      let maxVal = 0
      for (let y = 0; y < rows; y++)
        for (let x = 0; x < cols; x++)
          if (heatmapData[y][x] > maxVal) maxVal = heatmapData[y][x]

      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
          const val = heatmapData[y][x] / (maxVal || 1)
          const idx = (y * cols + x) * 4

          if (val < 0.2) {
            imgData.data[idx] = 0; imgData.data[idx+1] = 0; imgData.data[idx+2] = 200; imgData.data[idx+3] = 0
          } else if (val < 0.4) {
            const t = (val - 0.2) / 0.2
            imgData.data[idx] = 0; imgData.data[idx+1] = Math.floor(t * 255); imgData.data[idx+2] = 255; imgData.data[idx+3] = Math.floor(t * 120)
          } else if (val < 0.6) {
            const t = (val - 0.4) / 0.2
            imgData.data[idx] = Math.floor(t * 255); imgData.data[idx+1] = 255; imgData.data[idx+2] = Math.floor((1-t) * 255); imgData.data[idx+3] = Math.floor(120 + t * 40)
          } else if (val < 0.8) {
            const t = (val - 0.6) / 0.2
            imgData.data[idx] = 255; imgData.data[idx+1] = Math.floor((1-t) * 200); imgData.data[idx+2] = 0; imgData.data[idx+3] = Math.floor(140 + t * 40)
          } else {
            imgData.data[idx] = 255; imgData.data[idx+1] = 0; imgData.data[idx+2] = 0; imgData.data[idx+3] = 200
          }
        }
      }

      heatCtx.putImageData(imgData, 0, 0)

      const scaled = document.createElement('canvas')
      scaled.width = iw
      scaled.height = ih
      const scaledCtx = scaled.getContext('2d')
      scaledCtx.drawImage(heatCanvas, 0, 0, iw, ih)

      ctx.globalAlpha = 0.55
      ctx.drawImage(scaled, 0, 0)
      ctx.globalAlpha = 1.0
      setReady(true)
    }

    img.onerror = () => setReady(true)
    img.src = imageUrl
  }, [heatmapData, imageUrl, width, height])

  return (
    <div className="relative inline-block w-full">
      <canvas
        ref={canvasRef}
        className="rounded-lg w-full h-auto block"
        style={{ imageRendering: 'auto' }}
      />
      {!ready && (
        <div className="absolute inset-0 flex items-center justify-center bg-surface/80 rounded-lg">
          <span className="text-xs text-muted">Loading heatmap...</span>
        </div>
      )}
    </div>
  )
}
