import requests

# Datos de prueba para el perfilador
test_data = {
    "user_id": 1,
    "answers": [
        {"question_id": 1, "answer_id": 1, "points": 3, "type": "conservative"},
        {"question_id": 2, "answer_id": 1, "points": 3, "type": "conservative"},
        {"question_id": 3, "answer_id": 1, "points": 3, "type": "conservative"},
        {"question_id": 4, "answer_id": 1, "points": 3, "type": "conservative"},
        {"question_id": 5, "answer_id": 1, "points": 3, "type": "conservative"},
        {"question_id": 6, "answer_id": 1, "points": 3, "type": "conservative"},
    ]
}

try:
    response = requests.post("http://127.0.0.1:8000/api/perfil/quiz", json=test_data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)