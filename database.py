import sqlite3
from datetime import datetime, timedelta

DB_NAME = "banco.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        cidade TEXT,
        categoria TEXT,
        descricao TEXT,
        plano TEXT,
        data_cadastro TEXT,
        data_vencimento TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= CADASTRO =================
def cadastrar_prestador(nome, telefone, cidade, categoria, descricao):
    conn = conectar()
    cursor = conn.cursor()

    data_cadastro = datetime.now()
    data_vencimento = data_cadastro + timedelta(days=15)

    cursor.execute("""
    INSERT INTO prestadores 
    (nome, telefone, cidade, categoria, descricao, plano, data_cadastro, data_vencimento, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nome, telefone, cidade, categoria, descricao,
        "gratis",
        str(data_cadastro),
        str(data_vencimento),
        "ativo"
    ))

    conn.commit()
    conn.close()

# ================= BUSCA =================
def buscar_prestadores(cidade, categoria):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, telefone, descricao, plano, status FROM prestadores
    WHERE cidade LIKE ? AND categoria LIKE ?
    ORDER BY 
        CASE 
            WHEN plano = 'premium' THEN 1
            WHEN plano = 'destaque' THEN 2
            WHEN plano = 'gratis' AND status = 'ativo' THEN 3
            WHEN status = 'vencido' THEN 4
        END
    """, (f"%{cidade}%", f"%{categoria}%"))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

# ================= VENCIMENTOS =================
def verificar_vencimentos():
    conn = conectar()
    cursor = conn.cursor()

    agora = datetime.now()

    cursor.execute("SELECT id, data_vencimento FROM prestadores")

    for id_prestador, data_vencimento in cursor.fetchall():
        if data_vencimento:
            if datetime.fromisoformat(data_vencimento) < agora:
                cursor.execute("""
                UPDATE prestadores 
                SET status = 'vencido'
                WHERE id = ?
                """, (id_prestador,))

    conn.commit()
    conn.close()

# ================= PLANOS =================
def colocar_destaque(id_prestador):
    conn = conectar()
    cursor = conn.cursor()

    vencimento = datetime.now() + timedelta(days=30)

    cursor.execute("""
    UPDATE prestadores
    SET plano = 'destaque',
        status = 'ativo',
        data_vencimento = ?
    WHERE id = ?
    """, (vencimento, id_prestador))

    conn.commit()
    conn.close()

def liberar_15_dias(id_prestador):
    conn = conectar()
    cursor = conn.cursor()

    vencimento = datetime.now() + timedelta(days=15)

    cursor.execute("""
    UPDATE prestadores
    SET status = 'ativo',
        data_vencimento = ?
    WHERE id = ?
    """, (vencimento, id_prestador))

    conn.commit()
    conn.close()
