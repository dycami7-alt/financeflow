import os
import sqlite3

from app.config import DATABASE_URL


def _ensure_database_path():
    directory = os.path.dirname(DATABASE_URL)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    _ensure_database_path()
    connection = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def crear_tablas():
    """Create essential database tables for the application."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            profile_id INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"
    )

    # Tabla para perfiles financieros
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            profile_type TEXT NOT NULL,
            score INTEGER NOT NULL,
            strengths TEXT NOT NULL,  -- JSON string
            areas TEXT NOT NULL,      -- JSON string
            savings_plan TEXT NOT NULL,
            risk_tolerance TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Tabla para respuestas del perfilador
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profile_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            points INTEGER NOT NULL,
            answer_type TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        )
        """
    )

    # Tabla para metas financieras
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL DEFAULT 0,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Tabla para desafíos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_type TEXT NOT NULL,
            reward TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Tabla para mensajes de chat
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,  -- 'user' or 'assistant'
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Tabla para rachas de actividad
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            current_streak INTEGER NOT NULL DEFAULT 0,
            best_streak INTEGER NOT NULL DEFAULT 0,
            last_activity_date TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    # Tabla para sesiones de juego completadas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_type TEXT NOT NULL DEFAULT 'financial',
            score INTEGER NOT NULL,
            decisions TEXT NOT NULL,
            completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    connection.commit()
    connection.close()
