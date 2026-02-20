# Fraud-Flag Microservice API

A lightweight, test-backed RESTful fraud detection microservice built with Flask and SQLite.

Implements deterministic rule-based risk scoring, velocity-based transaction checks, persistent storage, and automated API testing.

---

## 🚀 Features

- RESTful API endpoints
- Deterministic rule-based fraud scoring engine
- Velocity-based transaction risk detection (time-window check)
- Persistent transaction storage (SQLite)
- Input validation and structured error handling
- Automated API tests using `pytest`
- Proper REST-compliant HTTP status codes (200, 201, 400, 404)

---

## 🏗 Architecture

Client Request → Flask API → Fraud Scoring Logic → SQLite Database → JSON Response

---

## 📌 API Endpoints

### Health Check  
`GET /health`

Response:
```json
{"status": "ok"}
```

---

### Create Transaction  
`POST /transactions`

Request:
```json
{
  "user_id": "u1",
  "amount": 1500,
  "country": "US"
}
```

Response:
```json
{
  "id": 1,
  "fraud_score": 0.8,
  "flagged": true
}
```

---

### List Transactions  
`GET /transactions?limit=10`

---

### Get Transaction by ID  
`GET /transactions/<id>`

---

## 🧠 Fraud Scoring Logic

Fraud score is computed using deterministic rules:

- Amount > 1000 → +0.5
- Country not SG → +0.3
- ≥3 transactions within 60 seconds → +0.4
- Score capped at 1.0
- Flagged if score ≥ 0.7

This rule-based approach ensures transparency and explainability of risk decisions.

---

## ✅ Test Coverage

This project includes automated API tests using `pytest`.

To run tests locally:

```bash
pytest -q
```

The test suite validates:
- Health endpoint availability
- Input validation and 400 error handling
- Successful transaction creation (201)
- Fraud scoring fields returned
- Transaction retrieval by ID
- Proper 404 handling
- Isolated test database configuration

---

## 📂 Project Structure

```
fraud-flag-microservice/
├── app.py              # Flask routes and fraud scoring logic
├── db.py               # Database layer abstraction
├── tests/              # Pytest test suite
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

- Python
- Flask
- SQLite
- Pytest
- RESTful API design principles

---

## ⚙️ How to Run Locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python app.py
```

Open:
http://127.0.0.1:5000/health

---

## 🧩 Design Decisions

- Separated application and database layers (`app.py` and `db.py`) to reduce coupling and improve maintainability.
- Implemented environment-based database configuration to enable isolated test databases.
- Applied deterministic rule-based fraud scoring for explainability and reproducibility.
- Used proper RESTful HTTP status codes (200, 201, 400, 404) for API compliance.
- Added automated tests with `pytest` to ensure endpoint reliability and prevent regressions.

---

## ⚡ Scalability Considerations

While SQLite is sufficient for lightweight local persistence, production deployment would require:

- PostgreSQL for concurrent write support
- Connection pooling
- Indexing on `user_id` and `created_at`
- Authentication and rate limiting middleware
- Containerization using Docker

---

## 🚧 Future Improvements

- Replace SQLite with PostgreSQL
- Add authentication and API key support
- Implement rate limiting per user
- Add CI pipeline (GitHub Actions)
- Containerize using Docker

---

## 📖 What I Learned

- Designing and structuring RESTful APIs with proper HTTP status codes
- Separating business logic from data access layers
- Implementing deterministic fraud scoring with time-window logic
- Writing automated API tests with isolated databases
- Building and documenting a production-style backend microservice