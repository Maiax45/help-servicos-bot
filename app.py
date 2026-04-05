import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = 8625636756

prestadores = []

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

Digite qualquer mensagem para usar o menu abaixo.
"""

    if user_id == ADMIN_ID:
        msg += "\n👑 Você está como ADMIN"

    await update.message.reply_text(msg, reply_markup=menu(user_id))
    context.user_data["iniciou"] = True

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    # PRIMEIRA MENSAGEM
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

# WEBHOOK (RAILWAY)
PORT = int(os.environ.get("PORT", 8000))
URL = "https://SEU-PROJETO.up.railway.app"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", boas_vindas))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=URL
)
