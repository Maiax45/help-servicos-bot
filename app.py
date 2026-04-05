from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import criar_tabela, adicionar_prestador, listar_prestadores

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"

criar_tabela()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        ["🔎 Procurar Prestador"],
        ["📝 Cadastrar como Prestador"],
        ["📞 Falar no WhatsApp"]
    ]

    await update.message.reply_text(
        "Bem-vindo à Help Serviços Maiax!\nEscolha uma opção:",
        reply_markup=ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    )

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if texto == "🔎 Procurar Prestador":
        prestadores = listar_prestadores()

        if not prestadores:
            await update.message.reply_text("Nenhum prestador cadastrado.")
            return

        resposta = "Prestadores disponíveis:\n\n"
        for p in prestadores:
            resposta += f"Nome: {p[0]}\nServiço: {p[1]}\nTelefone: {p[2]}\nCidade: {p[3]}\n\n"

        await update.message.reply_text(resposta)

    elif texto == "📝 Cadastrar como Prestador":
        await update.message.reply_text(
            "Envie:\nNome - Serviço - Telefone - Cidade\n\nExemplo:\nJoão - Eletricista - 38999999999 - Montes Claros"
        )
        context.user_data["cadastro"] = True

    elif context.user_data.get("cadastro"):
        try:
            nome, servico, telefone, cidade = texto.split(" - ")
            adicionar_prestador(nome, servico, telefone, cidade)

            await update.message.reply_text("Cadastro realizado com sucesso!")
            context.user_data["cadastro"] = False
        except:
            await update.message.reply_text("Formato inválido.")

    elif texto == "📞 Falar no WhatsApp":
        await update.message.reply_text("https://wa.me/5538999999999")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

print("Bot rodando...")
app.run_polling()

