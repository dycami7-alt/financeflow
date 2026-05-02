import { useState } from "react"
import { Button } from "@/components/ui/button"
import PersonalityQuiz from "./profiler-quiz"
import UserProfile from "./user-profile"
import ChallengesDashboard from "./challenges-dashboard"

type ProfilerStep = "quiz" | "results" | "challenges"

interface UserFinancialProfile {
  name: string
  profileType: "Conservative" | "Moderate" | "Aggressive" | "undefined"
  score: number
  strengths: string[]
  areas: string[]
  savingsPlan: string
  riskTolerance: string
}

export default function FinancialProfiler() {
  const [step, setStep] = useState<ProfilerStep>("quiz")
  const [profile, setProfile] = useState<UserFinancialProfile | null>(null)

  const handleQuizComplete = (newProfile: UserFinancialProfile) => {
    setProfile(newProfile)
    setStep("results")
  }

  const handleStartChallenges = () => {
    setStep("challenges")
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      {step === "quiz" && <PersonalityQuiz onComplete={handleQuizComplete} />}

      {step === "results" && profile && (
        <div className="space-y-6">
          <UserProfile profile={profile} />
          <Button
            onClick={handleStartChallenges}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-6 text-lg font-bold shadow-lg shadow-purple-500/50"
          >
            Crear Mis Retos Personalizados
          </Button>
        </div>
      )}

      {step === "challenges" && profile && <ChallengesDashboard profile={profile} />}
    </div>
  )
}
