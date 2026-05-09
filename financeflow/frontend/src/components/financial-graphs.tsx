import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

export default function FinancialGraphs() {
  const budgetData = [
    { categoria: "Necesidades", valor: 50, fill: "hsl(280, 100%, 50%)" },
    { categoria: "Diversión", valor: 30, fill: "hsl(200, 100%, 50%)" },
    { categoria: "Ahorro", valor: 20, fill: "hsl(150, 100%, 50%)" },
  ]

  const savingsGrowthData = [
    { mes: "Mes 1", ahorros: 100, conInteres: 100.42 },
    { mes: "Mes 3", ahorros: 300, conInteres: 301.26 },
    { mes: "Mes 6", ahorros: 600, conInteres: 603.01 },
    { mes: "Año 1", ahorros: 1200, conInteres: 1206.3 },
    { mes: "Año 2", ahorros: 2400, conInteres: 2425.37 },
    { mes: "Año 5", ahorros: 6000, conInteres: 6639.55 },
  ]

  const expenseCategories = [
    { nombre: "Comida", gasto: 150 },
    { nombre: "Transporte", gasto: 80 },
    { nombre: "Entretenimiento", gasto: 120 },
    { nombre: "Suscripciones", gasto: 45 },
    { nombre: "Otros", gasto: 55 },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-2">Conceptos Financieros Visuales</h2>
        <p className="text-muted-foreground">Entiende mejor cómo funciona el dinero con estas gráficas educativas</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-card border border-border/50 rounded-lg p-6">
          <h3 className="text-lg font-bold mb-4">Regla 50/30/20 del Presupuesto</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={budgetData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ categoria, valor }) => `${categoria}: ${valor}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="valor"
              >
                {budgetData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
            </PieChart>
          </ResponsiveContainer>
          <p className="text-xs text-muted-foreground mt-4 text-center">
            Divide tu dinero en estas 3 categorías para un presupuesto balanceado
          </p>
        </div>

        <div className="bg-card border border-border/50 rounded-lg p-6">
          <h3 className="text-lg font-bold mb-4">{"Interés Compuesto: Tu Dinero Trabaja"}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={savingsGrowthData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(0 0% 20%)" />
              <XAxis dataKey="mes" stroke="hsl(0 0% 50%)" />
              <YAxis stroke="hsl(0 0% 50%)" />
              <Tooltip
                contentStyle={{ backgroundColor: "hsl(0 0% 15%)", border: "1px solid hsl(200 100% 50%)" }}
                formatter={(value: number) => `$${value.toFixed(2)}`}
              />
              <Legend />
              <Line type="monotone" dataKey="ahorros" stroke="hsl(280 100% 50%)" strokeWidth={2} name="Ahorro Base" />
              <Line
                type="monotone"
                dataKey="conInteres"
                stroke="hsl(150 100% 50%)"
                strokeWidth={2}
                name="Con Interés 5% anual"
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-muted-foreground mt-4 text-center">
            Mira cómo tu dinero crece exponencialmente con el tiempo
          </p>
        </div>

        <div className="bg-card border border-border/50 rounded-lg p-6 lg:col-span-2">
          <h3 className="text-lg font-bold mb-4">Ejemplo: Gastos Mensuales Típicos</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={expenseCategories}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(0 0% 20%)" />
              <XAxis dataKey="nombre" stroke="hsl(0 0% 50%)" />
              <YAxis stroke="hsl(0 0% 50%)" />
              <Tooltip
                contentStyle={{ backgroundColor: "hsl(0 0% 15%)", border: "1px solid hsl(200 100% 50%)" }}
                formatter={(value) => `$${value}`}
              />
              <Bar dataKey="gasto" fill="hsl(200 100% 50%)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-xs text-muted-foreground mt-4 text-center">
            Identifica dónde va tu dinero y encuentra oportunidades para ahorrar
          </p>
        </div>
      </div>
    </div>
  )
}
