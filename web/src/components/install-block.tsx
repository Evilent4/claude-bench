'use client'

import { useState } from 'react'

const INSTALL_CMD = 'pipx install claude-bench && claude-bench'

export function InstallBlock() {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    await navigator.clipboard.writeText(INSTALL_CMD)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 font-mono text-sm text-zinc-300 flex items-center gap-3">
          <span className="text-zinc-600 select-none">$</span>
          <code>{INSTALL_CMD}</code>
        </div>
        <button
          onClick={handleCopy}
          className="shrink-0 h-12 px-4 rounded-lg border border-zinc-700 bg-zinc-900 text-sm text-zinc-400 hover:text-zinc-200 hover:border-zinc-600 transition-colors"
        >
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <p className="text-xs text-zinc-600">
        Run from your project directory, or use <code className="text-zinc-500">claude-bench --path ~/Projects/my-setup</code>
      </p>
    </div>
  )
}
