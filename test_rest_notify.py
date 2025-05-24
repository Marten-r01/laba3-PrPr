import requests

def test_notify_endpoint():
    url = "http://localhost:8080/bot/notify"
    payload = {
        "chat_id": 42,
        "message": "Тестовое REST-уведомление"
    }
    res = requests.post(url, json=payload)
    assert res.status_code == 200
    assert res.json().get("status") == "ok"