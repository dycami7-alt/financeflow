import os
import sys
import tempfile
import unittest
import importlib

TEST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if TEST_ROOT not in sys.path:
    sys.path.insert(0, TEST_ROOT)

import app.config as config
import app.database as database
import app.services.perfil_service as perfil_service
import app.main as app_main
from fastapi.testclient import TestClient

importlib.reload(config)
importlib.reload(database)
importlib.reload(perfil_service)
importlib.reload(app_main)

database.crear_tablas()
client = TestClient(app_main.app)


class FinancialScenarioTests(unittest.TestCase):
    def test_scenarios_are_defined(self):
        scenarios = perfil_service.get_financial_scenarios()
        self.assertEqual(len(scenarios), 5)
        for scenario in scenarios:
            self.assertIn("scenario_id", scenario)
            self.assertIn("options", scenario)
            self.assertGreater(len(scenario["options"]), 1)

    def test_evaluate_all_good_decisions(self):
        decisions = [
            {"scenario_id": 1, "selected_option": "A"},
            {"scenario_id": 2, "selected_option": "A"},
            {"scenario_id": 3, "selected_option": "A"},
            {"scenario_id": 4, "selected_option": "A"},
            {"scenario_id": 5, "selected_option": "A"},
        ]
        result = perfil_service.evaluate_financial_decisions(decisions)
        self.assertEqual(result["total_score"], 100)
        self.assertEqual(result["percentage"], 100)
        self.assertEqual(result["evaluation_message"], "Excelente: tus decisiones son sólidas y están bien orientadas financieramente.")
        self.assertTrue(all(item["quality"] == "buena" for item in result["results"]))

    def test_evaluate_decisions_route(self):
        decisions = [
            {"scenario_id": 1, "selected_option": "A"},
            {"scenario_id": 2, "selected_option": "B"},
            {"scenario_id": 3, "selected_option": "A"},
            {"scenario_id": 4, "selected_option": "C"},
            {"scenario_id": 5, "selected_option": "A"},
        ]
        response = client.post("/api/perfil/decisions", json={"decisions": decisions})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["max_score"], 100)
        self.assertEqual(data["percentage"], 60)
        self.assertEqual(data["total_score"], 60)
        self.assertEqual(data["results"][1]["quality"], "mala")
        self.assertEqual(data["results"][3]["quality"], "mala")

    def test_invalid_decision_returns_400(self):
        response = client.post("/api/perfil/decisions", json={"decisions": []})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "decisions es requerido y debe ser una lista")


if __name__ == "__main__":
    unittest.main()
