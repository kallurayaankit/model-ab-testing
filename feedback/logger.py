import sqlite3
import datetime

DB_PATH = "/data/feedback.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  user_id INTEGER,
                  model_version TEXT,
                  prediction REAL,
                  click INTEGER)''')
    conn.commit()
    conn.close()

def log_prediction(user_id, model_version, prediction):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO events (timestamp, user_id, model_version, prediction, click) VALUES (?,?,?,?,?)",
              (datetime.datetime.now().isoformat(), user_id, model_version, prediction, 0))
    conn.commit()
    conn.close()
    return c.lastrowid  # return event id for later click update

def log_click(event_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE events SET click = 1 WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def get_ctr():
    """Return CTR for each model version."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT model_version, SUM(click) as clicks, COUNT(*) as total FROM events GROUP BY model_version")
    rows = c.fetchall()
    conn.close()
    result = {}
    for model, clicks, total in rows:
        result[model] = clicks / total if total > 0 else 0
    return result