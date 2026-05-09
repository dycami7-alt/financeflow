from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.database import get_connection
from app.models.streak import Streak, StreakUpdate


def get_streak(user_id: int) -> Optional[Streak]:
    """Obtiene la racha de un usuario"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM streaks WHERE user_id = ?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return Streak(
            id=row['id'],
            user_id=row['user_id'],
            current_streak=row['current_streak'],
            best_streak=row['best_streak'],
            last_activity_date=row['last_activity_date'],
            created_at=row['created_at']
        )
    return None


def create_streak(user_id: int) -> Streak:
    """Crea una nueva racha para un usuario"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO streaks (user_id, current_streak, best_streak, last_activity_date)
        VALUES (?, 0, 0, NULL)
        """,
        (user_id,)
    )

    streak_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return Streak(
        id=streak_id,
        user_id=user_id,
        current_streak=0,
        best_streak=0,
        last_activity_date=None,
        created_at=datetime.now().isoformat()
    )


def get_or_create_streak(user_id: int) -> Streak:
    """Obtiene o crea la racha de un usuario"""
    streak = get_streak(user_id)
    if streak is None:
        streak = create_streak(user_id)
    return streak


def _parse_timestamp(timestamp: str) -> datetime:
    """Convierte un timestamp ISO a datetime."""
    return datetime.fromisoformat(timestamp)


def _days_since_last_activity(last_activity: str, current_time: datetime) -> int:
    """Calcula cuántos días han pasado desde la última actividad."""
    last_date = _parse_timestamp(last_activity).date()
    return (current_time.date() - last_date).days


def update_streak(user_id: int) -> Streak:
    """
    Actualiza la racha del usuario cuando completa una acción.
    Lógica:
    - Si la última actividad fue el mismo día: mantiene la racha
    - Si la última actividad fue ayer: incrementa la racha
    - Si la última actividad fue antes de ayer: reinicia la racha
    """
    result = track_daily_activity(user_id)
    return result["streak"]


def track_daily_activity(user_id: int) -> dict:
    """Registra una interacción diaria y retorna el estado de la racha."""
    streak = get_or_create_streak(user_id)
    now = datetime.utcnow()
    last_activity = streak.last_activity_date

    if last_activity is None:
        status = "started"
        new_current_streak = 1
        new_best_streak = max(streak.best_streak, 1)
        new_last_activity = now.isoformat()
        days_diff = None
    else:
        days_diff = _days_since_last_activity(last_activity, now)

        if days_diff <= 0:
            status = "same_day"
            new_current_streak = streak.current_streak
            new_best_streak = streak.best_streak
            new_last_activity = streak.last_activity_date
        elif days_diff == 1:
            status = "incremented"
            new_current_streak = streak.current_streak + 1
            new_best_streak = max(streak.best_streak, new_current_streak)
            new_last_activity = now.isoformat()
        else:
            status = "reset"
            new_current_streak = 1
            new_best_streak = max(streak.best_streak, 1)
            new_last_activity = now.isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE streaks
        SET current_streak = ?, best_streak = ?, last_activity_date = ?
        WHERE user_id = ?
        """,
        (new_current_streak, new_best_streak, new_last_activity, user_id)
    )
    conn.commit()
    conn.close()

    return {
        "status": status,
        "days_since_last_activity": days_diff,
        "streak": get_streak(user_id)
    }


def reset_streak(user_id: int) -> Optional[Streak]:
    """Reinicia la racha de un usuario"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE streaks
        SET current_streak = 0, last_activity_date = NULL
        WHERE user_id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return get_streak(user_id)


def update_streak_manual(user_id: int, update_data: StreakUpdate) -> Optional[Streak]:
    """Actualiza manualmente la racha de un usuario"""
    streak = get_streak(user_id)
    if not streak:
        return None

    # Preparar los valores a actualizar
    updates = {}
    if update_data.current_streak is not None:
        updates['current_streak'] = update_data.current_streak
    if update_data.best_streak is not None:
        updates['best_streak'] = update_data.best_streak
    if update_data.last_activity_date is not None:
        updates['last_activity_date'] = update_data.last_activity_date

    if not updates:
        return streak

    # Construir la consulta SQL
    set_clause = ', '.join(f"{key} = ?" for key in updates.keys())
    values = list(updates.values()) + [user_id]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE streaks SET {set_clause} WHERE user_id = ?",
        values
    )

    conn.commit()
    conn.close()

    return get_streak(user_id)