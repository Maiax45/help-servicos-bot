from flask import Flask
import threading
import os
from app import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Help Serviços Maiax está online!"

def iniciar_bot():
    main()

if __name__ == "__main__":
    iniciar_bot()
else:
    t = threading.Thread(target=iniciar_bot)
    t.daemon = True
    t.start()
