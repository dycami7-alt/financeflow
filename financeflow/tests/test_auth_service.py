import os
import sys
import tempfile
import unittest
from datetime import timedelta
import importlib

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

# Set a temporary database before importing application modules.
_tempdir = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = os.path.join(_tempdir.name, "test_auth_service.db")

import app.config as config
import app.database as database
import app.services.auth_service as auth_service
import jwt

importlib.reload(config)
importlib.reload(database)
importlib.reload(auth_service)

database.crear_tablas()


class AuthServiceUnitTests(unittest.TestCase):
    def test_hash_and_verify_password(self):
        hashed = auth_service.hash_password("secret123")
        self.assertTrue(auth_service.verify_password("secret123", hashed))
        self.assertFalse(auth_service.verify_password("wrong-password", hashed))

    def test_create_access_token_contains_claims(self):
        token = auth_service.create_access_token({"sub": "123", "email": "test@example.com"}, expires_delta=timedelta(minutes=1))
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        self.assertEqual(payload["sub"], "123")
        self.assertEqual(payload["email"], "test@example.com")
        self.assertEqual(payload["type"], "access")

    def test_refresh_token_is_verified(self):
        token = auth_service.create_refresh_token({"sub": "123", "email": "test@example.com"}, expires_delta=timedelta(minutes=1))
        payload = auth_service.verify_refresh_token(token)
        self.assertEqual(payload["sub"], "123")
        self.assertEqual(payload["type"], "refresh")

    def test_expired_access_token_raises_expired_signature(self):
        token = auth_service.create_access_token({"sub": "123"}, expires_delta=timedelta(seconds=-1))
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

    def test_user_registration_and_authentication(self):
        email = "user1@example.com"
        password = "TestPass123"
        user_id = auth_service.create_user(email, password)
        self.assertGreater(user_id, 0)

        user = auth_service.authenticate_user(email, password)
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], email)
        self.assertIsNone(auth_service.authenticate_user(email, "badpass"))


if __name__ == "__main__":
    unittest.main()
