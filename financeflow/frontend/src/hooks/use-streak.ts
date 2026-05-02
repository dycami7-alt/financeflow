import { useState, useEffect } from 'react'

interface StreakData {
  current_streak: number
  best_streak: number
  total_actions: number
  last_action: string | null
  streak_percentage: number
}

export function useStreakData(userId: string) {
  const [streak, setStreak] = useState<StreakData>({
    current_streak: 0,
    best_streak: 0,
    total_actions: 0,
    last_action: null,
    streak_percentage: 0,
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStreakData = async () => {
    try {
      setLoading(true)
      const response = await fetch(
        `http://localhost:8000/api/rachas/stats/${userId}`
      )
      if (!response.ok) throw new Error('Error fetching streak data')
      const data = await response.json()
      setStreak(data.data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const updateStreak = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/rachas/update/${userId}`,
        {
          method: 'POST',
        }
      )
      if (!response.ok) throw new Error('Error updating streak')
      const data = await response.json()
      setStreak({
        current_streak: data.data.current_streak,
        best_streak: data.data.best_streak,
        total_actions: data.data.total_actions,
        last_action: data.data.last_action_date,
        streak_percentage: 0,
      })
      return data.data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  const resetStreak = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/rachas/reset/${userId}`,
        {
          method: 'POST',
        }
      )
      if (!response.ok) throw new Error('Error resetting streak')
      await fetchStreakData()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  useEffect(() => {
    if (userId) {
      fetchStreakData()
    }
  }, [userId])

  return {
    streak,
    loading,
    error,
    updateStreak,
    resetStreak,
    refetch: fetchStreakData,
  }
}
