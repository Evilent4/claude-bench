'use client'

import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts'
import { Score } from '@/lib/supabase'
import { DIMENSIONS, DIMENSION_KEYS } from '@/lib/dimensions'

interface RadarChartProps {
  scores: Pick<Score, 'agents' | 'quality' | 'autonomy' | 'safety' | 'memory' | 'skills' | 'infra' | 'security' | 'domain'>
  size?: 'sm' | 'lg'
}

export function RadarChart({ scores, size = 'lg' }: RadarChartProps) {
  const data = DIMENSION_KEYS.map((key) => ({
    dimension: DIMENSIONS[key].label,
    value: Math.round((scores[key as keyof typeof scores] as number / DIMENSIONS[key].max) * 100),
    fullMark: 100,
  }))

  const h = size === 'sm' ? 200 : 350

  return (
    <ResponsiveContainer width="100%" height={h}>
      <RechartsRadarChart data={data} cx="50%" cy="50%" outerRadius={size === 'sm' ? '70%' : '75%'}>
        <PolarGrid stroke="#27272a" />
        <PolarAngleAxis
          dataKey="dimension"
          tick={{ fill: '#71717a', fontSize: size === 'sm' ? 10 : 12 }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={size === 'lg' ? { fill: '#52525b', fontSize: 10 } : false}
          axisLine={false}
        />
        <Radar
          name="Score"
          dataKey="value"
          stroke="#10b981"
          fill="#10b981"
          fillOpacity={0.2}
          strokeWidth={2}
        />
      </RechartsRadarChart>
    </ResponsiveContainer>
  )
}
