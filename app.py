from flask import Flask, request
import sqlite3
import datetime
import os
from telegram import Bot, Update

TOKEN = "8625636756:AAHRL7_-JLbf5jPSknlkR2gSB6QblvKiBhw"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# ================= BANCO =================
def conectar():
    return sqlite3.connect("banco.db")

def criar_banco():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        servico TEXT,
        cidade TEXT,
        telefone TEXT,
        vencimento TEXT,
        destaque INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

criar_banco()

# ================= WEBHOOK =================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        texto = update.message.text

        if texto == "/start":
            bot.send_message(update.message.chat.id,
                             "Bem-vindo ao Help Serviços Maiax\n\n"
                             "Digite:\nCadastrar Prestador\nProcurar Prestador")

        elif texto == "Cadastrar Prestador":
            bot.send_message(update.message.chat.id,
                             "Digite:\nNome - Serviço - Cidade - Telefone")

        elif "-" in texto:
            try:
                dados = texto.split("-")
                nome = dados[0].strip()
                servico = dados[1].strip()
                cidade = dados[2].strip()
                telefone = dados[3].strip()

                vencimento = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime("%Y-%m-%d")

                conn = conectar()
                c = conn.cursor()
                c.execute("INSERT INTO prestadores (nome, servico, cidade, telefone, vencimento) VALUES (?,?,?,?,?)",
                          (nome, servico, cidade, telefone, vencimento))
                conn.commit()
                conn.close()

                bot.send_message(update.message.chat.id, "Prestador cadastrado com 15 dias grátis!")
            except:
                bot.send_message(update.message.chat.id, "Erro no cadastro.")

        elif texto == "Procurar Prestador":
            conn = conectar()
            c = conn.cursor()
            c.execute("SELECT nome, servico, cidade, telefone FROM prestadores WHERE destaque = 1")
            dados = c.fetchall()
            conn.close()

            if dados:
                resposta = "Prestadores em destaque:\n\n"
                for d in dados:
                    resposta += f"Nome: {d[0]}\nServiço: {d[1]}\nCidade: {d[2]}\nTelefone: {d[3]}\n\n"
            else:
                resposta = "Nenhum prestador em destaque."

            bot.send_message(update.message.chat.id, resposta)

    return "ok"

# ================= SET WEBHOOK =================
@app.route("/setwebhook")
def set_webhook():
    url = os.getenv("URL")
    bot.set_webhook(f"{url}/{TOKEN}")
    return "Webhook configurado!"
