import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "astra_health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Экипаж
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crew (
            id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            age INTEGER,
            baseline_hr INTEGER,
            status TEXT
        )
    """)
    
    # История телеметрии
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            crew_id TEXT,
            heart_rate INTEGER,
            spo2 INTEGER,
            stress_level INTEGER,
            radiation_msev REAL
        )
    """)
    
    # Психологические опросники
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mental_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            crew_id TEXT,
            mood_score INTEGER,
            sleep_hours REAL,
            fatigue_index INTEGER,
            notes TEXT
        )
    """)
    
    # Заполнить экипаж, если пусто
    cursor.execute("SELECT COUNT(*) FROM crew")
    if cursor.fetchone()[0] == 0:
        initial_crew = [
            ("AST-01", "Alex Vance", "Commander", 42, 68, "Nominal"),
            ("AST-02", "Elena Rostova", "Medical Officer", 38, 72, "Nominal"),
            ("AST-03", "Marcus Chen", "Flight Engineer", 35, 65, "Nominal"),
            ("AST-04", "Sarah Jenkins", "Payload Specialist", 40, 70, "Nominal")
        ]
        cursor.executemany("INSERT INTO crew VALUES (?, ?, ?, ?, ?, ?)", initial_crew)
        conn.commit()
        
    conn.close()

def get_crew_list():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM crew", conn)
    conn.close()
    return df

def log_telemetry(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telemetry_history (timestamp, crew_id, heart_rate, spo2, stress_level, radiation_msev)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["timestamp"], data["crew_id"], data["heart_rate"], data["spo2"], data["stress_level"], data["radiation_msev"]))
    conn.commit()
    conn.close()

def get_telemetry_history(crew_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"SELECT * FROM telemetry_history WHERE crew_id = '{crew_id}' ORDER BY id DESC LIMIT 30", conn)
    conn.close()
    return df[::-1] # Разворачиваем для хронологического графика

def save_mental_log(crew_id, mood, sleep, fatigue, notes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mental_logs (timestamp, crew_id, mood_score, sleep_hours, fatigue_index, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), crew_id, mood, sleep, fatigue, notes))
    conn.commit()
    conn.close()

def get_mental_logs(crew_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"SELECT * FROM mental_logs WHERE crew_id = '{crew_id}' ORDER BY id DESC", conn)
    conn.close()
    return df