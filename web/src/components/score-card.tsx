import { Score } from '@/lib/supabase'
import { DIMENSIONS, DIMENSION_KEYS } from '@/lib/dimensions'
import { RadarChart } from './radar-chart'

function scoreBadgeColour(score: number): string {
  if (score >= 80) return 'text-emerald-400'
  if (score >= 50) return 'text-amber-400'
  return 'text-red-400'
}

export function ScoreCard({ score }: { score: Score }) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-6 max-w-md w-full">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-zinc-100">{score.handle}</h3>
          <p className="text-sm text-zinc-500">
            {new Date(score.created_at).toLocaleDateString('en-GB', {
              day: 'numeric',
              month: 'long',
              year: 'numeric',
            })}
          </p>
        </div>
        <div className="text-right">
          <div className={`text-3xl font-mono font-bold ${scoreBadgeColour(score.overall)}`}>
            {score.overall}
          </div>
          <div className="text-xs text-zinc-500 font-mono">/100</div>
        </div>
      </div>

      <div className="mb-4">
        <RadarChart scores={score} size="sm" />
      </div>

      <div className="grid grid-cols-3 gap-2 text-sm mb-4">
        {DIMENSION_KEYS.map((key) => (
          <div key={key} className="flex justify-between px-2 py-1 rounded bg-zinc-900">
            <span className="text-zinc-500">{DIMENSIONS[key].label}</span>
            <span className="font-mono text-zinc-300">
              {score[key]}/{DIMENSIONS[key].max}
            </span>
          </div>
        ))}
      </div>

      <div className="text-center text-xs text-zinc-600 border-t border-zinc-800 pt-3">
        Scored by Claude Bench
      </div>
    </div>
  )
}
