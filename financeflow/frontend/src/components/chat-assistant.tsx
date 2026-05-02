import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface Message {
  id: number
  text: string
  sender: "user" | "assistant"
}

interface ChatAssistantProps {
  onStreakUpdate?: (streak: number) => void
}

export default function ChatAssistant({ onStreakUpdate }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "🚀 ¡Bienvenido a FinanceFlow!\n\nSoy tu asistente financiero inteligente. Estoy aquí para:\n\n💡 Enseñarte finanzas desde cero\n📊 Ayudarte con presupuestos\n💰 Explicar inversiones\n🎯 Alcanzar tus metas\n⚡ Mantener tu racha\n\n¿Qué quieres aprender hoy?",
      sender: "assistant",
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: "user",
    }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    if (onStreakUpdate) {
      setTimeout(() => {
        onStreakUpdate(Math.floor(Math.random() * 30) + 5)
      }, 500)
    }

    setTimeout(() => {
      const assistantMessage: Message = {
        id: messages.length + 2,
        text: getDetailedResponse(input),
        sender: "assistant",
      }
      setMessages((prev) => [...prev, assistantMessage])
      setLoading(false)
    }, 800)
  }

  const getDetailedResponse = (userInput: string): string => {
    const lower = userInput.toLowerCase()

    const responses: Record<string, string> = {
      presupuesto: `📊 PRESUPUESTO PRO - La Guía Completa

Un presupuesto es tu MAPA del dinero. Sin él, navegas a ciegas.

🎯 PASO 1: CALCULA TUS INGRESOS
Suma TODO lo que entra en un mes:
- ¿Mesada? ¿Trabajos freelance? ¿Vendes cosas?
- Sé realista, no optimista

💸 PASO 2: LISTA TODOS TUS GASTOS
- Necesidades: Comida, transporte, útiles
- Diversión: Cine, juegos, salidas
- Suscripciones: Netflix, Spotify, etc.

📌 PASO 3: LA REGLA 50/30/20
✓ 50% = NECESIDADES (no puedes vivir sin)
✓ 30% = DIVERSIÓN (te hace feliz)
✓ 20% = AHORROS (tu futuro)

📈 EJEMPLO CON $200/mes
- Necesidades: $100
- Diversión: $60
- Ahorros: $40

⚡ TIPS AVANZADOS:
1. Usa Google Sheets o Notion (apps de verdad)
2. Revisa CADA MES y ajusta
3. No seas perfecto, nadie lo es
4. Pequeños cambios = resultados enormes

¿Necesitas ayuda con alguna categoría específica?`,

      ahorrar: `💰 CÓMO AHORRAR COMO UN PRO

Ahorrar no = sacrificarse. Es INVERTIR en tu libertad.

❓ ¿POR QUÉ AHORRAR?
- Emergencias (laptop rota, sorpresas)
- Tus sueños (viaje, consola, laptop gaming)
- Libertad (hacer lo que quieras sin depender)

🚀 EMPIEZA AQUÍ:

1️⃣ EMPIEZA EN PEQUEÑO
Even $1 cuenta. $10/mes > $0.
Crece gradualmente sin presión.

2️⃣ ABRE CUENTA SEPARADA
No mezcles con dinero de gastar.
"Dinero que no ves = dinero que no gastas"

3️⃣ AUTOMATIZA (MAGIA)
Transfiere el mismo día que recibes dinero.
Tu cerebro se adapta automáticamente.

4️⃣ VISUALIZA LA META
Foto en tu cuarto.
¿Cuánto falta? Actualiza cada semana.
¡Celebra cada milestone!

5️⃣ LA REGLA DE ORO
Ahorra PRIMERO, luego gasta lo que sobra.
(No al revés)

📊 LA MAGIA DEL TIEMPO:
Si ahorras $50/mes a 3% anual:
- Año 1: $618 (puro tuyo)
- Año 2: $1,259 (empezó a crecer)
- Año 5: $3,319 (dinero gratis!)
- Año 10: $6,958 (el tiempo trabaja por ti)

🎯 ¿Cuál es tu primera meta de ahorro?`,

      gastar: `🛍️ LOS 7 TRUCOS PARA GASTAR MENOS (Sin ser miserable)

Controlar gastos ≠ privarte de todo. Es ser CONSCIENTE.

🎯 TRUCO 1: REGLA DE 24H
Ves algo que quieres → Espera 24 horas
80% de las veces se te olvida 😂

💳 TRUCO 2: DINERO EN EFECTIVO
Psicológicamente duele más ver dinero real desaparecer.
Más consciencia = menos gastos impulsivos.

📋 TRUCO 3: LISTA ANTES DE SALIR
Escribe exactamente qué necesitas.
Evita los pasillos de "tentación".

🎬 TRUCO 4: ALTERNATIVAS BARATAS
- ¿Café con amigos? Hazlo en casa
- ¿Ropa? Busca ofertas online
- ¿Entretenimiento? YouTube, juegos gratis

❓ TRUCO 5: LA PREGUNTA MÁGICA
"¿LO NECESITO O LO QUIERO?"
- Necesidad = vivirías sin ello?
- Quiero = sería lindo pero no lo necesito
¡Sé honesto!

📱 TRUCO 6: TRACK TUS GASTOS
Apunta TODO por 1 mes.
Verás patrones que te sorprenden.

👑 TRUCO 7: ESTABLECE UN PRESUPUESTO DIVERTIDO
Asigna una cantidad fija para "gustos".
Cuando se acabe, ¡se acaba!

💡 LA VERDAD: No es negar todo. Es elegir CONSCIENTE.

¿En qué categoría gastas más de lo que debería?`,

      racha: `🔥 CÓMO MANTENER TU RACHA DE APRENDIZAJE FINANCIERO

Las rachas funcionan porque FUNCIONAN. Te lo garantizo.

✨ ¿QUÉ ES UNA RACHA?
Es la magia de hacer algo consistentemente.
Cada día que chequeas = +1 punto
Rompes la racha = vuelves a empezar

🎯 EL PODER PSICOLÓGICO:
- Día 1: "Empecé"
- Día 7: "Tengo una racha"
- Día 30: "No la voy a romper"
- Día 100: "¡Soy una persona diferente!"

🚀 CÓMO CONSTRUIR TU RACHA:
1. Cada día haz UNA pregunta financiera
2. Aprende un concepto nuevo (5 min)
3. Anota tus gastos (2 min)
4. Visualiza tu meta (1 min)

Total = 10 minutos. Super fácil.

📊 LAS RACHAS MÁS LARGAS GANAN:
- Día 7: Patrón emergente
- Día 30: Nuevo hábito formado
- Día 100: Trasformación real

🏆 TU MEJOR RACHA?
Cada día que llegues, ¡celebra!
Comparte con amigos, que vean que estás aprendiendo.

¡No rompas tu racha hoy! 🔥`,

      inversión: `📈 INVERSIONES PARA JÓVENES (Sí, a tu edad YA puedes)

Aquí está el secreto que los ricos conocen desde niños:

❓ ¿POR QUÉ INVERTIR?
- Tu dinero crece mientras duermes
- Aprendes desde joven
- A los 25 estarás AÑOS adelante

🎯 OPCIONES REALES:

1. FONDOS INDEXADOS (Lo más fácil)
   - Compras "paquetes" de acciones
   - El riesgo se divide
   - Retorno ~8% anual histórico
   - ✓ Perfecta para empezar

2. FONDOS MUTUALES
   - Profesionales invierten por ti
   - Comisiones bajas
   - Menos investigación requerida

3. CRIPTOMONEDAS (Alto riesgo, alta recompensa)
   - Bitcoin, Ethereum
   - Especulativo pero emocionante
   - Empieza con $10-20 max

4. ACCIONES INDIVIDUALES (Investigación seria)
   - Apple, Google, Microsoft
   - Requiere conocimiento real
   - Pero es ADICTIVO 😄

📌 REGLA DE ORO ABSOLUTA:
✓ Solo invierte dinero que NO necesites en 5 años
✓ Empieza pequeño ($10-20)
✓ Diversifica (NO todo en uno)
✓ Edúcate PRIMERO, invierte DESPUÉS

💡 LA VERDAD:
El mejor momento para empezar fue ayer.
El segundo mejor momento es HOY.

¿Qué tipo de inversión te atrae?`,

      interés: `🚀 INTERÉS COMPUESTO (La 8va Maravilla del Mundo)

Albert Einstein dijo que esto era lo más potente del universo.

❓ ¿QUÉ ES?
Es cuando tu dinero gana dinero,
y ese dinero nuevo TAMBIÉN gana dinero.
= CRECIMIENTO EXPONENCIAL

📊 EJEMPLO REAL (La diferencia es BRUTAL):

SI AHORRAS $100 UNA SOLA VEZ a 5% anual:
- Año 1: $105 (ganaste $5)
- Año 5: $128 (ganaste $28)
- Año 10: $163 (ganaste $63)
- Año 20: $265 (ganaste $165)
- Año 30: $432 (¡GANASTE $332!)

SIN HACER NADA. Solo esperar.

⚡ PERO SI AHORRAS $100/MES:
- Año 1: $1,236
- Año 5: $6,639
- Año 10: $14,566
- Año 20: $37,779
- Año 30: $82,571

¿VES LA DIFERENCIA?

🎯 ¿POR QUÉ TE IMPORTA?
- Empezar a los 15 vs 25 = $100,000+ de diferencia
- Es MAGIA del tiempo, no de la cantidad
- A los 50 años estarás RICO sin hacer mucho

💡 LA LECCIÓN: El mejor momento es HOY.
Incluso $5/mes en 30 años = riqueza real.

¿Quieres calcular tu futuro financiero?`,
    }

    for (const [key, response] of Object.entries(responses)) {
      if (lower.includes(key)) {
        return response
      }
    }

    return `⚡ Excelente pregunta. Aquí están los temas principales:

📚 **Conceptos Básicos:**
- Presupuesto
- Ahorrar
- Gastar

🎯 **Mentalidad:**
- Racha (mantén el fuego!)
- Metas

📈 **Avanzado:**
- Interés (compuesto)
- Inversión

Escribe cualquier tema y te doy la guía completa. 🚀`
  }

  const handleQuickQuestion = (question: string) => {
    setInput(question)
  }

  return (
    <div className="w-full max-w-3xl flex flex-col">
      <div
        ref={scrollRef}
        className="h-96 sm:h-[500px] overflow-y-auto mb-4 space-y-3 p-4 rounded-xl border border-purple-500/30 bg-black/40 backdrop-blur-sm"
      >
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-xs sm:max-w-sm px-4 py-3 rounded-lg text-sm leading-relaxed ${
                message.sender === "user"
                  ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-br-none shadow-lg shadow-purple-500/50"
                  : "bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-bl-none border border-cyan-500/30"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gradient-to-r from-slate-700 to-slate-800 px-4 py-3 rounded-lg rounded-bl-none border border-cyan-500/30">
              <div className="flex gap-1.5">
                <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></div>
                <div
                  className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.4s" }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {["💰 ¿Cómo hago un presupuesto?", "📊 ¿Cómo ahorrar?", "🔥 Mantener mi racha", "📈 Invertir dinero"].map(
            (question, idx) => (
              <button
                key={idx}
                onClick={() => handleQuickQuestion(question)}
                className="text-xs sm:text-sm p-3 rounded-lg bg-gradient-to-r from-purple-500/20 to-blue-500/20 hover:from-purple-500/40 hover:to-blue-500/40 text-cyan-300 transition-all border border-purple-500/50 font-medium hover:border-cyan-400/50 hover:shadow-lg hover:shadow-purple-500/20"
              >
                {question}
              </button>
            ),
          )}
        </div>

        <div className="flex gap-2">
          <Input
            type="text"
            placeholder="Pregunta algo sobre dinero..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            className="text-sm bg-slate-900 border-purple-500/30 text-white placeholder:text-muted-foreground focus:border-cyan-400/50"
          />
          <Button
            onClick={handleSendMessage}
            disabled={loading}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-6 font-medium shadow-lg shadow-purple-500/50"
          >
            →
          </Button>
        </div>
      </div>
    </div>
  )
}
