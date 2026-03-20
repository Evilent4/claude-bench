import { createClient, SupabaseClient } from '@supabase/supabase-js'

export interface Score {
  id: string
  handle: string
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
  created_at: string
}

function getClient(): SupabaseClient | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  if (!url || !key) return null
  return createClient(url, key)
}

export async function getScores(sort: string = 'overall'): Promise<Score[]> {
  const client = getClient()
  if (!client) return []

  const validSorts = [
    'overall', 'agents', 'quality', 'autonomy', 'safety',
    'memory', 'skills', 'infra', 'security', 'domain', 'created_at',
  ]
  const sortKey = validSorts.includes(sort) ? sort : 'overall'

  const { data, error } = await client
    .from('scores')
    .select('*')
    .order(sortKey, { ascending: false })
    .limit(100)

  if (error) {
    console.error('Failed to fetch scores:', error)
    return []
  }
  return (data as Score[]) || []
}

export async function getScoreById(id: string): Promise<Score | null> {
  const client = getClient()
  if (!client) return null

  const { data, error } = await client
    .from('scores')
    .select('*')
    .eq('id', id)
    .single()

  if (error) return null
  return data as Score
}

export async function getScoreByHandle(handle: string): Promise<Score | null> {
  const client = getClient()
  if (!client) return null

  const { data, error } = await client
    .from('scores')
    .select('*')
    .eq('handle', handle)
    .order('created_at', { ascending: false })
    .limit(1)
    .single()

  if (error) return null
  return data as Score
}

export async function insertScore(score: Omit<Score, 'id' | 'created_at'>): Promise<Score | null> {
  const client = getClient()
  if (!client) return null

  const { data, error } = await client
    .from('scores')
    .insert(score)
    .select()
    .single()

  if (error) {
    console.error('Failed to insert score:', error)
    return null
  }
  return data as Score
}
