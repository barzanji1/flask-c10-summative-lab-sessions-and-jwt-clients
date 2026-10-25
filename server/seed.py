
from app import app
from config import db
from models import User, Note


def seed_database():
    with app.app_context():

        username = "demo_user"

        user = User.query.filter_by(username=username).first()

        if user is None:
            user = User(username=username)
            user.set_password("DemoPass123!")

            db.session.add(user)
            db.session.flush()

            print("Created demo user.")

        if Note.query.filter_by(user_id=user.id).count() == 0:
            notes = [
                Note(
                    title="Welcome to Notes",
                    content="This is my first seeded note.",
                    user_id=user.id
                ),
                Note(
                    title="Learning Flask",
                    content="Flask makes it possible to build REST APIs.",
                    user_id=user.id
                ),
                Note(
                    title="Authentication",
                    content="Sessions keep track of logged-in users.",
                    user_id=user.id
                )
            ]

            db.session.add_all(notes)
            print("Created 3 demo notes.")

        db.session.commit()
        print("Database seeding complete.")


if __name__ == "__main__":
    seed_database()
