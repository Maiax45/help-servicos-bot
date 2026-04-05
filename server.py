from flask import Flask
import threading
import os
from app import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Help Serviços Maiax está online!"

def rodar_bot():
    main()

def start():
    t = threading.Thread(target=rodar_bot)
    t.start()

start()
