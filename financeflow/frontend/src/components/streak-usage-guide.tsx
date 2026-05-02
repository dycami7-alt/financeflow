/**
 * GUÍA DE USO DEL MÓDULO DE RACHAS
 * 
 * Este archivo muestra cómo integrar y usar el módulo de rachas en tu aplicación.
 */

// ============================================
// 1. USANDO EL HOOK (Recomendado)
// ============================================

import { useStreakData } from '@/hooks/use-streak'

function MyComponent() {
  const userId = 'user-123' // Reemplaza con el ID del usuario actual
  
  const {
    streak,           // Objeto con current_streak, best_streak, etc.
    loading,          // Booleano - cargando datos
    error,           // Mensaje de error si hay
    updateStreak,    // Función para actualizar la racha
    resetStreak,     // Función para reiniciar la racha
    refetch,         // Función para recargar los datos
  } = useStreakData(userId)

  // Ejemplo de uso en un evento
  const handleCompletedChallenge = async () => {
    await updateStreak() // Incrementa la racha
  }

  return (
    <div>
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <>
          <p>Racha actual: {streak.current_streak} 🔥</p>
          <p>Mejor racha: {streak.best_streak} 🏆</p>
          <button onClick={handleCompletedChallenge}>
            Completar desafío
          </button>
        </>
      )}
    </div>
  )
}

// ============================================
// 2. COMPONENTES LISTOS PARA USAR
// ============================================

// Componente simple (solo muestra los números)
import StreakDisplay from '@/components/streak-display'

function SimpleView() {
  return <StreakDisplay userId="user-123" autoUpdate={true} />
}

// Componente completo con dashboard
import { StreakDashboard } from '@/components/streak-dashboard'

function FullView() {
  return <StreakDashboard userId="user-123" />
}

// ============================================
// 3. ENDPOINTS API DISPONIBLES
// ============================================

/**
 * GET /api/rachas/stats/{user_id}
 * Obtiene estadísticas completas de racha
 * 
 * Response:
 * {
 *   "success": true,
 *   "data": {
 *     "current_streak": 5,
 *     "best_streak": 12,
 *     "total_actions": 48,
 *     "last_action": "2024-04-25",
 *     "streak_percentage": 41.67
 *   }
 * }
 */

/**
 * POST /api/rachas/update/{user_id}
 * Actualiza la racha cuando el usuario completa una acción
 * 
 * Response:
 * {
 *   "success": true,
 *   "message": "Racha actualizada",
 *   "data": {
 *     "user_id": "user-123",
 *     "current_streak": 6,
 *     "best_streak": 12,
 *     ...
 *   }
 * }
 */

/**
 * GET /api/rachas/{user_id}
 * Obtiene la información actual de racha
 */

/**
 * POST /api/rachas/reset/{user_id}
 * Reinicia la racha actual (mantiene el mejor record)
 */

// ============================================
// 4. LÓGICA DE RACHA EXPLICADA
// ============================================

/**
 * La racha se actualiza según estos criterios:
 * 
 * 1. PRIMERA VEZ:
 *    - current_streak = 1
 *    - best_streak = 1
 * 
 * 2. MISMO DÍA:
 *    - No cambia la racha (evita spam de acciones)
 * 
 * 3. DÍA SIGUIENTE:
 *    - current_streak += 1
 *    - Si current_streak > best_streak, actualiza best_streak
 * 
 * 4. MÁS DE 1 DÍA SIN ACTIVIDAD:
 *    - current_streak = 1 (se reinicia)
 *    - best_streak se mantiene (es el récord)
 */

// ============================================
// 5. EJEMPLO COMPLETO EN UN DASHBOARD
// ============================================

import React from 'react'
import { StreakDashboard } from '@/components/streak-dashboard'
import { useStreakData } from '@/hooks/use-streak'

export function CompleteDashboard() {
  const userId = 'current-user-id'
  const { updateStreak } = useStreakData(userId)

  const handleChallengeComplete = async () => {
    // Aquí va tu lógica de desafío
    // ...
    
    // Al completar, actualiza la racha
    await updateStreak()
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Panel de Racha */}
      <div className="lg:col-span-1">
        <StreakDashboard userId={userId} />
      </div>

      {/* Otros componentes del dashboard */}
      <div className="lg:col-span-2">
        <div className="space-y-4">
          {/* Desafíos, juegos, etc. */}
          <button
            onClick={handleChallengeComplete}
            className="w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 rounded-lg"
          >
            Completar Desafío
          </button>
        </div>
      </div>
    </div>
  )
}

export default CompleteDashboard
