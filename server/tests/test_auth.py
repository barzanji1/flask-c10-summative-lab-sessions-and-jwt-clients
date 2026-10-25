
def test_signup(client):
    response = client.post("/signup", json={
        "username": "testuser",
        "password": "TestPass123!"
    })

    assert response.status_code == 201
    assert response.json["username"] == "testuser"


def test_login_invalid_password(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "TestPass123!"
    })

    response = client.post("/login", json={
        "username": "testuser",
        "password": "WrongPassword123!"
    })

    assert response.status_code == 401


def test_check_session_without_login(client):
    response = client.get("/check_session")

    assert response.status_code == 401


def test_logout(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "TestPass123!"
    })

    response = client.delete("/logout")

    assert response.status_code == 204

    check = client.get("/check_session")
    assert check.status_code == 401
