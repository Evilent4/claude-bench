import { NextRequest, NextResponse } from 'next/server'
import { getScores, insertScore } from '@/lib/supabase'
import { DIMENSION_KEYS } from '@/lib/dimensions'

export async function GET(req: NextRequest) {
  const sort = req.nextUrl.searchParams.get('sort') || 'overall'
  const scores = await getScores(sort)
  return NextResponse.json(scores)
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null)

  if (!body || typeof body !== 'object') {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 })
  }

  if (!body.handle || typeof body.handle !== 'string') {
    return NextResponse.json({ error: 'handle is required' }, { status: 400 })
  }

  if (typeof body.overall !== 'number') {
    return NextResponse.json({ error: 'overall score is required' }, { status: 400 })
  }

  for (const key of DIMENSION_KEYS) {
    if (typeof body[key] !== 'number') {
      return NextResponse.json({ error: `${key} score is required` }, { status: 400 })
    }
  }

  const created = await insertScore({
    handle: body.handle,
    overall: body.overall,
    agents: body.agents,
    quality: body.quality,
    autonomy: body.autonomy,
    safety: body.safety,
    memory: body.memory,
    skills: body.skills,
    infra: body.infra,
    security: body.security,
    domain: body.domain,
    scanner_version: body.scanner_version || '1.0.0',
    metadata: body.metadata || {},
  })

  if (!created) {
    return NextResponse.json({ error: 'Failed to save score' }, { status: 500 })
  }

  return NextResponse.json(created, { status: 201 })
}
