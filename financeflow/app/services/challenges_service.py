from typing import List, Optional
from app.database import get_connection
from app.models.challenges import Challenge, ChallengeCreate, ChallengeUpdate
from app.services.perfil_service import get_user_profile


def create_challenge(user_id: int, challenge_data: ChallengeCreate) -> Challenge:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO challenges (user_id, challenge_type, reward)
        VALUES (?, ?, ?)
        """,
        (user_id, challenge_data.challenge_type, challenge_data.reward)
    )

    challenge_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return Challenge(
        id=challenge_id,
        user_id=user_id,
        challenge_type=challenge_data.challenge_type,
        reward=challenge_data.reward
    )


def get_challenges_by_user(user_id: int) -> List[Challenge]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM challenges WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()

    return [Challenge(**dict(row)) for row in rows]


def get_challenge_by_id(challenge_id: int, user_id: int) -> Optional[Challenge]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM challenges WHERE id = ? AND user_id = ?",
        (challenge_id, user_id)
    )

    row = cursor.fetchone()
    connection.close()

    if row:
        return Challenge(**dict(row))
    return None


def update_challenge(challenge_id: int, user_id: int, challenge_data: ChallengeUpdate) -> Optional[Challenge]:
    connection = get_connection()
    cursor = connection.cursor()

    # Build update query dynamically
    update_fields = []
    values = []

    if challenge_data.challenge_type is not None:
        update_fields.append("challenge_type = ?")
        values.append(challenge_data.challenge_type)

    if challenge_data.reward is not None:
        update_fields.append("reward = ?")
        values.append(challenge_data.reward)

    if not update_fields:
        return get_challenge_by_id(challenge_id, user_id)

    query = f"UPDATE challenges SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
    values.extend([challenge_id, user_id])

    cursor.execute(query, values)
    connection.commit()
    connection.close()

    return get_challenge_by_id(challenge_id, user_id)


def delete_challenge(challenge_id: int, user_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM challenges WHERE id = ? AND user_id = ?",
        (challenge_id, user_id)
    )

    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()

    return deleted


def generate_personalized_challenges(user_id: int) -> List[Challenge]:
    """Genera retos personalizados basados en el perfil del usuario"""
    profile = get_user_profile(user_id)
    if not profile:
        # Retos por defecto si no hay perfil
        return _get_default_challenges(user_id)

    profile_type = profile.profile_type

    challenges_data = []

    if profile_type == "Conservative":
        challenges_data = [
            {"type": "saving", "reward": "Medalla de Disciplina Financiera"},
            {"type": "budget", "reward": "Insignia de Control de Gastos"},
            {"type": "emergency_fund", "reward": "Escudo de Seguridad"},
        ]
    elif profile_type == "Moderate":
        challenges_data = [
            {"type": "investment", "reward": "Certificado de Inversión Inteligente"},
            {"type": "debt_reduction", "reward": "Trofeo de Libertad Financiera"},
            {"type": "goal_setting", "reward": "Corona de Planificación"},
        ]
    elif profile_type == "Aggressive":
        challenges_data = [
            {"type": "high_risk_investment", "reward": "Medalla de Alto Riesgo"},
            {"type": "entrepreneurship", "reward": "Llave del Éxito Empresarial"},
            {"type": "wealth_building", "reward": "Corona de Riqueza"},
        ]

    # Crear los retos en la BD
    created_challenges = []
    for data in challenges_data:
        challenge = create_challenge(user_id, ChallengeCreate(
            challenge_type=data["type"],
            reward=data["reward"]
        ))
        created_challenges.append(challenge)

    return created_challenges


def _get_default_challenges(user_id: int) -> List[Challenge]:
    """Retos por defecto para usuarios sin perfil"""
    default_data = [
        {"type": "saving", "reward": "Medalla de Ahorro"},
        {"type": "budget", "reward": "Insignia de Presupuesto"},
        {"type": "learning", "reward": "Certificado de Educación Financiera"},
    ]

    created_challenges = []
    for data in default_data:
        challenge = create_challenge(user_id, ChallengeCreate(
            challenge_type=data["type"],
            reward=data["reward"]
        ))
        created_challenges.append(challenge)

    return created_challenges