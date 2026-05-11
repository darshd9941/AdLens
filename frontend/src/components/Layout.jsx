import { Outlet, NavLink } from 'react-router-dom'
import { Eye, Upload, Film, Search, Zap } from 'lucide-react'

const nav = [
  { to: '/', icon: Zap, label: 'Home' },
  { to: '/analyze', icon: Eye, label: 'Analyze Ad' },
  { to: '/video', icon: Film, label: 'Video Analysis' },
  { to: '/competitors', icon: Search, label: 'Competitor Spy' },
]

export default function Layout() {
  return (
    <div className="flex h-screen">
      <aside className="w-56 bg-surface border-r border-border flex flex-col">
        <div className="p-5 border-b border-border">
          <h1 className="text-lg font-bold text-accent tracking-tight flex items-center gap-2">
            <Eye className="w-5 h-5" /> AdLens
          </h1>
          <p className="text-xs text-muted mt-1">AI Creative Intelligence</p>
        </div>
        <nav className="flex-1 p-2 flex flex-col gap-1">
          {nav.map(n => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-accent text-white'
                    : 'text-muted hover:bg-surface-2 hover:text-text'
                }`
              }
            >
              <n.icon className="w-4 h-4" />
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-border text-xs text-muted">
          Free &bull; No signup &bull; Local
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}
