# Fraud-Flag Microservice API

A lightweight RESTful backend service built using Flask and SQLite to score and flag potentially fraudulent transactions using rule-based logic.

---

## 🚀 Features

- RESTful API endpoints
- Rule-based fraud scoring engine
- Persistent transaction storage (SQLite)
- Input validation and structured error handling
- Velocity-based fraud detection (time-window check)

---

## 🏗 Architecture

Client Request → Flask API → Fraud Scoring Logic → SQLite Database → JSON Response

---

## 📌 API Endpoints

### Health Check
GET /health

Response:
```json
{"status":"ok"}
```

---

### Create Transaction
POST /transactions

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
GET /transactions?limit=10

---

### Get Transaction by ID
GET /transactions/<id>

---

## 🧠 Fraud Scoring Logic

Fraud score is computed using deterministic rules:

- Amount > 1000 → +0.5
- Country not SG → +0.3
- ≥3 transactions within 60 seconds → +0.4
- Score capped at 1.0
- Flagged if score ≥ 0.7

---

## 🛠 Tech Stack

- Python
- Flask
- SQLite
- REST API Design

---

## ⚙️ How to Run Locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install flask
python app.py
```

Open:
http://127.0.0.1:5000/health

---

## 🧩 Design Decisions

- Separated database logic into `db.py` to improve maintainability.
- Implemented input validation to prevent malformed payloads.
- Used rule-based scoring for deterministic and explainable fraud decisions.
- Designed schema to store both input and computed fraud results.

---

## 🚧 Future Improvements

- Replace SQLite with PostgreSQL for higher concurrency.
- Add authentication and rate limiting.
- Add unit tests and CI pipeline.
- Containerize using Docker.

---

## 📖 What I Learned

- Designing RESTful APIs with proper HTTP status codes.
- Structuring backend logic separately from data access layers.
- Implementing time-based fraud detection logic.
- Building and documenting a production-style microservice.
