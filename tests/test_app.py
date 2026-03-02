import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_success():
    # Arrange
    activity_name = "Soccer Team"
    email = "test@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")

def test_signup_already_signed_up():
    # Arrange
    activity_name = "Soccer Team"
    email = "test@example.com"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_signup_activity_not_found():
    # Arrange
    activity_name = "nonexistent"
    email = "test2@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
