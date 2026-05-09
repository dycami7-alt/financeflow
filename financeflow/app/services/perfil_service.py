import json
from typing import List, Dict, Any, Optional
from app.database import get_connection
from app.models.perfil import Profile, ProfileAnswer


def calculate_profile(answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula el perfil financiero basado en las respuestas"""
    total_score = sum(answer["points"] for answer in answers)
    max_score = len(answers) * 3  # Asumiendo max 3 puntos por pregunta
    percentage = round((total_score / max_score) * 100)

    # Contar tipos
    type_counts = {"conservative": 0, "moderate": 0, "aggressive": 0}
    for answer in answers:
        answer_type = answer["type"]
        if answer_type in type_counts:
            type_counts[answer_type] += 1

    # Determinar tipo de perfil
    profile_type = "Moderate"
    if type_counts["conservative"] >= 4:
        profile_type = "Conservative"
    elif type_counts["aggressive"] >= 4:
        profile_type = "Aggressive"

    # Obtener fortalezas, áreas, etc. basado en tipo
    strengths = get_strengths(profile_type)
    areas = get_areas_to_improve(profile_type)
    savings_plan = get_savings_plan(profile_type)
    risk_tolerance = get_risk_tolerance(profile_type)

    return {
        "profile_type": profile_type,
        "score": percentage,
        "strengths": strengths,
        "areas": areas,
        "savings_plan": savings_plan,
        "risk_tolerance": risk_tolerance,
        "total_score": total_score,
        "type_counts": type_counts
    }


def get_strengths(profile_type: str) -> List[str]:
    strength_map = {
        "Conservative": ["Disciplina", "Planificación", "Control de gastos"],
        "Moderate": ["Balance", "Flexibilidad", "Mentalidad realista"],
        "Aggressive": ["Ambición", "Visión de futuro", "Decisión rápida"],
    }
    return strength_map.get(profile_type, [])


def get_areas_to_improve(profile_type: str) -> List[str]:
    areas_map = {
        "Conservative": ["Mayor inversión", "Tomar riesgos calculados", "Disfrutar lo que ganas"],
        "Moderate": ["Aumentar disciplina", "Definir metas claras", "Aprender inversiones"],
        "Aggressive": ["Mejorar planificación", "Crear presupuesto", "Pensar a largo plazo"],
    }
    return areas_map.get(profile_type, [])


def get_savings_plan(profile_type: str) -> str:
    plan_map = {
        "Conservative": "30% ingresos mensuales hacia ahorro",
        "Moderate": "20% ingresos mensuales hacia ahorro",
        "Aggressive": "10% ingresos mensuales hacia ahorro (luego aumenta)",
    }
    return plan_map.get(profile_type, "")


def get_risk_tolerance(profile_type: str) -> str:
    tolerance_map = {
        "Conservative": "Bajo - Prefiere seguridad garantizada",
        "Moderate": "Medio - Dispuesto a riesgos moderados",
        "Aggressive": "Alto - Busca máximas ganancias",
    }
    return tolerance_map.get(profile_type, "")


def save_profile(user_id: int, profile_data: Dict[str, Any], answers: List[Dict[str, Any]]) -> int:
    """Guarda el perfil y las respuestas en la base de datos. Retorna el profile_id"""
    connection = get_connection()
    cursor = connection.cursor()

    # Insertar perfil
    cursor.execute(
        """
        INSERT INTO profiles (user_id, profile_type, score, strengths, areas, savings_plan, risk_tolerance)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            profile_data["profile_type"],
            profile_data["score"],
            json.dumps(profile_data["strengths"]),
            json.dumps(profile_data["areas"]),
            profile_data["savings_plan"],
            profile_data["risk_tolerance"]
        )
    )
    profile_id = cursor.lastrowid

    # Insertar respuestas
    for answer in answers:
        cursor.execute(
            """
            INSERT INTO profile_answers (profile_id, question_id, answer_id, points, answer_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                profile_id,
                answer["question_id"],
                answer["answer_id"],
                answer["points"],
                answer["type"]
            )
        )

    connection.commit()
    connection.close()
    return profile_id


def get_user_profile(user_id: int) -> Optional[Profile]:
    """Obtiene el perfil más reciente del usuario"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM profiles WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        data = dict(row)
        data["strengths"] = json.loads(data["strengths"])
        data["areas"] = json.loads(data["areas"])
        return Profile.from_dict(data)
    return None


def get_profile_answers(profile_id: int) -> List[ProfileAnswer]:
    """Obtiene las respuestas de un perfil"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM profile_answers WHERE profile_id = ?
        """,
        (profile_id,)
    )
    rows = cursor.fetchall()
    connection.close()

    answers = []
    for row in rows:
        data = dict(row)
        answers.append(ProfileAnswer.from_dict(data))
    return answers