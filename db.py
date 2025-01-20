import sqlite3

DB_FILE = 'resul.db'
INIT_SQL = """
CREATE TABLE IF NOT EXISTS experiment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_type TEXT NOT NULL,
    formulation_id TEXT NOT NULL,
    calculated_value REAL NOT NULL,
    is_valid BOOLEAN NOT NULL
);
"""

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(INIT_SQL)
        conn.commit()

def add_results(results):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        for result in results:
            cur.execute(
                "INSERT INTO experiment_results (experiment_type, formulation_id, calculated_value, is_valid) VALUES (?, ?, ?, ?)",
                (result['experiment_type'], result['formulation_id'], result['calculated_value'], result['is_valid'])
            )
        conn.commit()

def fetch_experiment_types():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT experiment_type FROM experiment_results")
        return [row[0] for row in cur.fetchall()]

def fetch_results(experiment_type):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT formulation_id, calculated_value, is_valid FROM experiment_results WHERE experiment_type=?", (experiment_type,))
        return cur.fetchall()
    
def fetch_all_results():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT experiment_type, formulation_id, calculated_value, is_valid FROM experiment_results")
        return cur.fetchall()