export const DIMENSIONS = {
  agents: { label: 'Agents', max: 15, description: 'Agent definitions, tool scoping, and model routing' },
  quality: { label: 'Quality', max: 15, description: 'Review pipelines, acceptance criteria, and testing gates' },
  autonomy: { label: 'Autonomy', max: 15, description: 'Flow protocol, crash recovery, and stall detection' },
  safety: { label: 'Safety', max: 15, description: 'Hooks, destructive command blocking, and guardrails' },
  memory: { label: 'Memory', max: 10, description: 'Session persistence, lessons, and cross-project state' },
  skills: { label: 'Skills', max: 10, description: 'Reusable skill definitions and dispatch protocols' },
  infra: { label: 'Infra', max: 10, description: 'MCP servers, scripts, queue runners, and tooling' },
  security: { label: 'Security', max: 5, description: 'Secret scanning, RLS policies, and auth hardening' },
  domain: { label: 'Domain', max: 5, description: 'Domain-specific agent specialisation and workflows' },
} as const

export type DimensionKey = keyof typeof DIMENSIONS
export const DIMENSION_KEYS = Object.keys(DIMENSIONS) as DimensionKey[]
export const MAX_OVERALL = Object.values(DIMENSIONS).reduce((sum, d) => sum + d.max, 0)
