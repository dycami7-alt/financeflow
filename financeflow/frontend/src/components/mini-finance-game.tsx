import { useState } from "react"
import { Button } from "@/components/ui/button"

interface GameScenario {
  id: number
  pregunta: string
  opciones: { texto: string; correcta: boolean; explicacion: string }[]
  contexto: string
}

const GAME_SCENARIOS: GameScenario[] = [
  {
    id: 1,
    contexto: "Recibes $100 como mesada",
    pregunta: "¿Cómo deberías dividirlo según la regla 50/30/20?",
    opciones: [
      {
        texto: "$50 necesidades, $30 diversión, $20 ahorros",
        correcta: true,
        explicacion: "✓ Correcto! Esta es la regla de oro: 50% necesario, 30% placer, 20% ahorro.",
      },
      {
        texto: "$70 diversión, $30 ahorros",
        correcta: false,
        explicacion: "✗ No es ideal. Necesitas cubrir tus necesidades primero.",
      },
      {
        texto: "$100 en un videojuego",
        correcta: false,
        explicacion: "✗ Eso es impulsivo. Los jóvenes ricos planifican sus gastos.",
      },
    ],
  },
  {
    id: 2,
    contexto: "Ves ropa que te encanta en una tienda",
    pregunta: "¿Qué haces?",
    opciones: [
      {
        texto: "Espero 24 horas antes de decidir",
        correcta: true,
        explicacion: "✓ Excelente! El 80% de compras impulsivas se olvidan en 24h.",
      },
      {
        texto: "La compro inmediatamente",
        correcta: false,
        explicacion: "✗ Las compras impulsivas son enemigas del ahorro.",
      },
      {
        texto: "Pido dinero prestado a mis amigos",
        correcta: false,
        explicacion: "✗ Nunca endeudarse para cosas que no necesitas.",
      },
    ],
  },
  {
    id: 3,
    contexto: "Tienes $50 y quieres invertir",
    pregunta: "¿Cuál es la opción más inteligente?",
    opciones: [
      {
        texto: "Fondos indexados o fondos mutuales",
        correcta: true,
        explicacion: "✓ Bien! El riesgo se divide y tienes ~8% anual de retorno histórico.",
      },
      {
        texto: "Guardar todo en criptomonedas",
        correcta: false,
        explicacion: "✗ Muy arriesgado para principiantes. Diversifica siempre.",
      },
      {
        texto: "Dejarlo en el colchón",
        correcta: false,
        explicacion: "✗ Sin invertir, pierdes dinero por inflación (~3% anual).",
      },
    ],
  },
  {
    id: 4,
    contexto: "Empiezas a ahorrar $10/mes desde ahora",
    pregunta: "¿Cuánto tendrás en 10 años con 5% interés?",
    opciones: [
      {
        texto: "~$1,300",
        correcta: true,
        explicacion: "✓ Correcto! El interés compuesto trabaja magia. Ese es el poder de empezar temprano.",
      },
      {
        texto: "$1,200 (10 x 12 x 10)",
        correcta: false,
        explicacion: "✗ No contaste el interés compuesto que multiplica tu dinero.",
      },
      {
        texto: "Solo $1,000",
        correcta: false,
        explicacion: "✗ Subestimaste el poder del tiempo y los intereses.",
      },
    ],
  },
  {
    id: 5,
    contexto: "Tu mejor amigo te invita a gastar dinero que no habías presupuestado",
    pregunta: "¿Cuál es la respuesta inteligente?",
    opciones: [
      {
        texto: "Revisar tu presupuesto y si hay espacio, ir",
        correcta: true,
        explicacion: "✓ Perfecto! Los mejores financieramente son disciplinados pero no aburridos.",
      },
      {
        texto: "Ir siempre, la vida es para vivirla",
        correcta: false,
        explicacion: "✗ La vida es mejor cuando tienes control de tu dinero y libertad financiera.",
      },
      {
        texto: "Nunca gastar dinero en diversión",
        correcta: false,
        explicacion: "✗ Balance es clave. El 30% de diversión es OBLIGATORIO en el presupuesto.",
      },
    ],
  },
]

interface GameState {
  currentScenario: number
  score: number
  answered: boolean
  selectedOption: number | null
  gameOver: boolean
}

export default function MiniFinanceGame({ onStreakUpdate }: { onStreakUpdate?: (streak: number) => void }) {
  const [gameState, setGameState] = useState<GameState>({
    currentScenario: 0,
    score: 0,
    answered: false,
    selectedOption: null,
    gameOver: false,
  })

  const currentScenario = GAME_SCENARIOS[gameState.currentScenario]

  const handleSelectOption = (index: number) => {
    if (gameState.answered) return

    const option = currentScenario.opciones[index]
    const newScore = gameState.score + (option.correcta ? 1 : 0)

    setGameState((prev) => ({
      ...prev,
      selectedOption: index,
      answered: true,
      score: newScore,
    }))
  }

  const handleNextQuestion = () => {
    if (gameState.currentScenario < GAME_SCENARIOS.length - 1) {
      setGameState((prev) => ({
        ...prev,
        currentScenario: prev.currentScenario + 1,
        selectedOption: null,
        answered: false,
      }))
    } else {
      setGameState((prev) => ({
        ...prev,
        gameOver: true,
      }))
      if (onStreakUpdate) {
        onStreakUpdate(Math.floor(Math.random() * 20) + 10)
      }
    }
  }

  const handleRestart = () => {
    setGameState({
      currentScenario: 0,
      score: 0,
      answered: false,
      selectedOption: null,
      gameOver: false,
    })
  }

  if (gameState.gameOver) {
    const percentage = (gameState.score / GAME_SCENARIOS.length) * 100

    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-gradient-to-br from-purple-500/20 to-cyan-500/20 border border-purple-500/50 rounded-xl p-8 text-center space-y-6">
          <h2 className="text-3xl font-bold">{"¡Juego Terminado!"}</h2>
          <div className="space-y-2">
            <p className="text-5xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
              {gameState.score}/{GAME_SCENARIOS.length}
            </p>
            <p className="text-xl text-muted-foreground">
              {percentage >= 80
                ? "🎉 Eres un experto financiero!"
                : percentage >= 60
                  ? "👍 Buen trabajo!"
                  : "💪 Sigue aprendiendo!"}
            </p>
          </div>

          <div className="space-y-2 text-left bg-card/50 p-4 rounded-lg">
            <p className="text-sm font-medium">Tu puntuación refleja:</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              {percentage >= 80 && <li>{"✓ Entiendes presupuestos y crecimiento financiero"}</li>}
              {percentage >= 80 && <li>{"✓ Sabes tomar decisiones inteligentes con dinero"}</li>}
              {percentage < 80 && <li>{"→ Necesitas reforzar conceptos de inversión"}</li>}
              {percentage < 80 && <li>{"→ Vuelve al tab \"Conceptos\" para aprender más"}</li>}
            </ul>
          </div>

          <Button
            onClick={handleRestart}
            className="w-full bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 text-white py-6 font-bold text-lg"
          >
            Jugar de Nuevo
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium">
            Pregunta {gameState.currentScenario + 1} de {GAME_SCENARIOS.length}
          </span>
          <span className="text-sm font-medium">Puntuación: {gameState.score}</span>
        </div>
        <div className="w-full h-2 bg-border rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 transition-all duration-300"
            style={{ width: `${((gameState.currentScenario + 1) / GAME_SCENARIOS.length) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-gradient-to-br from-card to-card/50 border border-border/50 rounded-xl p-6 sm:p-8 space-y-6">
        <div className="space-y-2">
          <p className="text-sm font-medium text-cyan-400">Contexto: {currentScenario.contexto}</p>
          <h2 className="text-2xl font-bold">{currentScenario.pregunta}</h2>
        </div>

        <div className="space-y-3">
          {currentScenario.opciones.map((opcion, index) => {
            const selected = gameState.selectedOption === index
            const answered = gameState.answered
            let bgColor = "bg-card hover:bg-card/80 border-border/50 hover:border-border"

            if (answered && selected) {
              bgColor = opcion.correcta ? "bg-green-500/20 border-green-500" : "bg-red-500/20 border-red-500"
            } else if (answered && opcion.correcta) {
              bgColor = "bg-green-500/20 border-green-500"
            }

            return (
              <button
                key={index}
                onClick={() => handleSelectOption(index)}
                disabled={answered}
                className={`w-full text-left p-4 rounded-lg border transition-all ${bgColor} ${answered ? "cursor-default" : "cursor-pointer"}`}
              >
                <p className="font-medium">{opcion.texto}</p>
                {answered && selected && (
                  <p className={`text-sm mt-2 ${opcion.correcta ? "text-green-400" : "text-red-400"}`}>
                    {opcion.explicacion}
                  </p>
                )}
                {answered && !selected && opcion.correcta && (
                  <p className="text-sm mt-2 text-green-400">{opcion.explicacion}</p>
                )}
              </button>
            )
          })}
        </div>

        {gameState.answered && (
          <Button
            onClick={handleNextQuestion}
            className="w-full bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 text-white py-6 font-bold"
          >
            {gameState.currentScenario === GAME_SCENARIOS.length - 1 ? "Ver Resultado" : "Siguiente Pregunta"}
          </Button>
        )}
      </div>
    </div>
  )
}
