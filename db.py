import sqlite3
from typing import Any, Dict, List, Optional

DB_PATH = "fraud.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read rows like dicts
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id TEXT NOT NULL,
              amount REAL NOT NULL,
              country TEXT NOT NULL,
              created_at TEXT NOT NULL,
              fraud_score REAL NOT NULL,
              flagged INTEGER NOT NULL
            );
            """
        )
        conn.commit()

def insert_transaction(tx: Dict[str, Any]) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO transactions (user_id, amount, country, created_at, fraud_score, flagged)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                tx["user_id"],
                tx["amount"],
                tx["country"],
                tx["created_at"],
                tx["fraud_score"],
                1 if tx["flagged"] else 0,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)

def list_transactions(limit: int = 50) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

def get_transaction(tx_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM transactions WHERE id = ?",
            (tx_id,),
        ).fetchone()
        return dict(row) if row else None