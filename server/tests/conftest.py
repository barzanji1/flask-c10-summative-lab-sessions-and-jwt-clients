
import os
import tempfile

import pytest

# Set the database before app.py creates the Flask app.
_test_directory = tempfile.TemporaryDirectory()
_test_database = os.path.join(_test_directory.name, "test.db")

os.environ["DATABASE_URL"] = f"sqlite:///{_test_database}"
os.environ["SECRET_KEY"] = "pytest-only-secret-key"

from app import app
from config import db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()
