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

if __name__ == "__main__":
    t = threading.Thread(target=rodar_bot)
    t.start()

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
