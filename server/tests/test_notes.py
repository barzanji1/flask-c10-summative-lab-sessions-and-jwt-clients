
def signup(client, username):
    return client.post("/signup", json={
        "username": username,
        "password": "TestPass123!"
    })


def test_create_note(client):
    signup(client, "alice")

    response = client.post("/notes", json={
        "title": "First Note",
        "content": "Learning Flask."
    })

    assert response.status_code == 201
    assert response.json["title"] == "First Note"
    assert response.json["user_id"] == 1


def test_get_notes_with_pagination(client):
    signup(client, "alice")

    for number in range(3):
        client.post("/notes", json={
            "title": f"Note {number}",
            "content": "Test content"
        })

    response = client.get("/notes?page=1&per_page=2")

    assert response.status_code == 200
    assert response.json["total"] == 3
    assert response.json["per_page"] == 2
    assert len(response.json["items"]) == 2
    assert response.json["total_pages"] == 2


def test_update_note(client):
    signup(client, "alice")

    created = client.post("/notes", json={
        "title": "Original",
        "content": "Original content"
    })

    note_id = created.json["id"]

    response = client.patch(f"/notes/{note_id}", json={
        "title": "Updated"
    })

    assert response.status_code == 200
    assert response.json["title"] == "Updated"


def test_delete_note(client):
    signup(client, "alice")

    created = client.post("/notes", json={
        "title": "Delete Me",
        "content": "Temporary note"
    })

    note_id = created.json["id"]

    deleted = client.delete(f"/notes/{note_id}")
    assert deleted.status_code == 204

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404


def test_user_cannot_access_another_users_note(client):
    signup(client, "alice")

    created = client.post("/notes", json={
        "title": "Private",
        "content": "Alice's private note"
    })

    note_id = created.json["id"]

    client.delete("/logout")
    signup(client, "bob")

    read_response = client.get(f"/notes/{note_id}")
    update_response = client.patch(
        f"/notes/{note_id}",
        json={"title": "Hacked"}
    )
    delete_response = client.delete(f"/notes/{note_id}")

    assert read_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404


def test_unauthenticated_user_cannot_create_note(client):
    response = client.post("/notes", json={
        "title": "Unauthorized",
        "content": "Should not be saved"
    })

    assert response.status_code == 401
