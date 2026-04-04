from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "HOME OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook recebido")
    return "ok", 200
