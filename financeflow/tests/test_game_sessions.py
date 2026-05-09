import os
import sys
import tempfile
import unittest
import importlib
from datetime import datetime, timedelta

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

import app.config as config
import app.database as database
import app.services.game_service as game_service
import app.main as app_main
from fastapi.testclient import TestClient

importlib.reload(config)
importlib.reload(database)
importlib.reload(game_service)
importlib.reload(app_main)

database.crear_tablas()
client = TestClient(app_main.app)


class GameSessionTests(unittest.TestCase):
    def test_create_and_retrieve_game_session(self):
        session_id = game_service.create_game_session(
            user_id=1,
            score=85,
            decisions=[{"scenario_id": 1, "selected_option": "A", "quality": "buena"}],
            game_type="financial",
        )
        self.assertGreater(session_id, 0)

        sessions = game_service.get_game_sessions_by_user(1)
        self.assertTrue(any(s["id"] == session_id for s in sessions))
        session = next(s for s in sessions if s["id"] == session_id)
        self.assertEqual(session["score"], 85)
        self.assertEqual(session["game_type"], "financial")
        self.assertIsInstance(session["decisions"], list)

    def test_register_game_session_route(self):
        response = client.post(
            "/api/juego/session",
            json={
                "user_id": 2,
                "score": 70,
                "game_type": "financial",
                "decisions": [{"scenario_id": 2, "selected_option": "B", "quality": "mala"}],
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["user_id"], 2)
        self.assertEqual(data["score"], 70)
        self.assertEqual(data["game_type"], "financial")
        self.assertIsInstance(data["decisions"], list)

    def test_list_sessions_with_filters(self):
        now = datetime.utcnow()
        older = now - timedelta(days=7)
        newer = now - timedelta(days=1)

        game_service.create_game_session(
            user_id=3,
            score=40,
            decisions=[{"scenario_id": 3, "selected_option": "A", "quality": "mala"}],
            game_type="financial",
            completed_at=older.isoformat(),
        )
        game_service.create_game_session(
            user_id=3,
            score=90,
            decisions=[{"scenario_id": 4, "selected_option": "C", "quality": "buena"}],
            game_type="financial",
            completed_at=newer.isoformat(),
        )

        response = client.get(f"/api/juego/sessions/3?min_score=50")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["score"], 90)

        start_date = (now - timedelta(days=2)).isoformat()
        response = client.get(f"/api/juego/sessions/3?start_date={start_date}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["score"], 90)

        end_date = (now - timedelta(days=2)).isoformat()
        response = client.get(f"/api/juego/sessions/3?end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["score"], 40)


if __name__ == "__main__":
    unittest.main()
