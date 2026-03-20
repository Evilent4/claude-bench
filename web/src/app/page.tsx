import { LeaderboardTable } from '@/components/leaderboard-table'
import { getScores } from '@/lib/supabase'

export const revalidate = 60

export default async function Home() {
  const scores = await getScores()

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Hero */}
      <section className="border-b border-zinc-800">
        <div className="max-w-6xl mx-auto px-6 py-20 md:py-28">
          <h1 className="text-4xl md:text-6xl font-bold text-white tracking-tight mb-4">
            Claude Bench
          </h1>
          <p className="text-lg md:text-xl text-zinc-400 mb-8 max-w-2xl">
            Score your Claude Code setup across 9 dimensions.
            See how your agents, memory, skills, and infrastructure stack up.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 font-mono text-sm text-zinc-300 flex items-center gap-3">
              <span className="text-zinc-600 select-none">$</span>
              <code>pip install claude-bench && claude-bench</code>
            </div>
            <a
              href="https://github.com/Evilent4/claude-bench"
              className="inline-flex items-center justify-center h-12 px-6 rounded-lg border border-zinc-700 text-zinc-300 hover:text-white hover:border-zinc-500 transition-colors text-sm font-medium"
            >
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="border-b border-zinc-800">
        <div className="max-w-6xl mx-auto px-6 py-16">
          <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider mb-8">
            How it works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="text-2xl font-mono text-emerald-500 mb-2">01</div>
              <h3 className="text-lg font-semibold text-zinc-200 mb-2">Scan</h3>
              <p className="text-sm text-zinc-500">
                Run the CLI on your Claude Code setup. It reads your agents, rules, hooks, skills,
                memory, and MCP configuration.
              </p>
            </div>
            <div>
              <div className="text-2xl font-mono text-emerald-500 mb-2">02</div>
              <h3 className="text-lg font-semibold text-zinc-200 mb-2">Score</h3>
              <p className="text-sm text-zinc-500">
                Get scored across 9 dimensions with a total out of 100.
                Each dimension measures a specific aspect of your setup maturity.
              </p>
            </div>
            <div>
              <div className="text-2xl font-mono text-emerald-500 mb-2">03</div>
              <h3 className="text-lg font-semibold text-zinc-200 mb-2">Compare</h3>
              <p className="text-sm text-zinc-500">
                Submit your score to the leaderboard and see how you stack up
                against other Claude Code setups worldwide.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Leaderboard */}
      <section>
        <div className="max-w-6xl mx-auto px-6 py-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-sm font-medium text-zinc-500 uppercase tracking-wider">
              Leaderboard
            </h2>
            <span className="text-xs text-zinc-600 font-mono">
              {scores.length} {scores.length === 1 ? 'setup' : 'setups'} scored
            </span>
          </div>
          {scores.length > 0 ? (
            <LeaderboardTable scores={scores} />
          ) : (
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-12 text-center">
              <p className="text-zinc-500 mb-2">No scores yet.</p>
              <p className="text-sm text-zinc-600">
                Be the first &mdash; run{' '}
                <code className="font-mono text-zinc-400">claude-bench --submit --name your-handle</code>
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800">
        <div className="max-w-6xl mx-auto px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="text-sm text-zinc-600">Claude Bench</span>
          <div className="flex items-center gap-6 text-sm text-zinc-600">
            <a href="https://github.com/Evilent4/claude-bench" className="hover:text-zinc-400 transition-colors">
              GitHub
            </a>
            <a href="/submit" className="hover:text-zinc-400 transition-colors">
              Submit Score
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
