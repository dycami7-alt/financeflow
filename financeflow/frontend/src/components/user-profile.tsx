interface Profile {
  name: string
  profileType: string
  score: number
  strengths: string[]
  areas: string[]
  savingsPlan: string
  riskTolerance: string
}

interface UserProfileProps {
  profile: Profile
}

const PROFILE_DESCRIPTIONS: Record<string, string> = {
  Conservative:
    "Eres disciplinado y responsable con tu dinero. Te encanta planificar y tienes control total de tus gastos. Tu desafío es aprender a disfrutar lo que ganas y tomar riesgos calculados.",
  Moderate:
    "Tienes un balance perfecto. Ahorras pero también disfrutas de la vida. Tu mentalidad es realista y adaptable a diferentes situaciones financieras.",
  Aggressive:
    "Tienes visión y ambición. Te mueves rápido y buscas oportunidades. Tu desafío es desarrollar disciplina y crear un plan financiero sólido a largo plazo.",
}

export default function UserProfile({ profile }: UserProfileProps) {
  const getProfileEmoji = (type: string) => {
    const emojiMap: Record<string, string> = {
      Conservative: "🛡️",
      Moderate: "⚖️",
      Aggressive: "🚀",
    }
    return emojiMap[type] || "💰"
  }

  const getProfileColor = (type: string) => {
    const colorMap: Record<string, string> = {
      Conservative: "from-blue-600 to-blue-400",
      Moderate: "from-purple-600 to-pink-400",
      Aggressive: "from-orange-600 to-red-400",
    }
    return colorMap[type] || "from-purple-600 to-blue-600"
  }

  return (
    <div className="space-y-6">
      <div className={`bg-gradient-to-br ${getProfileColor(profile.profileType)} rounded-2xl p-8 text-white space-y-4`}>
        <div className="flex items-center gap-4">
          <span className="text-5xl">{getProfileEmoji(profile.profileType)}</span>
          <div>
            <h2 className="text-3xl font-bold">Tu Perfil: {profile.profileType}</h2>
            <p className="text-white/80">Puntuación: {profile.score}%</p>
          </div>
        </div>

        <p className="text-lg leading-relaxed">{PROFILE_DESCRIPTIONS[profile.profileType]}</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-800/50 border border-green-500/30 rounded-xl p-4 space-y-3">
          <h3 className="font-bold text-green-400">Fortalezas</h3>
          <ul className="space-y-2">
            {profile.strengths.map((strength, idx) => (
              <li key={idx} className="text-sm text-white flex items-start gap-2">
                <span className="text-green-400">{"✓"}</span>
                {strength}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-800/50 border border-yellow-500/30 rounded-xl p-4 space-y-3">
          <h3 className="font-bold text-yellow-400">{"Áreas a Mejorar"}</h3>
          <ul className="space-y-2">
            {profile.areas.map((area, idx) => (
              <li key={idx} className="text-sm text-white flex items-start gap-2">
                <span className="text-yellow-400">{"→"}</span>
                {area}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-purple-900/50 to-purple-800/30 border border-purple-500/30 rounded-xl p-4">
          <p className="text-sm text-muted-foreground mb-2">Tolerancia al Riesgo</p>
          <p className="font-bold text-white">{profile.riskTolerance}</p>
        </div>

        <div className="bg-gradient-to-br from-cyan-900/50 to-cyan-800/30 border border-cyan-500/30 rounded-xl p-4">
          <p className="text-sm text-muted-foreground mb-2">Plan de Ahorro</p>
          <p className="font-bold text-white">{profile.savingsPlan}</p>
        </div>
      </div>
    </div>
  )
}
