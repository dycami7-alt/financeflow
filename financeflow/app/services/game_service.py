import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.database import get_connection


def create_game_session(
    user_id: int,
    score: int,
    decisions: List[Dict[str, Any]],
    game_type: str = "financial",
    completed_at: Optional[str] = None,
) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    if completed_at:
        cursor.execute(
            """
            INSERT INTO game_sessions (user_id, game_type, score, decisions, completed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                game_type,
                score,
                json.dumps(decisions, ensure_ascii=False),
                completed_at,
            ),
        )
    else:
        cursor.execute(
            """
            INSERT INTO game_sessions (user_id, game_type, score, decisions)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                game_type,
                score,
                json.dumps(decisions, ensure_ascii=False),
            ),
        )
    connection.commit()
    session_id = cursor.lastrowid
    connection.close()
    return session_id


def parse_iso_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def get_game_sessions_by_user(
    user_id: int,
    min_score: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM game_sessions WHERE user_id = ?"
    params: List[Any] = [user_id]

    if min_score is not None:
        query += " AND score >= ?"
        params.append(min_score)

    parsed_start = parse_iso_date(start_date)
    if parsed_start:
        query += " AND completed_at >= ?"
        params.append(parsed_start)

    parsed_end = parse_iso_date(end_date)
    if parsed_end:
        query += " AND completed_at <= ?"
        params.append(parsed_end)

    query += " ORDER BY completed_at DESC"
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    connection.close()
    sessions = []
    for row in rows:
        data = dict(row)
        try:
            data["decisions"] = json.loads(data["decisions"])
        except Exception:
            data["decisions"] = []
        sessions.append(data)
    return sessions
