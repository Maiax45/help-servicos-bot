from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import criar_tabela, adicionar_prestador, listar_por_servico, listar_prestadores, excluir_prestador

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = "8625636756"  # Coloque seu ID do Telegram

criar_tabela()

def menu():
    return ReplyKeyboardMarkup([
        ["🔎 Buscar Serviço"],
        ["📝 Cadastrar Prestador"],
        ["👑 Painel Admin"]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bem-vindo à Help Serviços Maiax!\n\nEscolha uma opção:",
        reply_markup=menu()
    )

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    # BUSCAR SERVIÇO
    if texto == "🔎 Buscar Serviço":
        await update.message.reply_text("Digite o serviço que você procura:")
        context.user_data["busca"] = True

    elif context.user_data.get("busca"):
        resultados = listar_por_servico(texto)

        if not resultados:
            await update.message.reply_text("❌ Nenhum prestador encontrado.")
            context.user_data["busca"] = False
            return

        for p in resultados:
            msg = f"""
🔧 {p[1].upper()}

👤 Nome: {p[0]}
📍 Cidade: {p[3]}
📞 Telefone: {p[2]}

⭐ Profissional verificado
"""
            await update.message.reply_text(msg)

        context.user_data["busca"] = False

    # CADASTRAR PRESTADOR
    elif texto == "📝 Cadastrar Prestador":
        await update.message.reply_text(
            "Envie no formato:\n\nNome - Serviço - Telefone - Cidade\n\n"
            "Exemplo:\nJoão - Eletricista - 38999999999 - Montes Claros"
        )
        context.user_data["cadastro"] = True

    elif context.user_data.get("cadastro"):
        try:
            nome, servico, telefone, cidade = texto.split(" - ")
            adicionar_prestador(nome, servico, telefone, cidade)
            await update.message.reply_text("✅ Cadastro realizado!")
            context.user_data["cadastro"] = False
        except:
            await update.message.reply_text("❌ Formato inválido.")

    # PAINEL ADMIN
    elif texto == "👑 Painel Admin":
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Você não é admin.")
            return

        prestadores = listar_prestadores()

        if not prestadores:
            await update.message.reply_text("Nenhum prestador cadastrado.")
            return

        msg = "📋 Prestadores cadastrados:\n\n"
        for p in prestadores:
            msg += f"{p[0]} - {p[1]}\n"

        msg += "\nDigite o NOME para excluir."

        await update.message.reply_text(msg)
        context.user_data["excluir"] = True

    elif context.user_data.get("excluir"):
        if user_id == ADMIN_ID:
            excluir_prestador(texto)
            await update.message.reply_text("🗑️ Prestador excluído.")
            context.user_data["excluir"] = False

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

print("Bot rodando...")
app.run_polling()

