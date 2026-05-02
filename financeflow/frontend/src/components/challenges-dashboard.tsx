import { useState } from "react"
import { Button } from "@/components/ui/button"

interface Challenge {
  id: number
  title: string
  description: string
  difficulty: "Fácil" | "Medio" | "Difícil"
  duration: string
  xp: number
  progress: number
  completed: boolean
}

interface UserProfile {
  profileType: string
}

interface ChallengesDashboardProps {
  profile: UserProfile
}

const CHALLENGES_BY_PROFILE: Record<string, Challenge[]> = {
  Conservative: [
    {
      id: 1,
      title: "Presupuesto Maestro",
      description: "Crea un presupuesto detallado y síguelo por 7 días",
      difficulty: "Fácil",
      duration: "7 días",
      xp: 50,
      progress: 0,
      completed: false,
    },
    {
      id: 2,
      title: "Reto de Ahorro Agresivo",
      description: "Ahorra 30% de tus ingresos durante 30 días",
      difficulty: "Medio",
      duration: "30 días",
      xp: 200,
      progress: 0,
      completed: false,
    },
    {
      id: 3,
      title: "Investidor Novato",
      description: "Investiga 3 opciones de inversión y crea un plan",
      difficulty: "Difícil",
      duration: "14 días",
      xp: 150,
      progress: 0,
      completed: false,
    },
  ],
  Moderate: [
    {
      id: 1,
      title: "Balance Perfecto",
      description: "Mantén el balance 50/30/20 durante 2 semanas",
      difficulty: "Fácil",
      duration: "14 días",
      xp: 100,
      progress: 0,
      completed: false,
    },
    {
      id: 2,
      title: "Sin Gastos Impulsivos",
      description: "Evita gastos impulsivos durante 21 días",
      difficulty: "Medio",
      duration: "21 días",
      xp: 180,
      progress: 0,
      completed: false,
    },
    {
      id: 3,
      title: "Fondo de Emergencia",
      description: "Crea y completa tu fondo de emergencia (1 mes gastos)",
      difficulty: "Difícil",
      duration: "60 días",
      xp: 300,
      progress: 0,
      completed: false,
    },
  ],
  Aggressive: [
    {
      id: 1,
      title: "Disciplina 101",
      description: "Sigue un presupuesto durante 7 días",
      difficulty: "Fácil",
      duration: "7 días",
      xp: 75,
      progress: 0,
      completed: false,
    },
    {
      id: 2,
      title: "Proyecto de Inversión",
      description: "Realiza tu primera inversión (aunque sea pequeña)",
      difficulty: "Medio",
      duration: "30 días",
      xp: 250,
      progress: 0,
      completed: false,
    },
    {
      id: 3,
      title: "Multiplicador de Dinero",
      description: "Crea un flujo de ingresos secundario (vender cosas, freelance)",
      difficulty: "Difícil",
      duration: "45 días",
      xp: 400,
      progress: 0,
      completed: false,
    },
  ],
}

export default function ChallengesDashboard({ profile }: ChallengesDashboardProps) {
  const [challenges, setChallenges] = useState<Challenge[]>(CHALLENGES_BY_PROFILE[profile.profileType] || [])
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null)

  const getDifficultyColor = (difficulty: string) => {
    const colorMap: Record<string, string> = {
      Fácil: "bg-green-500/20 text-green-300 border-green-500/50",
      Medio: "bg-yellow-500/20 text-yellow-300 border-yellow-500/50",
      Difícil: "bg-red-500/20 text-red-300 border-red-500/50",
    }
    return colorMap[difficulty] || ""
  }

  const handleUpdateProgress = (amount: number) => {
    if (selectedChallenge) {
      const newProgress = Math.min(100, selectedChallenge.progress + amount)
      const updated = { ...selectedChallenge, progress: newProgress, completed: newProgress === 100 }
      setSelectedChallenge(updated)
      setChallenges(challenges.map((c) => (c.id === updated.id ? updated : c)))
    }
  }

  const totalXP = challenges.reduce((sum, c) => sum + (c.completed ? c.xp : 0), 0)

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
          Tus Retos Personalizados
        </h2>
        <p className="text-muted-foreground">Completa desafíos tipo Duolingo y aprende ganando XP</p>
      </div>

      <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-xl p-6 flex justify-between items-center">
        <div>
          <p className="text-sm text-muted-foreground">Total XP Acumulado</p>
          <p className="text-3xl font-bold text-cyan-400">{totalXP} XP</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted-foreground">Retos Completados</p>
          <p className="text-3xl font-bold text-purple-400">
            {challenges.filter((c) => c.completed).length}/{challenges.length}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {challenges.map((challenge) => (
          <div
            key={challenge.id}
            className={`p-4 rounded-xl border transition-all cursor-pointer ${
              challenge.completed
                ? "bg-green-900/20 border-green-500/50"
                : "bg-slate-800/50 border-slate-700/50 hover:border-purple-500/50"
            }`}
            onClick={() => setSelectedChallenge(challenge)}
          >
            <div className="flex justify-between items-start mb-3">
              <h3 className="font-bold text-white">{challenge.title}</h3>
              <span className={`px-3 py-1 rounded-full text-xs border ${getDifficultyColor(challenge.difficulty)}`}>
                {challenge.difficulty}
              </span>
            </div>

            <p className="text-sm text-muted-foreground mb-4">{challenge.description}</p>

            <div className="space-y-2">
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-purple-600 to-cyan-600 transition-all"
                  style={{ width: `${challenge.progress}%` }}
                />
              </div>

              <div className="flex justify-between text-xs text-muted-foreground">
                <span>{challenge.duration}</span>
                <span>{challenge.xp} XP</span>
              </div>
            </div>

            {challenge.completed && <p className="text-green-400 text-xs font-bold mt-2">{"✓ COMPLETADO"}</p>}
          </div>
        ))}
      </div>

      {selectedChallenge && (
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-purple-500/30 rounded-xl p-6 space-y-4">
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">{selectedChallenge.title}</h3>
            <p className="text-muted-foreground">{selectedChallenge.description}</p>
          </div>

          <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
            <p className="font-semibold text-white">Progreso: {selectedChallenge.progress}%</p>
            <div className="w-full h-3 bg-slate-600 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-600 to-cyan-600 transition-all"
                style={{ width: `${selectedChallenge.progress}%` }}
              />
            </div>
          </div>

          {selectedChallenge.progress < 100 && (
            <div className="grid grid-cols-3 gap-2">
              <Button onClick={() => handleUpdateProgress(10)} className="bg-blue-600 hover:bg-blue-700">
                +10%
              </Button>
              <Button onClick={() => handleUpdateProgress(25)} className="bg-purple-600 hover:bg-purple-700">
                +25%
              </Button>
              <Button onClick={() => handleUpdateProgress(50)} className="bg-cyan-600 hover:bg-cyan-700">
                Completar
              </Button>
            </div>
          )}

          {selectedChallenge.completed && (
            <div className="bg-green-900/30 border border-green-500/50 rounded-lg p-4 text-center space-y-2">
              <p className="text-2xl">🎉</p>
              <p className="font-bold text-green-400">{"¡Reto Completado!"}</p>
              <p className="text-sm text-muted-foreground">+{selectedChallenge.xp} XP ganados</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
