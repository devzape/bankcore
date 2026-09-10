def test_register_new_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    client.post("/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "otherpass"},
    )
    assert response.status_code == 400


def test_login_with_correct_credentials(client):
    client.post("/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "testpass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_wrong_password_fails(client):
    client.post("/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401