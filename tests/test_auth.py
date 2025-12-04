def test_register_user(client):
    """Test POST /register returns token."""

    # Arrange
    user_data = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    #  Act - make request
    response = client.post("/api/v1/auth/register", json=user_data)

    # Assert
    assert response.status_code == 201

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0

def test_duplicate_email_registration(client):
    """Test POST /register duplicate email returning email"""

    # Arrange
    user_data_1 = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    user_data_2 = {
        "email": "user@test.com",
        "full_name": "Test User2",
        "password": "testPassword2"
    }

    # Act
    client.post("/api/v1/auth/register", json=user_data_1)
    response = client.post("/api/v1/auth/register", json=user_data_2)

    # Assert
    data = response.json()
    assert response.status_code == 400
    assert "User already exist" in data["detail"]

def test_invalid_email_format(client):
    """Test POST /register return error if invalid email format"""

    # Arrange
    user_data = {
        "email": "usertest.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    # Act
    response = client.post("/api/v1/auth/register", json=user_data)

    # Assert
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "email" for error in errors)

def test_login_success(client):
    """Test POST /login success"""

    # Arrange
    registration_data = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    login_data = {
        "email": "user@test.com",
        "password": "testPassword"
    }

    # Act
    client.post("/api/v1/auth/register", json=registration_data)
    response = client.post("/api/v1/auth/login", json=login_data)

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0

def test_incorrect_password(client):
    """Test POST /login Incorrect password"""

    # Arrange
    registration_data = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    login_data = {
        "email": "user@test.com",
        "password": "wrongPassword"
    }

    # Act
    client.post("/api/v1/auth/register", json=registration_data)
    response = client.post("/api/v1/auth/login", json=login_data)

    # Assert
    assert response.status_code == 401
    error = response.json()["detail"]
    assert "Invalid Credentials" in error

def test_wrong_user(client):
    """Test POST /login non-existent user"""

    # Arrange
    login_data = {
        "email": "user@wrong.com",
        "password": "testPassword"
    }

    # Act
    response = client.post("/api/v1/auth/login", json=login_data)

    # Assert
    assert response.status_code == 401
    error = response.json()["detail"]
    assert "Invalid Credentials" in error

from app.core.security import decode_access_token
from jose import jwt
from app.config import settings

def test_valid_refresh_token(client):
    """Test POST /refresh resfresh token"""

    # Arrange
    registration_data = {
        "email": "user@test.com",
        "full_name": "Test User",
        "password": "testPassword"
    }

    client.post("/api/v1/auth/register", json=registration_data)

    login_response = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "testPassword"
    })
    original_tokens = login_response.json()

    refresh_response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": original_tokens["refresh_token"]
    })
    new_tokens = refresh_response.json()

    # Decode and compare expiration times
    original_access = jwt.decode(original_tokens["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    new_access = jwt.decode(new_tokens["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Assert
    assert original_access["exp"] <= new_access["exp"]