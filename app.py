from flask import Flask, jsonify, request
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Tuple

import db

app = Flask(__name__)
db.init_db()

# --- Helpers: validation & scoring ---

def parse_transaction_payload(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Basic input validation. Returns (ok, error_message).
    """
    required = ["user_id", "amount", "country"]
    for k in required:
        if k not in data:
            return False, f"Missing required field: {k}"

    if not isinstance(data["user_id"], str) or not data["user_id"].strip():
        return False, "user_id must be a non-empty string"

    # amount can be int or float
    if not isinstance(data["amount"], (int, float)):
        return False, "amount must be a number"
    if data["amount"] < 0:
        return False, "amount must be >= 0"

    if not isinstance(data["country"], str) or len(data["country"].strip()) < 2:
        return False, "country must be a valid string (e.g., 'SG')"

    return True, ""

def count_recent_transactions(user_id: str, seconds: int = 60) -> int:
    """
    Simple approach: fetch recent entries and count those within window.
    For a tiny project this is fine; in real systems you'd index + query by time.
    """
    # We'll just scan last 50 for simplicity
    recent = db.list_transactions(limit=50)
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=seconds)
    count = 0
    for tx in recent:
        if tx["user_id"] != user_id:
            continue
        try:
            created_at = datetime.fromisoformat(tx["created_at"])
        except ValueError:
            continue
        if created_at >= cutoff:
            count += 1
    return count

def fraud_score(user_id: str, amount: float, country: str) -> float:
    score = 0.0

    if amount > 1000:
        score += 0.5

    if country.strip().upper() != "SG":
        score += 0.3

    # velocity check
    recent_count = count_recent_transactions(user_id=user_id, seconds=60)
    if recent_count >= 3:
        score += 0.4

    return min(score, 1.0)

# --- Routes ---

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    ok, err = parse_transaction_payload(data)
    if not ok:
        return jsonify({"error": err}), 400

    user_id = data["user_id"].strip()
    amount = float(data["amount"])
    country = data["country"].strip().upper()

    score = fraud_score(user_id, amount, country)
    flagged = score >= 0.7  # threshold can be tuned

    tx = {
        "user_id": user_id,
        "amount": amount,
        "country": country,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "fraud_score": score,
        "flagged": flagged,
    }

    tx_id = db.insert_transaction(tx)
    return jsonify({"id": tx_id, "fraud_score": score, "flagged": flagged}), 201

@app.route("/transactions", methods=["GET"])
def list_all_transactions():
    limit_raw = request.args.get("limit", "50")
    try:
        limit = max(1, min(int(limit_raw), 200))
    except ValueError:
        return jsonify({"error": "limit must be an integer"}), 400

    items = db.list_transactions(limit=limit)
    return jsonify({"transactions": items, "count": len(items)}), 200

@app.route("/transactions/<int:tx_id>", methods=["GET"])
def get_one_transaction(tx_id: int):
    item = db.get_transaction(tx_id)
    if item is None:
        return jsonify({"error": "transaction not found"}), 404
    return jsonify(item), 200

if __name__ == "__main__":
    app.run(debug=True)