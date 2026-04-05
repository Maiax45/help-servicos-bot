import sqlite3
from datetime import datetime, timedelta

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
        data_cadastro TEXT,
        data_vencimento TEXT,
        status TEXT,
        destaque INTEGER
    )
    """)

    conn.commit()
    conn.close()

def adicionar_prestador(nome, servico, telefone, cidade):
    conn = conectar()
    c = conn.cursor()

    data_cadastro = datetime.now()
    vencimento = data_cadastro + timedelta(days=15)

    c.execute("""
    INSERT INTO prestadores 
    (nome, servico, telefone, cidade, data_cadastro, data_vencimento, status, destaque)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, servico, telefone, cidade, data_cadastro, vencimento, "Ativo", 0))

    conn.commit()
    conn.close()

def listar_por_servico(servico):
    conn = conectar()
    c = conn.cursor()

    hoje = datetime.now()

    c.execute("""
    SELECT nome, servico, telefone, cidade, destaque
    FROM prestadores
    WHERE servico LIKE ? AND status='Ativo' AND data_vencimento >= ?
    ORDER BY destaque DESC
    """, ('%' + servico + '%', hoje))

    dados = c.fetchall()
    conn.close()
    return dados

def listar_todos():
    conn = conectar()
    c = conn.cursor()

    c.execute("SELECT nome, servico, status, data_vencimento FROM prestadores")
    dados = c.fetchall()

    conn.close()
    return dados

def prestadores_vencendo():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    SELECT nome, servico, data_vencimento
    FROM prestadores
    WHERE date(data_vencimento) <= date('now', '+3 day')
    """)

    dados = c.fetchall()
    conn.close()
    return dados

def ativar_pagamento(nome):
    conn = conectar()
    c = conn.cursor()

    nova_data = datetime.now() + timedelta(days=30)

    c.execute("""
    UPDATE prestadores
    SET data_vencimento=?, status='Ativo'
    WHERE nome=?
    """, (nova_data, nome))

    conn.commit()
    conn.close()

def excluir_prestador(nome):
    conn = conectar()
    c = conn.cursor()

    c.execute("DELETE FROM prestadores WHERE nome=?", (nome,))
    conn.commit()
    conn.close()

def tornar_destaque(nome):
    conn = conectar()
    c = conn.cursor()

    c.execute("UPDATE prestadores SET destaque=1 WHERE nome=?", (nome,))
    conn.commit()
    conn.close()
