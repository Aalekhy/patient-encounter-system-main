def test_create_doctor_success(client):
    response = client.post(
        "/doctors", json={"name": "Dr Smith", "specialization": "Cardiology"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["is_active"] is True


def test_get_doctor_success(client):
    response = client.get("/doctors/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Dr Smith"


def test_get_doctor_not_found(client):
    response = client.get("/doctors/999")
    assert response.status_code == 404


def test_deactivate_doctor(client):
    response = client.patch("/doctors/1/deactivate")
    assert response.status_code == 200
    assert response.json()["is_active"] is False
