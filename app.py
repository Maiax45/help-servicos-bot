from flask import Flask, request
import os
import requests

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
app = Flask(__name__)

# Rota do webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            enviar_mensagem(chat_id, "Bem-vindo ao Help Serviços Maiax!")

    return 'ok'

# Função para enviar mensagem
def enviar_mensagem(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    requests.post(url, json=payload)

# Rota inicial
@app.route('/')
def home():
    return 'Bot rodando'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
