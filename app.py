from flask import Flask, request, render_template, redirect
import requests
import os
import psycopg2
from database import criar_tabelas
from pagamentos import gerar_link_pagamento

app = Flask(__name__)
TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
DATABASE_URL = os.getenv("DATABASE_URL")

criar_tabelas()

def conectar():
    return psycopg2.connect(DATABASE_URL)

def enviar_mensagem(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto}
    requests.post(url, json=payload)

def enviar_menu(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Você é:",
        "reply_markup": {
            "keyboard": [
                ["Sou Cliente"],
                ["Sou Prestador"]
            ],
            "resize_keyboard": True
        }
    }
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Bot online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            enviar_menu(chat_id)

        elif text == "Sou Prestador":
            enviar_mensagem(chat_id, "Digite seu nome:")

        elif text == "Sou Cliente":
            listar_prestadores(chat_id)

    return "ok"

def listar_prestadores(chat_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, servico, telefone FROM prestadores WHERE status='aprovado'")
    dados = cur.fetchall()

    resposta = "Prestadores disponíveis:\n\n"

    for nome, servico, telefone in dados:
        whatsapp = f"https://wa.me/{telefone}"
        resposta += f"{nome} - {servico}\nWhatsApp: {whatsapp}\n\n"

    enviar_mensagem(chat_id, resposta)

# PAINEL ADMIN
@app.route("/admin")
def admin():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prestadores WHERE status='pendente'")
    prestadores = cur.fetchall()
    return render_template("admin.html", prestadores=prestadores)

@app.route("/aprovar/<id>")
def aprovar(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE prestadores SET status='aprovado' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")

@app.route("/rejeitar/<id>")
def rejeitar(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE prestadores SET status='rejeitado' WHERE id=%s", (id,))
    conn.commit()
    return redirect("/admin")
