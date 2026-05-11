import { useCallback, useState } from 'react'
import { Upload, Image, Film } from 'lucide-react'

export default function UploadZone({ onFile, accept = 'image/*', label }) {
  const [dragging, setDragging] = useState(false)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) onFile(file)
  }, [onFile])

  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) onFile(file)
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
        dragging
          ? 'border-accent bg-accent/10'
          : 'border-border hover:border-accent/50 hover:bg-surface-2'
      }`}
      onClick={() => document.getElementById('file-input').click()}
    >
      <input
        id="file-input"
        type="file"
        accept={accept}
        onChange={handleChange}
        className="hidden"
      />
      <div className="flex flex-col items-center gap-3">
        <div className="w-14 h-14 rounded-full bg-surface-2 flex items-center justify-center">
          {accept.includes('video') ? (
            <Film className="w-7 h-7 text-accent" />
          ) : (
            <Image className="w-7 h-7 text-accent" />
          )}
        </div>
        <div>
          <p className="text-sm font-medium">{label || 'Drop your ad creative here'}</p>
          <p className="text-xs text-muted mt-1">or click to browse</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted">
          <Upload className="w-3 h-3" />
          {accept.includes('video') ? 'MP4, MOV, WebM' : 'JPG, PNG, WebP'}
        </div>
      </div>
    </div>
  )
}
