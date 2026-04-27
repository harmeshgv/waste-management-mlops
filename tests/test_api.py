from io import BytesIO

from PIL import Image
from sqlalchemy import text


def make_test_image_bytes():
    image = Image.new("RGB", (12, 12), color="green")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_health_endpoint_returns_running(client):
    test_client, _engine = client

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_predict_creates_pending_task_with_expected_coordinates(client):
    test_client, _engine = client

    response = test_client.post(
        "/predict",
        data={"city": "Chennai", "locality": "Perumbakkam"},
        files={"file": ("waste.png", make_test_image_bytes(), "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "prediction": "construction-waste",
        "severity": 2,
    }

    tasks_response = test_client.get("/tasks", params={"city": "Chennai"})
    tasks = tasks_response.json()["tasks"]

    assert tasks_response.status_code == 200
    assert tasks_response.json()["count"] == 1
    assert tasks[0]["city"] == "Chennai"
    assert tasks[0]["waste_type"] == "construction-waste"
    assert tasks[0]["severity"] == 2
    assert tasks[0]["lat"] == 12.915
    assert tasks[0]["lng"] == 80.229
    assert tasks[0]["status"] == "pending"


def test_predict_rejects_invalid_image(client):
    test_client, _engine = client

    response = test_client.post(
        "/predict",
        data={"city": "Chennai", "locality": "Perumbakkam"},
        files={"file": ("broken.txt", BytesIO(b"not-an-image"), "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid image"}


def test_route_returns_deduplicated_tasks_in_priority_order(client):
    test_client, engine = client

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO tasks (city, waste_type, severity, lat, lng, status)
            VALUES
            ('Chennai', 'packed', 1, 12.9000, 80.2000, 'pending'),
            ('Chennai', 'open_litter', 3, 12.9000, 80.2000, 'pending'),
            ('Chennai', 'construction-waste', 2, 13.0418, 80.2341, 'pending')
        """))

    response = test_client.get("/route", params={"city": "Chennai"})

    assert response.status_code == 200
    route = response.json()["route"]
    assert len(route) == 2
    assert route[0]["waste_type"] == "open_litter"
    assert route[0]["severity"] == 3
    assert route[1]["waste_type"] == "construction-waste"
    assert route[1]["severity"] == 2


def test_complete_marks_task_as_completed_and_hides_it_from_pending_list(client):
    test_client, engine = client

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO tasks (city, waste_type, severity, lat, lng, status)
            VALUES ('Chennai', 'packed', 1, 12.9791, 80.2212, 'pending')
        """))
        task_id = conn.execute(text("SELECT id FROM tasks")).scalar_one()

    response = test_client.post("/complete", params={"task_id": task_id})

    assert response.status_code == 200
    assert response.json() == {"message": "Task completed"}

    tasks_response = test_client.get("/tasks", params={"city": "Chennai"})
    assert tasks_response.status_code == 200
    assert tasks_response.json()["count"] == 0
    assert tasks_response.json()["tasks"] == []
