import { useEffect, useRef } from 'react'

export default function HeatmapOverlay({ imageUrl, heatmapData, width, height }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (!heatmapData || !canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    canvas.width = width
    canvas.height = height

    const img = new Image()
    img.onload = () => {
      ctx.drawImage(img, 0, 0, width, height)

      const heatCanvas = document.createElement('canvas')
      heatCanvas.width = width
      heatCanvas.height = height
      const heatCtx = heatCanvas.getContext('2d')

      const imgData = heatCtx.createImageData(width, height)
      const maxVal = Math.max(...heatmapData.flat())

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const val = heatmapData[y]?.[x] || 0
          const norm = val / (maxVal || 1)
          const idx = (y * width + x) * 4

          if (norm < 0.25) {
            imgData.data[idx] = 0
            imgData.data[idx + 1] = 0
            imgData.data[idx + 2] = Math.floor(norm * 4 * 255)
          } else if (norm < 0.5) {
            const t = (norm - 0.25) * 4
            imgData.data[idx] = 0
            imgData.data[idx + 1] = Math.floor(t * 255)
            imgData.data[idx + 2] = 255
          } else if (norm < 0.75) {
            const t = (norm - 0.5) * 4
            imgData.data[idx] = Math.floor(t * 255)
            imgData.data[idx + 1] = 255
            imgData.data[idx + 2] = Math.floor((1 - t) * 255)
          } else {
            const t = (norm - 0.75) * 4
            imgData.data[idx] = 255
            imgData.data[idx + 1] = Math.floor((1 - t) * 255)
            imgData.data[idx + 2] = 0
          }
          imgData.data[idx + 3] = Math.floor(norm * 180)
        }
      }

      heatCtx.putImageData(imgData, 0, 0)

      ctx.globalAlpha = 1
      ctx.drawImage(heatCanvas, 0, 0)
    }
    img.src = imageUrl
  }, [heatmapData, imageUrl, width, height])

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      className="rounded-lg max-w-full"
    />
  )
}
