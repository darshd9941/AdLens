import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const uploadImage = (file, copyText = '') => {
  const form = new FormData()
  form.append('file', file)
  if (copyText) form.append('copy_text', copyText)
  return api.post('/analyze-image', form)
}

export const uploadVideo = (file) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/analyze-video', form)
}

export const checkCompliance = (file) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/check-compliance', form)
}

export const searchCompetitors = (query) =>
  api.get('/competitor-search', { params: { q: query } })
