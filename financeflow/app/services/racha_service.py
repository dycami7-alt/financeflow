from datetime import datetime, timedelta
from typing import Dict, Optional
from app.models.racha import RachaData

# Simulamos una "base de datos" en memoria (puedes expandir esto con una BD real)
rachas_db: Dict[str, RachaData] = {}

def get_or_create_racha(user_id: str) -> RachaData:
    """Obtiene o crea una racha para un usuario"""
    if user_id not in rachas_db:
        rachas_db[user_id] = RachaData(user_id)
    return rachas_db[user_id]

def update_racha(user_id: str) -> RachaData:
    """
    Actualiza la racha del usuario cuando completa una acción.
    Lógica:
    - Si es el mismo día: no cambia la racha actual
    - Si es el día siguiente: incrementa la racha actual
    - Si pasaron más de 2 días: reinicia la racha actual
    """
    racha = get_or_create_racha(user_id)
    
    now = datetime.now().date()
    last_action = racha.last_action_date
    
    if last_action is None:
        # Primera vez que realiza una acción
        racha.current_streak = 1
        racha.best_streak = 1
        racha.last_action_date = now
    else:
        # Convertir a fecha si es datetime
        if isinstance(last_action, datetime):
            last_action = last_action.date()
        
        days_diff = (now - last_action).days
        
        if days_diff == 0:
            # Misma día, no cambia la racha
            pass
        elif days_diff == 1:
            # Día siguiente, incrementa la racha
            racha.current_streak += 1
            if racha.current_streak > racha.best_streak:
                racha.best_streak = racha.current_streak
            racha.last_action_date = now
        else:
            # Más de 1 día sin actividad, reinicia la racha
            racha.current_streak = 1
            racha.last_action_date = now
    
    racha.total_actions += 1
    racha.updated_at = datetime.now()
    
    return racha

def get_racha(user_id: str) -> Dict:
    """Obtiene la información de la racha del usuario"""
    racha = get_or_create_racha(user_id)
    return racha.to_dict()

def reset_racha(user_id: str) -> Dict:
    """Reinicia la racha del usuario"""
    racha = get_or_create_racha(user_id)
    racha.current_streak = 0
    racha.best_streak = max(racha.best_streak, 0)  # Mantiene el mejor record
    racha.last_action_date = None
    racha.updated_at = datetime.now()
    return racha.to_dict()

def get_racha_stats(user_id: str) -> Dict:
    """Obtiene estadísticas completas de rachas"""
    racha = get_or_create_racha(user_id)
    return {
        "current_streak": racha.current_streak,
        "best_streak": racha.best_streak,
        "total_actions": racha.total_actions,
        "last_action": racha.last_action_date.isoformat() if racha.last_action_date else None,
        "streak_percentage": (racha.total_actions / max(racha.current_streak + racha.best_streak, 1)) * 100 if racha.current_streak > 0 else 0
    }
