interface Goal {
  id: number
  title: string
  description: string
  deadline: string
  progress: number
  target: string
  status: "En curso" | "Completado" | "Pendiente"
  badge: string
}

const GOALS: Goal[] = [
  {
    id: 1,
    title: "Ahorra tu primer fondo de emergencia",
    description: "Acumula $500 en 30 días para cubrir imprevistos.",
    deadline: "30 días",
    progress: 65,
    target: "$500",
    status: "En curso",
    badge: "Fondo seguro",
  },
  {
    id: 2,
    title: "Presupuesto 50/30/20",
    description: "Organiza tus gastos y mantén el balance durante 7 días.",
    deadline: "7 días",
    progress: 100,
    target: "Balanceado",
    status: "Completado",
    badge: "Maestro del presupuesto",
  },
  {
    id: 3,
    title: "Tu primera inversión inteligente",
    description: "Aprende sobre fondos indexados y define una estrategia.",
    deadline: "15 días",
    progress: 40,
    target: "Plan listo",
    status: "En curso",
    badge: "Inversor novato",
  },
]

export default function GoalsPanel() {
  return (
    <div className="space-y-6 float-up">
      <div className="bg-card border border-border/50 rounded-xl p-6 float-up">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Metas Financieras</p>
            <h2 className="text-3xl font-bold">Avanza con objetivos claros</h2>
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            <div className="bg-slate-950/60 border border-slate-700 rounded-2xl p-4 text-center">
              <p className="text-xs uppercase text-muted-foreground">Metas activas</p>
              <p className="text-2xl font-bold text-cyan-400">2</p>
            </div>
            <div className="bg-slate-950/60 border border-slate-700 rounded-2xl p-4 text-center">
              <p className="text-xs uppercase text-muted-foreground">Completadas</p>
              <p className="text-2xl font-bold text-green-400">1</p>
            </div>
            <div className="bg-slate-950/60 border border-slate-700 rounded-2xl p-4 text-center">
              <p className="text-xs uppercase text-muted-foreground">XP estimada</p>
              <p className="text-2xl font-bold text-purple-400">520</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {GOALS.map((goal) => (
          <div
            key={goal.id}
            className={`rounded-3xl border p-5 shadow-sm transition hover:-translate-y-1 float-up ${
              goal.status === "Completado"
                ? "border-green-500/30 bg-green-950/20"
                : "border-slate-700 bg-slate-950/80"
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{goal.deadline}</p>
                <h3 className="mt-2 text-lg font-semibold text-white">{goal.title}</h3>
              </div>
              <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-muted-foreground">{goal.status}</span>
            </div>

            <p className="mt-4 text-sm leading-6 text-muted-foreground">{goal.description}</p>

            <div className="mt-5 space-y-3">
              <div className="flex items-center justify-between text-xs uppercase text-muted-foreground">
                <span>{goal.progress}% completado</span>
                <span>{goal.target}</span>
              </div>
              <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-500 to-cyan-500" style={{ width: `${goal.progress}%` }} />
              </div>
            </div>

            <div className="mt-5 rounded-2xl border border-slate-700 bg-slate-900/70 p-4 text-sm text-muted-foreground">
              <p className="font-semibold text-white">Insignia:</p>
              <p>{goal.badge}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
