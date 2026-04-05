from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = 8625636756  # SEU ID

prestadores = []

# MENU
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

# BOAS VINDAS
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    msg = """
👋 Bem-vindo à *Help Serviços Maiax*!

📌 *COMO USAR:*

👥 *CLIENTE:*
1. Clique em *Buscar Serviço*
2. Digite o serviço (ex: eletricista)
3. Escolha o profissional
4. Entre em contato

👨‍🔧 *PRESTADOR:*
1. Clique em *Cadastrar Prestador*
2. Envie:
Nome - Serviço - Telefone - Cidade

Exemplo:
João - Eletricista - 38999999999 - Montes Claros
"""

    if user_id == ADMIN_ID:
        msg += "\n\n👑 Você está como ADMIN"

    await update.message.reply_text(msg, reply_markup=menu(user_id))
    context.user_data["iniciou"] = True

# MENSAGENS
async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    # SE FOR A PRIMEIRA MENSAGEM → MOSTRA MENU
    if not context.user_data.get("iniciou"):
        await boas_vindas(update, context)
        return

    # BUSCAR
    if texto == "🔎 Buscar Serviço":
        await update.message.reply_text("Digite o serviço:")
        context.user_data["busca"] = True

    elif context.user_data.get("busca"):
        resultados = [p for p in prestadores if texto.lower() in p["servico"].lower()]

        if not resultados:
            await update.message.reply_text("❌ Nenhum prestador encontrado.")
        else:
            for p in resultados:
                msg = f"""
🔧 {p['servico'].upper()}

👤 Nome: {p['nome']}
📍 Cidade: {p['cidade']}
📞 Telefone: {p['telefone']}
"""
                await update.message.reply_text(msg)

        context.user_data["busca"] = False

    # CADASTRO
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

            await update.message.reply_text("✅ Cadastro realizado!")
        except:
            await update.message.reply_text("❌ Formato inválido.\nUse:\nNome - Serviço - Telefone - Cidade")

        context.user_data["cadastro"] = False

    # COMO USAR
    elif texto == "📖 Como Usar":
        await boas_vindas(update, context)

    # ADMIN
    elif texto == "👑 Admin":
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Acesso negado.")
            return

        if not prestadores:
            await update.message.reply_text("Nenhum prestador cadastrado.")
            return

        msg = "📋 Lista de Prestadores:\n\n"
        for p in prestadores:
            msg += f"{p['nome']} - {p['servico']} - {p['cidade']}\n"

        await update.message.reply_text(msg)

# RODAR
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", boas_vindas))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

print("Bot rodando...")
app.run_polling()
