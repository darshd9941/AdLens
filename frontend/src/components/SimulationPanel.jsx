import { useState, useEffect } from 'react'
import { IndianRupee, TrendingUp, ArrowUpRight, ArrowDownRight, Clock, Beaker, BarChart3, Download } from 'lucide-react'
import axios from 'axios'

const INDUSTRIES = [
  { value: 'default', label: 'General' },
  { value: 'ecommerce', label: 'E-commerce' },
  { value: 'saas', label: 'SaaS / Tech' },
  { value: 'education', label: 'Education' },
  { value: 'food', label: 'Food & Beverage' },
  { value: 'fashion', label: 'Fashion' },
  { value: 'real_estate', label: 'Real Estate' },
  { value: 'health', label: 'Health & Fitness' },
  { value: 'local_business', label: 'Local Business' },
]

export default function SimulationPanel({ analysis }) {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [industry, setIndustry] = useState('default')
  const [budget, setBudget] = useState(1000)

  const runSimulation = async () => {
    if (!analysis) return
    setLoading(true)
    try {
      const res = await axios.post('/api/simulate', null, {
        params: {
          overallScore: analysis.overallScore || 50,
          copyScore: analysis.copyScore || 50,
          ctaScore: analysis.ctaScore || 50,
          visualScore: analysis.visualScore || 50,
          industry,
          dailyBudget: budget,
          extractedText: analysis.extractedText || '',
        },
      })
      setData(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  if (!analysis) return null

  const sim = data?.simulation
  const abTests = data?.abTests
  const posting = data?.postingSchedule

  return (
    <div className="space-y-6 mt-6">
      {/* Controls */}
      <div className="bg-surface border border-border rounded-xl p-4">
        <h3 className="text-sm font-semibold text-accent uppercase tracking-wider mb-3 flex items-center gap-2">
          <IndianRupee className="w-4 h-4" /> India Market Simulation
        </h3>
        <div className="flex gap-3 items-end flex-wrap">
          <div className="flex-1 min-w-[160px]">
            <label className="text-[10px] text-muted uppercase block mb-1">Industry</label>
            <select
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent"
            >
              {INDUSTRIES.map((i) => (
                <option key={i.value} value={i.value}>{i.label}</option>
              ))}
            </select>
          </div>
          <div className="flex-1 min-w-[160px]">
            <label className="text-[10px] text-muted uppercase block mb-1">Daily Budget (₹)</label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              min={100}
              step={100}
              className="w-full bg-bg border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent"
            />
          </div>
          <button
            onClick={runSimulation}
            disabled={loading}
            className="px-5 py-2 bg-accent text-white text-sm font-medium rounded-lg hover:bg-accent-hover disabled:opacity-40"
          >
            {loading ? 'Simulating...' : 'Run Simulation'}
          </button>
        </div>
      </div>

      {sim && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <MetricCard label="CTR" value={`${sim.metrics.ctr}%`} good={sim.metrics.ctr > 1.5} />
            <MetricCard label="CPM" value={`₹${sim.metrics.cpm}`} good={sim.metrics.cpm < 100} />
            <MetricCard label="CPC" value={`₹${sim.metrics.cpc}`} good={sim.metrics.cpc < 5} />
            <MetricCard label="ROAS" value={`${sim.metrics.roas}x`} good={sim.metrics.roas > 3} />
          </div>

          {/* Daily Estimates */}
          <div className="bg-surface border border-border rounded-xl p-4">
            <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Daily Estimate (₹{budget}/day)</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <EstimateItem icon={ArrowUpRight} label="Impressions" value={sim.daily.impressions.toLocaleString()} />
              <EstimateItem icon={TrendingUp} label="Clicks" value={sim.daily.clicks.toLocaleString()} />
              <EstimateItem label="Likes" value={sim.daily.likes.toLocaleString()} />
              <EstimateItem label="Comments" value={sim.daily.comments.toLocaleString()} />
              <EstimateItem label="Shares" value={sim.daily.shares.toLocaleString()} />
              <EstimateItem label="Saves" value={sim.daily.saves.toLocaleString()} />
              <EstimateItem label="Conversions" value={sim.daily.conversions} />
              <EstimateItem label="Revenue" value={`₹${sim.daily.revenue.toLocaleString()}`} highlight />
            </div>
          </div>

          {/* Monthly Estimate */}
          <div className="bg-surface border border-border rounded-xl p-4">
            <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Monthly Estimate (₹{(budget * 30).toLocaleString()}/month)</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <EstimateItem label="Total Impressions" value={sim.monthly.impressions.toLocaleString()} />
              <EstimateItem label="Total Clicks" value={sim.monthly.clicks.toLocaleString()} />
              <EstimateItem label="Total Conversions" value={sim.monthly.conversions.toLocaleString()} />
              <EstimateItem label="Total Revenue" value={`₹${sim.monthly.revenue.toLocaleString()}`} highlight />
            </div>
          </div>

          {/* Platform Performance */}
          <div className="bg-surface border border-border rounded-xl p-4">
            <h4 className="text-xs text-muted uppercase tracking-wider mb-3">Platform Breakdown</h4>
            <div className="space-y-2">
              {sim.bestPlatforms.map((p, i) => (
                <div key={i} className="flex items-center justify-between bg-surface-2 rounded-lg px-3 py-2">
                  <div>
                    <span className="text-sm font-medium capitalize">{p.name.replace(/_/g, ' ')}</span>
                  </div>
                  <div className="flex gap-4 text-xs text-muted">
                    <span>CTR: <b className="text-text">{p.ctr}%</b></span>
                    <span>CPM: <b className="text-text">₹{p.cpm}</b></span>
                    <span>Clicks: <b className="text-text">{p.daily_clicks}</b></span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* A/B Tests */}
          {abTests && abTests.length > 0 && (
            <div className="bg-surface border border-border rounded-xl p-4">
              <h4 className="text-xs text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
                <Beaker className="w-4 h-4" /> A/B Test Suggestions
              </h4>
              <div className="space-y-3">
                {abTests.map((t, i) => (
                  <div key={i} className="bg-surface-2 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium">{t.test}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${t.priority === 'High' ? 'bg-red/10 text-red' : 'bg-yellow/10 text-yellow'}`}>
                        {t.priority}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs mt-2">
                      <div className="bg-bg rounded px-2 py-1.5">
                        <span className="text-muted">A:</span> {t.variant_a}
                      </div>
                      <div className="bg-bg rounded px-2 py-1.5">
                        <span className="text-muted">B:</span> {t.variant_b}
                      </div>
                    </div>
                    <p className="text-[11px] text-green mt-1.5">Expected: {t.expected_impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Posting Schedule */}
          {posting && (
            <div className="bg-surface border border-border rounded-xl p-4">
              <h4 className="text-xs text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
                <Clock className="w-4 h-4" /> Best Posting Times (IST)
              </h4>
              <div className="space-y-2">
                {posting.weekday.slice(0, 3).map((t, i) => (
                  <div key={i} className="flex items-center justify-between bg-surface-2 rounded-lg px-3 py-2">
                    <div className="flex items-center gap-3">
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${t.score >= 90 ? 'bg-green/10 text-green' : t.score >= 75 ? 'bg-yellow/10 text-yellow' : 'bg-surface text-muted'}`}>
                        {t.score}
                      </div>
                      <div>
                        <span className="text-sm font-medium">{t.time}</span>
                        <p className="text-[11px] text-muted">{t.note}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {posting.recommended_schedule.map((s, i) => (
                  <span key={i} className="text-[11px] bg-surface-2 text-muted px-2 py-1 rounded-lg">{s}</span>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

function MetricCard({ label, value, good }) {
  return (
    <div className="bg-surface border border-border rounded-xl p-3 text-center">
      <span className="text-[10px] text-muted uppercase">{label}</span>
      <p className={`text-xl font-bold mt-1 ${good ? 'text-green' : 'text-yellow'}`}>{value}</p>
    </div>
  )
}

function EstimateItem({ label, value, icon: Icon, highlight }) {
  return (
    <div className="text-center">
      <span className="text-[10px] text-muted uppercase">{label}</span>
      <p className={`text-sm font-medium mt-0.5 ${highlight ? 'text-green' : 'text-text'}`}>
        {Icon && <Icon className="w-3 h-3 inline mr-1" />}
        {value}
      </p>
    </div>
  )
}
