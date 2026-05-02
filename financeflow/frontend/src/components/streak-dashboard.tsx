import { useState, useEffect } from 'react'
import { useStreakData } from '@/hooks/use-streak'

interface StreakedashboardProps {
  userId?: string
}

export function StreakDashboard({ userId = 'default-user' }: StreakedashboardProps) {
  const { streak, loading, error, updateStreak, refetch } =
    useStreakData(userId)
  const [showDetails, setShowDetails] = useState(false)
  const [notificationMessage, setNotificationMessage] = useState('')

  const handleQuickAction = async () => {
    const result = await updateStreak()
    if (result) {
      setNotificationMessage('¡Has ganado puntos en tu racha! 🎊')
      setTimeout(() => setNotificationMessage(''), 3000)
      refetch()
    }
  }

  const getStreakLevel = (streak: number): string => {
    if (streak === 0) return 'Sin racha'
    if (streak < 5) return 'Principiante'
    if (streak < 15) return 'Consistente'
    if (streak < 30) return 'Impresionante'
    return 'Legendario'
  }

  const getStreakColor = (streak: number): string => {
    if (streak === 0) return 'text-gray-400'
    if (streak < 5) return 'text-yellow-400'
    if (streak < 15) return 'text-cyan-400'
    if (streak < 30) return 'text-purple-400'
    return 'text-red-400'
  }

  if (loading) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-700 rounded-lg">
        <div className="animate-pulse space-y-4">
          <div className="h-12 bg-slate-700 rounded"></div>
          <div className="h-20 bg-slate-700 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 space-y-6 rounded-lg">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">Tu Racha</h2>
        <span className={`text-sm font-semibold px-3 py-1 rounded-full bg-slate-700 ${getStreakColor(streak.current_streak)}`}>
          {getStreakLevel(streak.current_streak)}
        </span>
      </div>

      {/* Main Stats */}
      <div className="grid grid-cols-2 gap-4">
        {/* Current Streak */}
        <div className="bg-slate-800/50 rounded-lg p-4 border border-cyan-500/20">
          <p className="text-xs text-gray-400 mb-2">Racha Actual</p>
          <div className="flex items-center gap-2">
            <span className="text-4xl">🔥</span>
            <div>
              <p className="text-3xl font-bold text-cyan-400">
                {streak.current_streak}
              </p>
              <p className="text-xs text-gray-400">días seguidos</p>
            </div>
          </div>
        </div>

        {/* Best Streak */}
        <div className="bg-slate-800/50 rounded-lg p-4 border border-purple-500/20">
          <p className="text-xs text-gray-400 mb-2">Mejor Racha</p>
          <div className="flex items-center gap-2">
            <span className="text-4xl">🏆</span>
            <div>
              <p className="text-3xl font-bold text-purple-400">
                {streak.best_streak}
              </p>
              <p className="text-xs text-gray-400">tu récord</p>
            </div>
          </div>
        </div>
      </div>

      {/* Progress */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Progreso hacia el siguiente nivel</span>
          <span className="text-cyan-400 font-semibold">
            {streak.current_streak} / {(streak.best_streak || 1) + 5}
          </span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
          <div
            className="bg-gradient-to-r from-cyan-500 to-cyan-400 h-full transition-all duration-500"
            style={{
              width: `${Math.min(
                (streak.current_streak / ((streak.best_streak || 1) + 5)) * 100,
                100
              )}%`,
            }}
          />
        </div>
      </div>

      {/* Details Toggle */}
      {showDetails && (
        <div className="space-y-3 pt-4 border-t border-slate-700">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-gray-400">Total de Acciones</p>
              <p className="text-lg font-semibold text-white">
                {streak.total_actions}
              </p>
            </div>
            <div>
              <p className="text-gray-400">Última Acción</p>
              <p className="text-lg font-semibold text-white">
                {streak.last_action
                  ? new Date(streak.last_action).toLocaleDateString('es-ES', {
                    month: 'short',
                    day: 'numeric',
                  })
                  : 'Nunca'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 pt-4 border-t border-slate-700">
        <button
          onClick={handleQuickAction}
          className="flex-1 bg-cyan-600 hover:bg-cyan-700 text-white font-semibold py-2 px-4 rounded"
        >
          ✨ Actualizar Racha
        </button>
        <button
          className="px-4 py-2 border border-slate-600 hover:bg-slate-700 text-white rounded font-medium"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Ocultar' : 'Detalles'}
        </button>
      </div>

      {/* Notification */}
      {notificationMessage && (
        <div className="bg-cyan-500/20 border border-cyan-500 rounded-lg p-3 text-center text-cyan-300 animate-pulse text-sm">
          {notificationMessage}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-500/20 border border-red-500 rounded-lg p-3 text-center text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Tips */}
      <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
        <p className="text-xs font-semibold text-gray-400 mb-2">💡 Consejo:</p>
        <p className="text-xs text-gray-400 leading-relaxed">
          {streak.current_streak === 0
            ? 'Comienza tu racha completando una acción hoy mismo.'
            : streak.current_streak < 5
            ? 'Sigue adelante, cada día cuenta!'
            : 'Vas muy bien, no rompas tu racha!'}
        </p>
      </div>
    </div>
  )
}
