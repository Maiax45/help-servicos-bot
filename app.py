from flask import Flask, request
import os
import requests

app = Flask(__name__)
TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"

@app.route("/")
def home():
    return "HOME OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Recebi uma mensagem do Telegram")
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            enviar_mensagem(chat_id, "Bot funcionando 100%!")

    return "ok", 200

def enviar_mensagem(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    requests.post(url, json=payload)
