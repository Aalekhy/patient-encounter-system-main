def test_create_patient_success(client):
    response = client.post(
        "/patients",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.com",
            "phone": "9876543210",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john.doe@test.com"
    assert "id" in data


def test_create_patient_duplicate_email(client):
    response = client.post(
        "/patients",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john.doe@test.com",
            "phone": "9999999999",
        },
    )
    assert response.status_code == 400


def test_get_patient_success(client):
    response = client.get("/patients/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_patient_not_found(client):
    response = client.get("/patients/999")
    assert response.status_code == 404
