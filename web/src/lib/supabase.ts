import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
)

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
