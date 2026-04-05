import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabela():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        servico TEXT,
        telefone TEXT,
        cidade TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def adicionar_prestador(nome, servico, telefone, cidade):
    conn = conectar()
    c = conn.cursor()

    c.execute("INSERT INTO prestadores (nome, servico, telefone, cidade, status) VALUES (?, ?, ?, ?, ?)",
              (nome, servico, telefone, cidade, "Ativo"))

    conn.commit()
    conn.close()

def listar_prestadores():
    conn = conectar()
    c = conn.cursor()

    c.execute("SELECT nome, servico, telefone, cidade FROM prestadores WHERE status='Ativo'")
    dados = c.fetchall()

    conn.close()
    return dados

def excluir_prestador(nome):
    conn = conectar()
    c = conn.cursor()

    c.execute("DELETE FROM prestadores WHERE nome=?", (nome,))

    conn.commit()
    conn.close()
