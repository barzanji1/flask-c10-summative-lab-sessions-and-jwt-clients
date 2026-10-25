# Notes API — Flask Summative Lab

A RESTful Notes API built with Python, Flask, SQLAlchemy, and session-based authentication.

## Features

- User registration and login
- Secure password hashing using Flask-Bcrypt
- Session-based authentication
- Create, read, update, and delete notes
- User-specific note ownership and authorization
- Paginated note retrieval
- Database migrations using Flask-Migrate
- Database seeding
- Automated testing using pytest

## Technologies

- Python 3.8
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite
- pytest
- Pipenv

## Installation

Clone the repository and navigate to the backend:

```bash
git clone git@github.com:barzanji1/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

Install dependencies:

```bash
pipenv install --dev
```

Set a local development secret key:

```bash
export SECRET_KEY="replace-with-a-long-random-secret"
```

Apply database migrations:

```bash
pipenv run flask --app app db upgrade
```

Start the API:

```bash
pipenv run python app.py
```

The development API runs at `http://127.0.0.1:5555`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a user |
| POST | `/login` | Authenticate a user |
| GET | `/check_session` | Check the current session |
| DELETE | `/logout` | Log out |
| GET | `/notes` | Retrieve paginated notes |
| POST | `/notes` | Create a note |
| GET | `/notes/<id>` | Retrieve a note |
| PATCH | `/notes/<id>` | Update a note |
| DELETE | `/notes/<id>` | Delete a note |

### Pagination

Example:

`GET /notes?page=1&per_page=5`

Returns notes belonging to the authenticated user, with pagination metadata.

## Database Seeding

Run:

```bash
pipenv run python seed.py
```

This creates a demonstration user and three sample notes if the demo user does not already have notes.

Demo credentials for local development:

- Username: `demo_user`
- Password: `DemoPass123!`

Do not deploy the demo account with these credentials in production.

## Automated Testing

Run:

```bash
pipenv run python -m pytest tests/ -v
```

The test suite covers authentication, Notes CRUD, pagination, and cross-user authorization.

Latest verified result: **10 tests passed**.

## Security

- Passwords are stored as bcrypt hashes.
- Protected endpoints require authentication.
- Notes are restricted to their authenticated owners.
- Unauthorized access to another user's note returns HTTP 404.
- The application uses a signed Flask session cookie.

For production deployment, configure a strong secret key, HTTPS, secure cookie settings, and CSRF protection for cookie-authenticated state-changing requests.

## Project Status

Backend functionality implemented and verified through manual API requests and automated tests.