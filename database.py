import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DATABASE_URL)

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        servico TEXT,
        telefone TEXT,
        cidade TEXT,
        status TEXT,
        plano TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()
