from fastapi.testclient import TestClient

from knowitall.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_analysis() -> None:
    response = client.post(
        "/api/v1/analyses",
        json={
            "question": "修改订单字段会影响哪些页面？",
            "business_line_ids": ["commerce-order"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "CHANGE_IMPACT"
    assert payload["effective_scope"]["business_line_ids"] == ["commerce-order"]
