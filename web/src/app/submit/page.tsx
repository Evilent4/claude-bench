'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { DIMENSION_KEYS } from '@/lib/dimensions'

interface ParsedScore {
  overall: number
  agents: number
  quality: number
  autonomy: number
  safety: number
  memory: number
  skills: number
  infra: number
  security: number
  domain: number
  scanner_version: string
  metadata: Record<string, unknown>
}

function validateScore(data: unknown): data is ParsedScore {
  if (typeof data !== 'object' || data === null) return false
  const obj = data as Record<string, unknown>

  if (typeof obj.overall !== 'number') return false
  for (const key of DIMENSION_KEYS) {
    if (typeof obj[key] !== 'number') return false
  }
  if (typeof obj.scanner_version !== 'string') return false

  return true
}

export default function SubmitPage() {
  const router = useRouter()
  const [handle, setHandle] = useState('')
  const [jsonInput, setJsonInput] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const text = await file.text()
    setJsonInput(text)
    setError(null)
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)

    if (!handle.trim()) {
      setError('Handle is required.')
      return
    }

    let parsed: unknown
    try {
      parsed = JSON.parse(jsonInput)
    } catch {
      setError('Invalid JSON. Paste the output from claude-bench or upload score.json.')
      return
    }

    if (!validateScore(parsed)) {
      setError('JSON schema mismatch. Ensure all dimension scores and scanner_version are present.')
      return
    }

    setSubmitting(true)
    try {
      const res = await fetch('/api/scores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ handle: handle.trim(), ...parsed }),
      })

      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.error || `Server error: ${res.status}`)
      }

      const created = await res.json()
      router.push(`/profile/${created.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Submission failed.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950">
      <div className="max-w-2xl mx-auto px-6 py-16">
        <Link href="/" className="text-sm text-zinc-600 hover:text-zinc-400 transition-colors mb-8 inline-block">
          &larr; Back to leaderboard
        </Link>

        <h1 className="text-3xl font-bold text-white mb-2">Submit Score</h1>
        <p className="text-zinc-500 mb-8">
          Paste the JSON output from <code className="font-mono text-zinc-400">claude-bench</code> or
          upload your <code className="font-mono text-zinc-400">score.json</code> file.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="handle" className="block text-sm font-medium text-zinc-300 mb-2">
              Handle
            </label>
            <input
              id="handle"
              type="text"
              value={handle}
              onChange={(e) => setHandle(e.target.value)}
              placeholder="e.g. my-setup"
              className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 font-mono text-sm"
            />
          </div>

          <div>
            <label htmlFor="json" className="block text-sm font-medium text-zinc-300 mb-2">
              Score JSON
            </label>
            <textarea
              id="json"
              value={jsonInput}
              onChange={(e) => { setJsonInput(e.target.value); setError(null) }}
              placeholder='{"overall": 72, "agents": 10, ...}'
              rows={12}
              className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 font-mono text-sm resize-y"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">
              Or upload file
            </label>
            <input
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="text-sm text-zinc-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border file:border-zinc-700 file:bg-zinc-900 file:text-zinc-300 file:text-sm file:cursor-pointer hover:file:bg-zinc-800 file:transition-colors"
            />
          </div>

          {error && (
            <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white font-medium py-3 transition-colors"
          >
            {submitting ? 'Submitting...' : 'Submit Score'}
          </button>
        </form>
      </div>
    </div>
  )
}
