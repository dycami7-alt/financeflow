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


def get_financial_scenarios() -> List[Dict[str, Any]]:
    return [
        {
            "scenario_id": 1,
            "title": "Fondo de emergencia",
            "description": "Te enfrentas a un gasto inesperado de 1.200 USD.",
            "options": [
                {
                    "option_id": "A",
                    "text": "Reservar inmediatamente 3-6 meses de gastos en un fondo de emergencia.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Un fondo de emergencia protege tu estabilidad cuando ocurren imprevistos sin endeudarte."
                },
                {
                    "option_id": "B",
                    "text": "Cubrirlo con tarjeta de crédito y pagarlo después.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Depender de deuda costosa aumenta riesgos y puede generar pagos prolongados."
                },
                {
                    "option_id": "C",
                    "text": "Usar inversiones de alto riesgo para obtener el dinero rápido.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Vender inversiones en un mal momento o tomar riesgos innecesarios puede disminuir tu patrimonio."
                }
            ]
        },
        {
            "scenario_id": 2,
            "title": "Deuda de alto interés",
            "description": "Tienes una tarjeta con 25% de interés y te ofrecen una compra impulsiva.",
            "options": [
                {
                    "option_id": "A",
                    "text": "Pagar primero el saldo de la tarjeta antes de hacer compras extras.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Reducir deuda de alto interés es una decisión inteligente que libera flujo de efectivo y evita cargos futuros."
                },
                {
                    "option_id": "B",
                    "text": "Comprar ahora y lidiar con el pago después.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Agregar más deuda con alto interés puede empeorar tu situación financiera rápidamente."
                },
                {
                    "option_id": "C",
                    "text": "Ahorrar algo primero y luego decidir si compras.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Planificar la compra te ayuda a evitar decisiones impulsivas y protege tus finanzas."
                }
            ]
        },
        {
            "scenario_id": 3,
            "title": "Inversión a largo plazo",
            "description": "Tienes ahorros para invertir y eliges entre diversas estrategias.",
            "options": [
                {
                    "option_id": "A",
                    "text": "Diversificar en una mezcla moderada de inversiones a largo plazo.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Diversificar reduce riesgo y permite construir patrimonio con menor volatilidad."
                },
                {
                    "option_id": "B",
                    "text": "Poner todo en una sola acción volátil.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Concentrar tus fondos en un solo activo puede llevar a pérdidas significativas."
                },
                {
                    "option_id": "C",
                    "text": "Dejar todo en efectivo sin invertir.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "El efectivo pierde valor con la inflación, por lo que ahorrar sin invertir no maximiza tu crecimiento."
                }
            ]
        },
        {
            "scenario_id": 4,
            "title": "Ahorro para la jubilación",
            "description": "Decides cómo destinar parte de tu salario al retiro.",
            "options": [
                {
                    "option_id": "A",
                    "text": "Ahorrar consistentemente y aumentar el monto cada año.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Aumentar el ahorro gradualmente es la mejor forma de construir un retiro seguro sin perjudicar tu flujo de caja."
                },
                {
                    "option_id": "B",
                    "text": "No ahorrar para el retiro y gastar todo el salario.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Postergar el ahorro para el retiro puede dejarte sin recursos suficientes en el futuro."
                },
                {
                    "option_id": "C",
                    "text": "Ahorrar lo mínimo permitido por ley y nada más.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Ahorrar solo lo mínimo puede ser insuficiente para mantener tu estilo de vida en el futuro."
                }
            ]
        },
        {
            "scenario_id": 5,
            "title": "Protección financiera",
            "description": "Evalúas si debes contratar seguro y mantener tus finanzas organizadas.",
            "options": [
                {
                    "option_id": "A",
                    "text": "Contratar seguro adecuado y mantener un presupuesto mensual.",
                    "quality": "buena",
                    "score": 20,
                    "explanation": "Prevenir riesgos y controlar gastos te da estabilidad y protege tu patrimonio."
                },
                {
                    "option_id": "B",
                    "text": "Evitar seguros porque son costosos.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "No asegurar activos importantes puede exponerte a pérdidas que podrían ser difíciles de superar."
                },
                {
                    "option_id": "C",
                    "text": "Confiar en que la familia cubrirá cualquier problema.",
                    "quality": "mala",
                    "score": 0,
                    "explanation": "Depender de otros para emergencias financieras no es una estrategia confiable."
                }
            ]
        }
    ]


def evaluate_financial_decisions(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    scenarios = get_financial_scenarios()
    scenario_map = {s["scenario_id"]: s for s in scenarios}
    results = []
    total_score = 0
    max_score = len(scenarios) * 20

    for decision in decisions:
        scenario_id = decision.get("scenario_id")
        selected_option = decision.get("selected_option")
        scenario = scenario_map.get(scenario_id)

        if scenario is None:
            results.append({
                "scenario_id": scenario_id,
                "quality": "mala",
                "score": 0,
                "explanation": "Escenario inválido.",
                "selected_option": selected_option
            })
            continue

        option = next((opt for opt in scenario["options"] if opt["option_id"] == selected_option), None)

        if option is None:
            results.append({
                "scenario_id": scenario_id,
                "title": scenario["title"],
                "quality": "mala",
                "score": 0,
                "explanation": "Opción no válida para este escenario.",
                "selected_option": selected_option
            })
            continue

        results.append({
            "scenario_id": scenario_id,
            "title": scenario["title"],
            "selected_option": selected_option,
            "quality": option["quality"],
            "score": option["score"],
            "explanation": option["explanation"],
            "option_text": option["text"]
        })
        total_score += option["score"]

    percentage = round((total_score / max_score) * 100) if max_score else 0
    if percentage >= 80:
        message = "Excelente: tus decisiones son sólidas y están bien orientadas financieramente."
    elif percentage >= 60:
        message = "Buen trabajo: tienes buenas bases, pero hay áreas donde puedes mejorar."
    else:
        message = "Necesitas reforzar tus decisiones financieras con mayor disciplina y planificación."

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "evaluation_message": message,
        "results": results
    }


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