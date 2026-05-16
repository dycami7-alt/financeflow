import { useEffect, useState } from "react"
import AuthPanel from "@/components/auth-panel"
import ChatAssistant from "@/components/chat-assistant"
import Dashboard from "@/components/dashboard"
import FinancialGraphs from "@/components/financial-graphs"
import MiniFinanceGame from "@/components/mini-finance-game"
import StreakDisplay from "@/components/streak-display"
import FinancialProfiler from "@/components/financial-profiler"

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export default function App() {
  const [activeTab, setActiveTab] = useState<"auth" | "chat" | "dashboard" | "graphs" | "game" | "profiler">("dashboard")
  const [currentStreak, setCurrentStreak] = useState(12)
  const [bestStreak] = useState(42)
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)
  const [authMessage, setAuthMessage] = useState<string | null>(null)

  const saveSession = (access: string, refresh: string, email: string) => {
    setAccessToken(access)
    setRefreshToken(refresh)
    setUserEmail(email)
    localStorage.setItem("financeflow_access_token", access)
    localStorage.setItem("financeflow_refresh_token", refresh)
  }

  const clearSession = () => {
    setAccessToken(null)
    setRefreshToken(null)
    setUserEmail(null)
    setAuthMessage(null)
    localStorage.removeItem("financeflow_access_token")
    localStorage.removeItem("financeflow_refresh_token")
  }

  const handleAuthSuccess = (access: string, refresh: string, email: string) => {
    saveSession(access, refresh, email)
    setActiveTab("dashboard")
    setAuthMessage(`Bienvenido, ${email}`)
  }

  const fetchCurrentUser = async (token: string) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (!response.ok) throw new Error("Token inválido")
    const data = await response.json()
    return data.email as string
  }

  const refreshSession = async (refresh: string) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refresh }),
    })
    if (!response.ok) throw new Error("Refresh token inválido")
    const data = await response.json()
    return data
  }

  useEffect(() => {
    const restoreAuth = async () => {
      const storedAccess = localStorage.getItem("financeflow_access_token")
      const storedRefresh = localStorage.getItem("financeflow_refresh_token")
      if (!storedAccess && !storedRefresh) return

      try {
        if (storedAccess) {
          const email = await fetchCurrentUser(storedAccess)
          saveSession(storedAccess, storedRefresh ?? "", email)
          return
        }
      } catch {
        if (storedRefresh) {
          try {
            const data = await refreshSession(storedRefresh)
            const email = await fetchCurrentUser(data.access_token)
            saveSession(data.access_token, data.refresh_token, email)
            return
          } catch {
            clearSession()
          }
        }
      }
    }

    restoreAuth()
  }, [])

  const handleLogout = () => {
    clearSession()
    setActiveTab("auth")
  }

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <header className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
              FinanceFlow
            </h1>
            <p className="text-xs text-muted-foreground mt-1">Tu asistente financiero inteligente</p>
          </div>
          <StreakDisplay currentStreak={currentStreak} bestStreak={bestStreak} />
        </div>
      </header>

      <div className="border-b border-border/50 bg-background/50 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap gap-2">
            {[
              { id: "chat", label: "Asistente", icon: "💬" },
              { id: "dashboard", label: "Panel", icon: "📋" },
              { id: "profiler", label: "Mi Perfil", icon: "🎯" },
              { id: "graphs", label: "Conceptos", icon: "📊" },
              { id: "game", label: "Juego", icon: "🎮" },
              { id: "auth", label: userEmail ? "Cuenta" : "Acceder", icon: "🔐" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() =>
                  setActiveTab(tab.id as "auth" | "chat" | "dashboard" | "graphs" | "game" | "profiler")
                }
                className={`px-4 py-4 font-medium transition-all border-b-2 text-sm sm:text-base ${
                  activeTab === tab.id
                    ? "border-cyan-400 text-cyan-400"
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
          <div className="hidden sm:flex flex-col items-end text-right">
            <span className="text-xs text-muted-foreground">{userEmail ? "Sesión activa" : "Invitado"}</span>
            <span className="text-sm text-foreground">
              {userEmail ?? "Inicia sesión para sincronizar tu progreso"}
            </span>
          </div>
        </div>
      </div>

      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
        {authMessage ? (
          <div className="mb-6 rounded-3xl border border-cyan-500/20 bg-cyan-500/5 p-4 text-sm text-cyan-600">
            {authMessage}
          </div>
        ) : null}
        {activeTab === "dashboard" && <Dashboard />}
        {activeTab === "chat" && <ChatAssistant onStreakUpdate={setCurrentStreak} />}
        {activeTab === "profiler" && <FinancialProfiler />}
        {activeTab === "graphs" && <FinancialGraphs />}
        {activeTab === "game" && <MiniFinanceGame onStreakUpdate={setCurrentStreak} />}
        {activeTab === "auth" && (
          <AuthPanel userEmail={userEmail} onAuthSuccess={handleAuthSuccess} onLogout={handleLogout} />
        )}
      </div>
    </main>
  )
}
