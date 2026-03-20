import { LeaderboardTable } from '@/components/leaderboard-table'
import { InstallBlock } from '@/components/install-block'
import { getScores } from '@/lib/supabase'

export const revalidate = 60

export default async function Home() {
  const scores = await getScores()

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Hero + How it works combined */}
      <section className="border-b border-zinc-800">
        <div className="max-w-6xl mx-auto px-6 py-12 md:py-16">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-10">
            <div className="max-w-2xl">
              <h1 className="text-3xl md:text-5xl font-bold text-white tracking-tight mb-3">
                Claude Bench
              </h1>
              <p className="text-base md:text-lg text-zinc-400">
                Score your Claude Code setup across 9 dimensions.
              </p>
            </div>
            <a
              href="https://github.com/Evilent4/claude-bench"
              className="shrink-0 inline-flex items-center justify-center h-10 px-5 rounded-lg border border-zinc-700 text-zinc-300 hover:text-white hover:border-zinc-500 transition-colors text-sm font-medium"
            >
              View on GitHub
            </a>
          </div>

          <div className="mb-10 max-w-xl">
            <InstallBlock />
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="flex gap-3">
              <span className="text-lg font-mono text-emerald-500 shrink-0">01</span>
              <div>
                <h3 className="text-sm font-semibold text-zinc-200 mb-1">Scan</h3>
                <p className="text-xs text-zinc-500">
                  Run the CLI on your Claude Code setup. It reads agents, rules, hooks, skills, memory, and MCP config.
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-lg font-mono text-emerald-500 shrink-0">02</span>
              <div>
                <h3 className="text-sm font-semibold text-zinc-200 mb-1">Score</h3>
                <p className="text-xs text-zinc-500">
                  Get scored across 9 dimensions with a total out of 100. Each measures a specific aspect of your setup.
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <span className="text-lg font-mono text-emerald-500 shrink-0">03</span>
              <div>
                <h3 className="text-sm font-semibold text-zinc-200 mb-1">Compare</h3>
                <p className="text-xs text-zinc-500">
                  Submit your score to the leaderboard and see how you stack up against other setups worldwide.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Leaderboard */}
      <section>
        <div className="max-w-6xl mx-auto px-6 py-10">
          <div className="flex items-center justify-between mb-6">
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
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-10 text-center">
              <p className="text-zinc-500 mb-1">No scores yet.</p>
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
        <div className="max-w-6xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
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
