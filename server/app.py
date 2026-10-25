
from config import create_app, db
from models import User, Note
from flask import request, session

app = create_app()


@app.route("/")
def index():
    return {"message": "Notes API is running"}, 200


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "A JSON object is required"}, 400

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not isinstance(username, str) or not username.strip():
        return {"error": "Username is required"}, 400

    if not isinstance(password, str) or len(password) < 8:
        return {"error": "Password must be at least 8 characters"}, 400

    if (
        password_confirmation is not None
        and password_confirmation != password
    ):
        return {"error": "Passwords do not match"}, 400

    username = username.strip()

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id

    return user.to_dict(), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "A JSON object is required"}, 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return {"error": "Username and password are required"}, 400

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return {"error": "Invalid username or password"}, 401

    session.clear()
    session["user_id"] = user.id

    return user.to_dict(), 200


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "Not authenticated"}, 401

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()
        return {"error": "Not authenticated"}, 401

    return user.to_dict(), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return {}, 204


@app.route("/notes", methods=["GET", "POST"])
def notes():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "Authentication required"}, 401

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()
        return {"error": "Authentication required"}, 401

    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        if page < 1 or per_page < 1 or per_page > 100:
            return {"error": "Invalid pagination parameters"}, 400

        pagination = Note.query.filter_by(
            user_id=user.id
        ).order_by(Note.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": [
                note.to_dict() for note in pagination.items
            ]
        }, 200

    if request.method == "POST":
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {"error": "A JSON object is required"}, 400

        title = data.get("title")
        content = data.get("content")

        if not isinstance(title, str) or not title.strip():
            return {"error": "Title is required"}, 400

        if len(title.strip()) > 200:
            return {"error": "Title must be 200 characters or fewer"}, 400

        if not isinstance(content, str) or not content.strip():
            return {"error": "Content is required"}, 400

        note = Note(
            title=title.strip(),
            content=content,
            user_id=user.id
        )

        db.session.add(note)
        db.session.commit()

        return note.to_dict(), 201


@app.route("/notes/<int:note_id>", methods=["GET", "PATCH", "DELETE"])
def note_detail(note_id):
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "Authentication required"}, 401

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()
        return {"error": "Authentication required"}, 401

    note = Note.query.filter_by(
        id=note_id,
        user_id=user.id
    ).first()

    if note is None:
        return {"error": "Note not found"}, 404

    if request.method == "GET":
        return note.to_dict(), 200

    if request.method == "PATCH":
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {"error": "A JSON object is required"}, 400

        if "title" not in data and "content" not in data:
            return {"error": "Provide title or content"}, 400

        if "title" in data:
            title = data["title"]

            if not isinstance(title, str) or not title.strip():
                return {"error": "Title cannot be empty"}, 400

            if len(title.strip()) > 200:
                return {"error": "Title must be 200 characters or fewer"}, 400

            note.title = title.strip()

        if "content" in data:
            content = data["content"]

            if not isinstance(content, str) or not content.strip():
                return {"error": "Content cannot be empty"}, 400

            note.content = content

        db.session.commit()
        return note.to_dict(), 200

    if request.method == "DELETE":
        db.session.delete(note)
        db.session.commit()
        return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
