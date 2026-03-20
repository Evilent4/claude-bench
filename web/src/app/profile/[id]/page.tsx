import Link from 'next/link'
import { notFound } from 'next/navigation'
import { mockScores } from '@/lib/mock-data'
import { RadarChart } from '@/components/radar-chart'
import { DimensionBreakdown } from '@/components/dimension-breakdown'
import { CopyButton } from './copy-button'

export default async function ProfilePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const score = mockScores.find((s) => s.id === id)

  if (!score) notFound()

  const badgeUrl = `https://claudebench.dev/api/badge/${score.id}`
  const profileUrl = `https://claudebench.dev/profile/${score.id}`
  const badgeMarkdown = `![Claude Bench](${badgeUrl})`

  function overallColour(s: number): string {
    if (s >= 80) return 'text-emerald-400'
    if (s >= 50) return 'text-amber-400'
    return 'text-red-400'
  }

  const meta = score.metadata as Record<string, unknown>

  return (
    <div className="min-h-screen bg-zinc-950">
      <div className="max-w-4xl mx-auto px-6 py-16">
        <Link href="/" className="text-sm text-zinc-600 hover:text-zinc-400 transition-colors mb-8 inline-block">
          &larr; Back to leaderboard
        </Link>

        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-12">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">{score.handle}</h1>
            <p className="text-sm text-zinc-500">
              Scored on{' '}
              {new Date(score.created_at).toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
              })}
              {' '}with scanner v{score.scanner_version}
            </p>
          </div>
          <div className="text-right">
            <div className={`text-5xl font-mono font-bold ${overallColour(score.overall)}`}>
              {score.overall}
            </div>
            <div className="text-sm text-zinc-500 font-mono">/100</div>
          </div>
        </div>

        {/* Radar + Breakdown */}
        <div className="grid md:grid-cols-2 gap-12 mb-12">
          <div>
            <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider mb-4">
              Radar
            </h2>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">
              <RadarChart scores={score} size="lg" />
            </div>
          </div>
          <div>
            <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider mb-4">
              Breakdown
            </h2>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
              <DimensionBreakdown score={score} />
            </div>
          </div>
        </div>

        {/* Metadata */}
        {meta && Object.keys(meta).length > 0 && (
          <div className="mb-12">
            <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider mb-4">
              Metadata
            </h2>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(meta).map(([key, value]) => (
                  <div key={key}>
                    <div className="text-xs text-zinc-500 mb-1">{key.replace(/_/g, ' ')}</div>
                    <div className="font-mono text-sm text-zinc-300">{String(value)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Share */}
        <div>
          <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider mb-4">
            Share
          </h2>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6 space-y-4">
            <div>
              <div className="text-xs text-zinc-500 mb-2">Badge embed (Markdown)</div>
              <div className="flex items-center gap-2">
                <code className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 font-mono text-xs text-zinc-400 overflow-x-auto">
                  {badgeMarkdown}
                </code>
                <CopyButton text={badgeMarkdown} />
              </div>
            </div>
            <div>
              <div className="text-xs text-zinc-500 mb-2">Profile link</div>
              <div className="flex items-center gap-2">
                <code className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 font-mono text-xs text-zinc-400 overflow-x-auto">
                  {profileUrl}
                </code>
                <CopyButton text={profileUrl} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
