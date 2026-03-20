import { NextRequest, NextResponse } from 'next/server'
import { mockScores } from '@/lib/mock-data'
import { DIMENSION_KEYS } from '@/lib/dimensions'

export async function GET(req: NextRequest) {
  const sort = req.nextUrl.searchParams.get('sort') || 'overall'
  const validSorts = ['overall', ...DIMENSION_KEYS, 'created_at']

  const sortKey = validSorts.includes(sort) ? sort : 'overall'

  const sorted = [...mockScores].sort((a, b) => {
    const av = a[sortKey as keyof typeof a]
    const bv = b[sortKey as keyof typeof b]
    if (typeof av === 'number' && typeof bv === 'number') return bv - av
    if (typeof av === 'string' && typeof bv === 'string') return bv.localeCompare(av)
    return 0
  })

  return NextResponse.json(sorted)
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

  // TODO: Insert into Supabase when connected
  const created = {
    id: crypto.randomUUID(),
    ...body,
    created_at: new Date().toISOString(),
  }

  console.log('Score submitted:', created)
  return NextResponse.json(created, { status: 201 })
}
