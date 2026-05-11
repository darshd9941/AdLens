import { useState } from 'react'
import { Search, Loader2, ExternalLink, Calendar, DollarSign } from 'lucide-react'
import { searchCompetitors } from '../utils/api'

export default function CompetitorInsights() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await searchCompetitors(query)
      setResults(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-xl font-bold mb-1">Competitor Ad Spy</h2>
      <p className="text-sm text-muted mb-6">
        Search Meta Ads Library to see what ads your competitors are running
      </p>

      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search competitor brand or domain..."
            className="w-full bg-surface border border-border rounded-lg pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-accent"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-5 py-2.5 bg-accent text-white text-sm font-medium rounded-lg hover:bg-accent-hover disabled:opacity-40 flex items-center gap-2"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
          Search
        </button>
      </form>

      {results && (
        <div className="space-y-4">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-sm text-muted">
              Found {results.ads?.length || 0} ads for "{results.query}"
            </span>
          </div>

          {results.ads?.length === 0 && (
            <div className="bg-surface border border-border rounded-xl p-8 text-center">
              <p className="text-muted text-sm">No ads found. Try a different search term.</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.ads?.map((ad, i) => (
              <div key={i} className="bg-surface border border-border rounded-xl overflow-hidden">
                {ad.thumbnail && (
                  <img src={ad.thumbnail} alt="Ad" className="w-full h-48 object-cover" />
                )}
                <div className="p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{ad.pageName}</span>
                    <a
                      href={ad.libraryUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-accent hover:text-accent-hover"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                  {ad.headline && (
                    <p className="text-sm font-medium text-accent">{ad.headline}</p>
                  )}
                  {ad.body && (
                    <p className="text-xs text-muted line-clamp-3">{ad.body}</p>
                  )}
                  <div className="flex items-center gap-4 text-xs text-muted pt-2 border-t border-border">
                    {ad.startDate && (
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" /> {ad.startDate}
                      </span>
                    )}
                    {ad.platforms && (
                      <span>{ad.platforms.join(', ')}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!results && !loading && (
        <div className="bg-surface border border-border rounded-xl p-12 text-center">
          <Search className="w-12 h-12 text-border mx-auto mb-3" />
          <p className="text-sm text-muted">
            Enter a competitor name or domain to see their active ads
          </p>
          <p className="text-xs text-muted mt-2">
            Data sourced from Meta Ads Library (public data)
          </p>
        </div>
      )}
    </div>
  )
}
