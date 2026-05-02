import { useState } from "react"
import { Button } from "@/components/ui/button"

interface QuizQuestion {
  id: number
  question: string
  answers: { text: string; points: number; type: string }[]
}

const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: 1,
    question: "¿Cuándo recibes dinero (mesada, regalo), qué haces?",
    answers: [
      { text: "Lo guardo inmediatamente en mi cuenta", points: 3, type: "conservative" },
      { text: "Divido entre ahorrar y gastar", points: 2, type: "moderate" },
      { text: "Lo gasto en lo que quiero, luego pienso en ahorrar", points: 1, type: "aggressive" },
    ],
  },
  {
    id: 2,
    question: "¿Cómo manejas tus gastos?",
    answers: [
      { text: "Tengo un presupuesto detallado y lo sigo al pie de la letra", points: 3, type: "conservative" },
      { text: "Intento controlarlos pero a veces me paso", points: 2, type: "moderate" },
      { text: "Gasto según lo que necesito en el momento", points: 1, type: "aggressive" },
    ],
  },
  {
    id: 3,
    question: "¿Qué harías si tuvieras $500 extra?",
    answers: [
      { text: "Ahorrar la mayoría, gastar poco", points: 3, type: "conservative" },
      { text: "Ahorrar $250 y gastar $250 en algo especial", points: 2, type: "moderate" },
      { text: "Gastar en algo que realmente quiero", points: 1, type: "aggressive" },
    ],
  },
  {
    id: 4,
    question: "¿Tienes una meta de ahorro?",
    answers: [
      { text: "Sí, muy específica y llevo un registro diario", points: 3, type: "conservative" },
      { text: "Más o menos, pero no es muy detallada", points: 2, type: "moderate" },
      { text: "No realmente, voy viendo según avance", points: 1, type: "aggressive" },
    ],
  },
  {
    id: 5,
    question: "¿Qué te motivaría a ahorrar?",
    answers: [
      { text: "La seguridad de tener dinero guardado", points: 3, type: "conservative" },
      { text: "Un balance entre seguridad y libertad", points: 2, type: "moderate" },
      { text: "La posibilidad de alcanzar mis sueños rápidamente", points: 1, type: "aggressive" },
    ],
  },
  {
    id: 6,
    question: "¿Cómo te sientes con invertir dinero?",
    answers: [
      { text: "Prefiero cosas seguras y sin riesgo", points: 3, type: "conservative" },
      { text: "Riesgo moderado con posible ganancia", points: 2, type: "moderate" },
      { text: "Me gustaría intentar inversiones arriesgadas", points: 1, type: "aggressive" },
    ],
  },
]

interface ProfilerQuizProps {
  onComplete: (profile: {
    name: string
    profileType: "Conservative" | "Moderate" | "Aggressive"
    score: number
    strengths: string[]
    areas: string[]
    savingsPlan: string
    riskTolerance: string
  }) => void
}

export default function PersonalityQuiz({ onComplete }: ProfilerQuizProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<number[]>([])
  const [scores, setScores] = useState({ conservative: 0, moderate: 0, aggressive: 0 })

  const handleAnswer = (points: number, type: string) => {
    const newAnswers = [...answers, points]
    setAnswers(newAnswers)

    const newScores = {
      ...scores,
      [type]: scores[type as keyof typeof scores] + 1,
    }
    setScores(newScores)

    if (currentQuestion < QUIZ_QUESTIONS.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      calculateProfile(newAnswers, newScores)
    }
  }

  const calculateProfile = (finalAnswers: number[], finalScores: typeof scores) => {
    const totalScore = finalAnswers.reduce((a, b) => a + b, 0)
    const maxScore = QUIZ_QUESTIONS.length * 3

    let profileType: "Conservative" | "Moderate" | "Aggressive" = "Moderate"
    if (finalScores.conservative >= 4) profileType = "Conservative"
    if (finalScores.aggressive >= 4) profileType = "Aggressive"

    const strengths = getStrengths(profileType)
    const areas = getAreasToImprove(profileType)
    const savingsPlan = getSavingsPlan(profileType)
    const riskTolerance = getRiskTolerance(profileType)

    onComplete({
      name: "Joven Financiero",
      profileType,
      score: Math.round((totalScore / maxScore) * 100),
      strengths,
      areas,
      savingsPlan,
      riskTolerance,
    })
  }

  const getStrengths = (type: string) => {
    const strengthMap: Record<string, string[]> = {
      Conservative: ["Disciplina", "Planificación", "Control de gastos"],
      Moderate: ["Balance", "Flexibilidad", "Mentalidad realista"],
      Aggressive: ["Ambición", "Visión de futuro", "Decisión rápida"],
    }
    return strengthMap[type] || []
  }

  const getAreasToImprove = (type: string) => {
    const areasMap: Record<string, string[]> = {
      Conservative: ["Mayor inversión", "Tomar riesgos calculados", "Disfrutar lo que ganas"],
      Moderate: ["Aumentar disciplina", "Definir metas claras", "Aprender inversiones"],
      Aggressive: ["Mejorar planificación", "Crear presupuesto", "Pensar a largo plazo"],
    }
    return areasMap[type] || []
  }

  const getSavingsPlan = (type: string) => {
    const planMap: Record<string, string> = {
      Conservative: "30% ingresos mensuales hacia ahorro",
      Moderate: "20% ingresos mensuales hacia ahorro",
      Aggressive: "10% ingresos mensuales hacia ahorro (luego aumenta)",
    }
    return planMap[type] || ""
  }

  const getRiskTolerance = (type: string) => {
    const toleranceMap: Record<string, string> = {
      Conservative: "Bajo - Prefiere seguridad garantizada",
      Moderate: "Medio - Dispuesto a riesgos moderados",
      Aggressive: "Alto - Busca máximas ganancias",
    }
    return toleranceMap[type] || ""
  }

  const progress = ((currentQuestion + 1) / QUIZ_QUESTIONS.length) * 100

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
          Descubre Tu Perfil Financiero
        </h2>
        <p className="text-muted-foreground">Responde 6 preguntas y conoce tu mentalidad financiera</p>
      </div>

      <div className="w-full h-1 bg-slate-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-purple-600 to-cyan-600 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-purple-500/30 rounded-xl p-8 space-y-6">
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-white">
            {currentQuestion + 1}. {QUIZ_QUESTIONS[currentQuestion].question}
          </h3>
          <div className="space-y-2">
            {QUIZ_QUESTIONS[currentQuestion].answers.map((answer, idx) => (
              <Button
                key={idx}
                onClick={() => handleAnswer(answer.points, answer.type)}
                className="w-full h-auto p-4 text-left justify-start bg-slate-700/50 hover:bg-purple-600/50 text-white border border-purple-500/30 hover:border-cyan-400/50 transition-all rounded-lg"
              >
                {answer.text}
              </Button>
            ))}
          </div>
        </div>
      </div>

      <p className="text-center text-sm text-muted-foreground">
        Pregunta {currentQuestion + 1} de {QUIZ_QUESTIONS.length}
      </p>
    </div>
  )
}
