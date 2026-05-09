import os
import sys
import tempfile
import unittest
import importlib
from datetime import timedelta

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

# Prepare a temporary database before importing application modules.
_tempdir = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = os.path.join(_tempdir.name, "test_auth_routes.db")

import app.config as config
import app.database as database
import app.services.auth_service as auth_service
import app.main as app_main
import jwt
from fastapi.testclient import TestClient

importlib.reload(config)
importlib.reload(database)
importlib.reload(auth_service)
importlib.reload(app_main)

database.crear_tablas()
client = TestClient(app_main.app)


class AuthRoutesIntegrationTests(unittest.TestCase):
    def test_register_login_and_refresh(self):
        register_resp = client.post(
            "/api/auth/register",
            json={"email": "integration@example.com", "password": "StrongPass1"},
        )
        self.assertEqual(register_resp.status_code, 200)

        register_data = register_resp.json()
        self.assertIn("access_token", register_data)
        self.assertIn("refresh_token", register_data)

        login_resp = client.post(
            "/api/auth/login",
            json={"email": "integration@example.com", "password": "StrongPass1"},
        )
        self.assertEqual(login_resp.status_code, 200)

        login_data = login_resp.json()
        self.assertIn("access_token", login_data)
        self.assertIn("refresh_token", login_data)

        access_token = login_data["access_token"]
        refresh_token = login_data["refresh_token"]

        me_resp = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(me_resp.status_code, 200)
        me_data = me_resp.json()
        self.assertEqual(me_data["email"], "integration@example.com")

        refresh_resp = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        self.assertEqual(refresh_resp.status_code, 200)
        refresh_data = refresh_resp.json()
        self.assertIn("access_token", refresh_data)
        self.assertIn("refresh_token", refresh_data)

    def test_duplicate_registration_returns_400(self):
        client.post(
            "/api/auth/register",
            json={"email": "duplicate@example.com", "password": "Password123"},
        )
        duplicate_resp = client.post(
            "/api/auth/register",
            json={"email": "duplicate@example.com", "password": "Password123"},
        )
        self.assertEqual(duplicate_resp.status_code, 400)
        self.assertEqual(duplicate_resp.json()["detail"], "Email ya registrado")

    def test_expired_access_token_is_rejected(self):
        expired_token = auth_service.create_access_token(
            {"sub": "1", "email": "expired@example.com"}, expires_delta=timedelta(seconds=-5)
        )
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Token inválido o expirado")


if __name__ == "__main__":
    unittest.main()
