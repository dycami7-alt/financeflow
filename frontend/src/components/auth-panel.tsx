import { FormEvent, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

const AUTH_API_BASE = (import.meta.env.VITE_API_URL ?? "http://localhost:8000") as string

interface AuthPanelProps {
  userEmail: string | null
  onAuthSuccess: (accessToken: string, refreshToken: string, email: string) => void
  onLogout: () => void
}

export default function AuthPanel({ userEmail, onAuthSuccess, onLogout }: AuthPanelProps) {
  const [mode, setMode] = useState<"login" | "register">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const submitLabel = mode === "login" ? "Ingresar" : "Crear cuenta"
  const alternateLabel =
    mode === "login"
      ? "¿No tienes cuenta? Regístrate"
      : "¿Ya tienes cuenta? Inicia sesión"
  const endpoint = mode === "login" ? "login" : "register"

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const response = await fetch(`${AUTH_API_BASE}/api/auth/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()
      if (!response.ok) {
        setMessage(data.detail || "Ocurrió un error al procesar tu solicitud.")
        return
      }

      onAuthSuccess(data.access_token, data.refresh_token, data.email ?? email)
      setMessage(
        mode === "login"
          ? "Has iniciado sesión correctamente."
          : "Cuenta creada con éxito. Bienvenido."
      )
      setPassword("")
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "No se pudo conectar con el servidor."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 rounded-3xl border border-border/50 bg-card/80 p-8 shadow-xl shadow-black/5 float-up">
      <div className="flex flex-col gap-2">
        <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">Cuenta segura</p>
        <h1 className="text-3xl font-bold">Accede a tu cuenta de FinanceFlow</h1>
        <p className="max-w-2xl text-base leading-7 text-muted-foreground">
          Regístrate o inicia sesión para sincronizar tu progreso, metas y desafíos en todos tus dispositivos.
        </p>
      </div>

      {userEmail ? (
        <div className="rounded-3xl border border-cyan-500/20 bg-cyan-500/5 p-6">
          <p className="text-sm text-muted-foreground">Sesión activa</p>
          <p className="mt-3 text-xl font-semibold text-foreground">{userEmail}</p>
          <p className="mt-2 text-sm text-muted-foreground">
            Ahora puedes acceder a tus gráficos, metas y rachas con tu usuario.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button variant="secondary" type="button" onClick={onLogout}>
              Cerrar sesión
            </Button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-medium text-foreground">Correo electrónico</span>
              <Input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="tucorreo@ejemplo.com"
                required
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-foreground">Contraseña</span>
              <Input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••••"
                required
                minLength={8}
              />
            </label>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <Button type="submit" className="w-full sm:w-auto" disabled={loading}>
              {loading ? "Procesando..." : submitLabel}
            </Button>
            <button
              type="button"
              className="text-sm text-muted-foreground hover:text-foreground"
              onClick={() => setMode(mode === "login" ? "register" : "login")}
            >
              {alternateLabel}
            </button>
          </div>

          {message ? (
            <div className="rounded-2xl border border-border/50 bg-muted/10 p-4 text-sm text-foreground">
              {message}
            </div>
          ) : null}
        </form>
      )}
    </div>
  )
}
