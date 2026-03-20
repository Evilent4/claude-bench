'use client'

import { useState } from 'react'
import Link from 'next/link'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Score } from '@/lib/supabase'
import { DIMENSIONS, DIMENSION_KEYS, type DimensionKey } from '@/lib/dimensions'

function scoreBadgeClass(score: number): string {
  if (score >= 80) return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
  if (score >= 50) return 'bg-amber-500/15 text-amber-400 border-amber-500/30'
  return 'bg-red-500/15 text-red-400 border-red-500/30'
}

function dimensionBg(value: number, max: number): string {
  const pct = value / max
  if (pct >= 0.8) return 'bg-emerald-500/10'
  if (pct >= 0.5) return 'bg-amber-500/10'
  return 'bg-red-500/10'
}

type SortKey = 'overall' | DimensionKey | 'created_at'

export function LeaderboardTable({ scores }: { scores: Score[] }) {
  const [sortKey, setSortKey] = useState<SortKey>('overall')
  const [sortAsc, setSortAsc] = useState(false)
  const [expanded, setExpanded] = useState<string | null>(null)

  function handleSort(key: SortKey) {
    if (sortKey === key) {
      setSortAsc(!sortAsc)
    } else {
      setSortKey(key)
      setSortAsc(false)
    }
  }

  const sorted = [...scores].sort((a, b) => {
    const av = a[sortKey as keyof Score]
    const bv = b[sortKey as keyof Score]
    if (typeof av === 'number' && typeof bv === 'number') {
      return sortAsc ? av - bv : bv - av
    }
    if (typeof av === 'string' && typeof bv === 'string') {
      return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av)
    }
    return 0
  })

  const sortIndicator = (key: SortKey) =>
    sortKey === key ? (sortAsc ? ' \u2191' : ' \u2193') : ''

  return (
    <div className="w-full overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow className="border-zinc-800 hover:bg-transparent">
            <TableHead className="text-zinc-500 w-12">#</TableHead>
            <TableHead className="text-zinc-500">Handle</TableHead>
            <TableHead
              className="text-zinc-500 cursor-pointer hover:text-zinc-300 transition-colors"
              onClick={() => handleSort('overall')}
            >
              Overall{sortIndicator('overall')}
            </TableHead>
            {DIMENSION_KEYS.map((key) => (
              <TableHead
                key={key}
                className="text-zinc-500 cursor-pointer hover:text-zinc-300 transition-colors hidden lg:table-cell"
                onClick={() => handleSort(key)}
              >
                {DIMENSIONS[key].label}{sortIndicator(key)}
              </TableHead>
            ))}
            <TableHead
              className="text-zinc-500 cursor-pointer hover:text-zinc-300 transition-colors hidden md:table-cell"
              onClick={() => handleSort('created_at')}
            >
              Date{sortIndicator('created_at')}
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sorted.map((score, i) => (
            <>
              <TableRow
                key={score.id}
                className="border-zinc-800/50 hover:bg-zinc-900/50 cursor-pointer"
                onClick={() => setExpanded(expanded === score.id ? null : score.id)}
              >
                <TableCell className="font-mono text-zinc-600">{i + 1}</TableCell>
                <TableCell>
                  <Link
                    href={`/profile/${score.id}`}
                    className="font-medium text-zinc-200 hover:text-white transition-colors"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {score.handle}
                  </Link>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" className={scoreBadgeClass(score.overall)}>
                    <span className="font-mono">{score.overall}</span>
                  </Badge>
                </TableCell>
                {DIMENSION_KEYS.map((key) => (
                  <TableCell
                    key={key}
                    className={`hidden lg:table-cell font-mono text-sm text-zinc-400 ${dimensionBg(score[key], DIMENSIONS[key].max)}`}
                  >
                    {score[key]}
                  </TableCell>
                ))}
                <TableCell className="hidden md:table-cell text-zinc-500 text-sm">
                  {new Date(score.created_at).toLocaleDateString('en-GB', {
                    day: 'numeric',
                    month: 'short',
                  })}
                </TableCell>
              </TableRow>
              {expanded === score.id && (
                <TableRow key={`${score.id}-expanded`} className="border-zinc-800/50 lg:hidden">
                  <TableCell colSpan={4} className="py-3">
                    <div className="grid grid-cols-3 gap-2 text-sm">
                      {DIMENSION_KEYS.map((key) => (
                        <div key={key} className="flex justify-between gap-2 px-2 py-1 rounded bg-zinc-900">
                          <span className="text-zinc-500">{DIMENSIONS[key].label}</span>
                          <span className="font-mono text-zinc-300">{score[key]}/{DIMENSIONS[key].max}</span>
                        </div>
                      ))}
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
