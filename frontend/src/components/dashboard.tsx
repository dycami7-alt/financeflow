import ChallengesDashboard from "@/components/challenges-dashboard"
import FinancialGraphs from "@/components/financial-graphs"
import GoalsPanel from "@/components/goals-panel"

const MOCK_PROFILE = { profileType: "Moderate" }

export default function Dashboard() {
  return (
    <div className="space-y-10 float-up">
      <section className="rounded-3xl border border-border/50 bg-card/80 p-8 shadow-xl shadow-black/5 float-up">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-3">
            <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">Panel de Control</p>
            <h1 className="text-4xl font-bold neon-text">Tu tablero financiero tipo Duolingo</h1>
            <p className="max-w-2xl text-base leading-7 text-muted-foreground">
              Aprende con gráficas educativas, metas claras y desafíos diarios para mejorar tus decisiones de dinero.
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-3xl border border-slate-700/80 bg-slate-950/80 p-5 text-center animate-pulse">
              <p className="text-sm text-muted-foreground">Racha actual</p>
              <p className="mt-3 text-3xl font-bold text-cyan-400">12</p>
            </div>
            <div className="rounded-3xl border border-slate-700/80 bg-slate-950/80 p-5 text-center animate-pulse">
              <p className="text-sm text-muted-foreground">XP acumulada</p>
              <p className="mt-3 text-3xl font-bold text-purple-400">520</p>
            </div>
            <div className="rounded-3xl border border-slate-700/80 bg-slate-950/80 p-5 text-center animate-pulse">
              <p className="text-sm text-muted-foreground">Retos completados</p>
              <p className="mt-3 text-3xl font-bold text-green-400">3</p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-8 xl:grid-cols-[1.4fr_0.9fr]">
        <div className="space-y-8">
          <div className="rounded-3xl border border-border/50 bg-card/80 p-6">
            <div className="flex items-center justify-between gap-4 mb-6">
              <div>
                <p className="text-sm text-muted-foreground">Gráficas educativas</p>
                <h2 className="text-2xl font-bold">Visualiza conceptos clave</h2>
              </div>
            </div>
            <FinancialGraphs />
          </div>

          <div className="rounded-3xl border border-border/50 bg-card/80 p-6">
            <GoalsPanel />
          </div>
        </div>

        <div className="space-y-8">
          <div className="rounded-3xl border border-border/50 bg-card/80 p-6">
            <div className="mb-6">
              <p className="text-sm text-muted-foreground">Desafíos tipo Duolingo</p>
              <h2 className="text-2xl font-bold">Completa misiones financieras</h2>
            </div>
            <ChallengesDashboard profile={MOCK_PROFILE} />
          </div>
        </div>
      </section>
    </div>
  )
}
