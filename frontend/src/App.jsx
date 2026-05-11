import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import StaticAnalysis from './pages/StaticAnalysis'
import VideoAnalysis from './pages/VideoAnalysis'
import CompetitorInsights from './pages/CompetitorInsights'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<StaticAnalysis />} />
        <Route path="/video" element={<VideoAnalysis />} />
        <Route path="/competitors" element={<CompetitorInsights />} />
      </Route>
    </Routes>
  )
}
