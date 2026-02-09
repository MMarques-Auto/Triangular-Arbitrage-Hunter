import sqlite3
from datetime import datetime
import os

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            base_pair TEXT,
            middle_pair TEXT,
            final_pair TEXT,
            t_profit REAL,
            r_profit REAL,
            status TEXT,
            reason TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DB] Banco de dados iniciado e verificado | {DB_NAME}")

def save(t, t_profit, r_profit, status, reason):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if isinstance(t_profit, dict):
            t_profit = t_profit.get('lucro_pct', 0.0)
            
        if isinstance(r_profit, dict):
            r_profit = r_profit.get('lucro_pct', 0.0)

        try:
            t_profit = float(t_profit)
        except:
            t_profit = 0.0
            
        try:
            r_profit = float(r_profit)
        except:
            r_profit = 0.0

        p_base = t.get('base_pair') or t.get('par_compra') or t.get('moeda_base') or "N/A"
        p_meio = t.get('middle_pair') or t.get('par_meio') or "N/A"
        p_fim  = t.get('final_pair') or t.get('par_venda') or "N/A"
        
        cursor.execute('''
            INSERT INTO historico (date, base_pair, middle_pair, final_pair, t_profit, r_profit, status, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            date_str,
            p_base,
            p_meio,
            p_fim,
            t_profit,
            r_profit,
            status,
            reason
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"[ERRO CRÍTICO DB] Ainda falhou: {e}")
        print(f"Dados rejeitados -> TP: {type(t_profit)} | RP: {type(r_profit)}")