from typing import List
from app.database import get_connection
from app.models.chat import ChatMessage


def save_message(user_id: int, role: str, content: str) -> ChatMessage:
    """Guarda un mensaje en la base de datos"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages (user_id, role, content)
        VALUES (?, ?, ?)
        """,
        (user_id, role, content)
    )

    message_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return ChatMessage(
        id=message_id,
        user_id=user_id,
        role=role,
        content=content
    )


def get_chat_history(user_id: int, limit: int = 50) -> List[ChatMessage]:
    """Obtiene el historial de chat del usuario, limitado a los últimos mensajes"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM chat_messages
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cursor.fetchall()
    connection.close()

    # Revertir para tener orden cronológico
    messages = [ChatMessage(**dict(row)) for row in rows]
    messages.reverse()

    return messages


def clear_chat_history(user_id: int) -> bool:
    """Limpia el historial de chat del usuario"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM chat_messages WHERE user_id = ?",
        (user_id,)
    )

    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()

    return deleted