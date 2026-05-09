import { useEffect, useState } from 'react'
import { useStreakData } from '@/hooks/use-streak'

interface StreakDisplayProps {
  userId?: string
  autoUpdate?: boolean
}

export default function StreakDisplay({
  userId = 'default-user',
  autoUpdate = false,
}: StreakDisplayProps) {
  const { streak, loading, error, updateStreak, resetStreak, refetch } =
    useStreakData(userId)
  const [updateMessage, setUpdateMessage] = useState<string>('')

  const handleUpdateStreak = async () => {
    const result = await updateStreak()
    if (result) {
      setUpdateMessage('¡Racha actualizada! 🎉')
      setTimeout(() => setUpdateMessage(''), 2000)
    }
  }

  useEffect(() => {
    if (autoUpdate) {
      const interval = setInterval(refetch, 60000) // Actualizar cada minuto
      return () => clearInterval(interval)
    }
  }, [autoUpdate, refetch])

  if (loading) {
    return (
      <div className="h-20 w-full bg-slate-700 rounded animate-pulse" />
    )
  }

  if (error) {
    return (
      <div className="text-red-500 text-sm">Error: {error}</div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-6 p-4 rounded-lg bg-gradient-to-r from-slate-900 to-slate-800 border border-cyan-500/20">
        <div className="flex-1">
          <p className="text-xs text-muted-foreground mb-1">Racha Actual</p>
          <div className="text-3xl font-bold text-cyan-400 streak-pulse flex items-center gap-2">
            <span>🔥</span>
            {streak.current_streak}
          </div>
          {streak.last_action && (
            <p className="text-xs text-muted-foreground mt-1">
              Última: {new Date(streak.last_action).toLocaleDateString()}
            </p>
          )}
        </div>

        <div className="h-12 w-px bg-border/50"></div>

        <div className="flex-1">
          <p className="text-xs text-muted-foreground mb-1">Mejor Racha</p>
          <div className="text-2xl font-bold text-purple-400 flex items-center gap-2">
            <span>🏆</span>
            {streak.best_streak}
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Total: {streak.total_actions} acciones
          </p>
        </div>
      </div>

      <div className="flex gap-2 justify-end">
        <button
          onClick={handleUpdateStreak}
          className="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded text-sm font-medium"
        >
          Actualizar Racha
        </button>
        <button
          onClick={resetStreak}
          className="bg-transparent border border-red-400 text-red-400 hover:bg-red-400/10 px-4 py-2 rounded text-sm font-medium"
        >
          Reiniciar
        </button>
      </div>

      {updateMessage && (
        <p className="text-center text-sm text-cyan-400 animate-pulse">
          {updateMessage}
        </p>
      )}
    </div>
  )
}

