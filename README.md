# Patient Encounter System

Production-grade backend API for managing patients, doctors, and appointments.

Built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **Poetry**, with proper
validation, conflict detection, testing, and CI.

---

## Features

- Patient management (create, fetch, delete with rules)
- Doctor management (create, activate/deactivate, delete with rules)
- Appointment scheduling with:
  - timezone-aware datetime enforcement
  - no past appointments
  - duration validation (15–180 minutes)
  - doctor availability checks
  - overlap prevention (per doctor)
- Shared MySQL-safe design (table prefixing)
- Unit tests (SQLite in-memory)
- CI with Ruff, Black, Bandit, Pytest

---

## Tech Stack

- Python 3.10
- FastAPI
- SQLAlchemy ORM
- MySQL (PyMySQL)
- Poetry
- Pytest
- GitHub Actions CI

---

## Setup & Run (Local)

### 1. Install dependencies
```bash
poetry install
```

### 2. Configure database
Set environment variable:
```bash
export DATABASE_URL="mysql+pymysql://user:pass@host:3306/dbname"
```
(or create `src/config_local.py` with `DATABASE_URL = "..."`)

### 3. Run the server
```bash
poetry run uvicorn src.main:app --reload
```

### 4. Open API docs
```
http://127.0.0.1:8000/docs
```

---

## Run Tests

```bash
poetry run pytest
```

---

## CI

On every push and pull request, GitHub Actions runs:
- Ruff (lint)
- Black (format check)
- Bandit (security)
- Pytest (unit tests)

---

## Author

Aaryan Singh
