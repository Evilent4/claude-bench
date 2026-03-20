import { Score } from '@/lib/supabase'
import { DIMENSIONS, DIMENSION_KEYS } from '@/lib/dimensions'

function barColour(value: number, max: number): string {
  const pct = value / max
  if (pct >= 0.8) return 'bg-emerald-500'
  if (pct >= 0.5) return 'bg-amber-500'
  return 'bg-red-500'
}

export function DimensionBreakdown({ score }: { score: Score }) {
  return (
    <div className="space-y-4">
      {DIMENSION_KEYS.map((key) => {
        const dim = DIMENSIONS[key]
        const value = score[key]
        const pct = (value / dim.max) * 100

        return (
          <div key={key}>
            <div className="flex items-center justify-between mb-1">
              <div>
                <span className="text-sm font-medium text-zinc-200">{dim.label}</span>
                <span className="text-xs text-zinc-500 ml-2">{dim.description}</span>
              </div>
              <span className="font-mono text-sm text-zinc-400">
                {value}/{dim.max}
              </span>
            </div>
            <div className="h-2 rounded-full bg-zinc-800 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${barColour(value, dim.max)}`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        )
      })}
    </div>
  )
}
