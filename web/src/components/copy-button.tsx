'use client'

import { useState } from 'react'

export function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <button
      onClick={handleCopy}
      className="shrink-0 rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs text-zinc-400 hover:text-zinc-200 hover:border-zinc-600 transition-colors"
    >
      {copied ? 'Copied' : 'Copy'}
    </button>
  )
}
