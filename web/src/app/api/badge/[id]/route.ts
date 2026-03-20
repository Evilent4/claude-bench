import { NextRequest, NextResponse } from 'next/server'
import { getScoreById, getScoreByHandle } from '@/lib/supabase'

function badgeColour(score: number): string {
  if (score >= 80) return '#10b981'
  if (score >= 50) return '#f59e0b'
  return '#ef4444'
}

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  // Try UUID first, then handle
  let score = await getScoreById(id)
  if (!score) score = await getScoreByHandle(id)

  if (!score) {
    return new NextResponse('Not found', { status: 404 })
  }

  const labelWidth = 100
  const valueWidth = 60
  const totalWidth = labelWidth + valueWidth
  const colour = badgeColour(score.overall)

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${totalWidth}" height="20" role="img" aria-label="Claude Bench: ${score.overall}/100">
  <title>Claude Bench: ${score.overall}/100</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="${totalWidth}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="${labelWidth}" height="20" fill="#18181b"/>
    <rect x="${labelWidth}" width="${valueWidth}" height="20" fill="${colour}"/>
    <rect width="${totalWidth}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="11">
    <text aria-hidden="true" x="${labelWidth / 2}" y="15" fill="#010101" fill-opacity=".3">Claude Bench</text>
    <text x="${labelWidth / 2}" y="14" fill="#fff">Claude Bench</text>
    <text aria-hidden="true" x="${labelWidth + valueWidth / 2}" y="15" fill="#010101" fill-opacity=".3">${score.overall}/100</text>
    <text x="${labelWidth + valueWidth / 2}" y="14" fill="#fff">${score.overall}/100</text>
  </g>
</svg>`

  return new NextResponse(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=3600',
    },
  })
}
