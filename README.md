# devtrack

A small Django REST API for tracking reporters and issues. Data is stored in JSON files under `issues/files/`.

## Setup

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework
```

## Run the server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

## Reporter endpoints

Base URL: `/api/reporters/` (keep the trailing slash)

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/reporters/` | Create a reporter |
| `GET` | `/api/reporters/` | List all reporters |
| `GET` | `/api/reporters/?id=1` | Get one reporter by id |

**Create a reporter**

```bash
curl -X POST http://127.0.0.1:8000/api/reporters/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Priya Sharma", "email": "priya.sharma@example.com", "team": "qa"}'
```

| Field | Rules |
|-------|-------|
| `name` | required, not empty |
| `email` | required, must contain `@` |
| `team` | required, one of `backend`, `frontend`, `qa`, `devops` |

The `id` is assigned by the server.

**Responses**

| Status | When |
|--------|------|
| `201` | Reporter created |
| `200` | Reporter(s) returned |
| `400` | Missing fields, invalid team or email, or non-numeric `id` |
| `404` | No reporter with that `id` |
| `405` | Method not allowed (for example `DELETE`) |

Example (`201 Created`):

![Create reporter](photos/reporters/06-create-reporter-201.png)

More Postman screenshots, one for each success and error case, are in [`photos/reporters/`](photos/reporters/).
