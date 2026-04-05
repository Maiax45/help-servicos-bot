import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = 8625636756
URL = "web-production-8e168.up.railway.app"  # URL do Railway

prestadores = []

app_flask = Flask(__name__)

def menu(user_id):
    if user_id == ADMIN_ID:
        return ReplyKeyboardMarkup([
            ["🔎 Buscar Serviço"],
            ["📝 Cadastrar Prestador"],
            ["📖 Como Usar"],
            ["👑 Admin"]
        ], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([
            ["🔎 Buscar Serviço"],
            ["📝 Cadastrar Prestador"],
            ["📖 Como Usar"]
        ], resize_keyboard=True)

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    msg = """
👋 Bem-vindo à Help Serviços Maiax!

Digite qualquer mensagem para abrir o menu e encontrar um profissional.
"""

    if user_id == ADMIN_ID:
        msg += "\n👑 Você é ADMIN"

    await update.message.reply_text(msg, reply_markup=menu(user_id))
    context.user_data["iniciou"] = True

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    if not context.user_data.get("iniciou"):
        await boas_vindas(update, context)
        return

    if texto == "🔎 Buscar Serviço":
        await update.message.reply_text("Digite o serviço:")
        context.user_data["busca"] = True

    elif context.user_data.get("busca"):
        resultados = [p for p in prestadores if texto.lower() in p["servico"].lower()]

        if not resultados:
            await update.message.reply_text("Nenhum prestador encontrado.")
        else:
            for p in resultados:
                msg = f"""
🔧 {p['servico']}
👤 {p['nome']}
📍 {p['cidade']}
📞 {p['telefone']}
"""
                await update.message.reply_text(msg)

        context.user_data["busca"] = False

    elif texto == "📝 Cadastrar Prestador":
        await update.message.reply_text("Envie:\nNome - Serviço - Telefone - Cidade")
        context.user_data["cadastro"] = True

    elif context.user_data.get("cadastro"):
        try:
            nome, servico, telefone, cidade = texto.split(" - ")

            prestadores.append({
                "nome": nome,
                "servico": servico,
                "telefone": telefone,
                "cidade": cidade
            })

            await update.message.reply_text("Cadastro realizado!")
        except:
            await update.message.reply_text("Formato inválido.")

        context.user_data["cadastro"] = False

    elif texto == "👑 Admin":
        if user_id != ADMIN_ID:
            await update.message.reply_text("Acesso negado.")
            return

        msg = "Prestadores cadastrados:\n"
        for p in prestadores:
            msg += f"{p['nome']} - {p['servico']}\n"

        await update.message.reply_text(msg)

# TELEGRAM BOT
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", boas_vindas))
bot_app.add_handler(MessageHandler(filters.TEXT, mensagens))

# WEBHOOK ROUTE
@app_flask.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "ok"

@app_flask.route("/")
def home():
    return "Bot rodando!"

if __name__ == "__main__":
    bot_app.bot.set_webhook(f"{URL}/{TOKEN}")
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
