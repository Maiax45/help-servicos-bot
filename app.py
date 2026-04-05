from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

from database import (
    criar_tabelas,
    cadastrar_prestador,
    buscar_prestadores,
    verificar_vencimentos,
    colocar_destaque,
    liberar_15_dias,
)

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = 8625636756  # COLOQUE SEU ID

# Estados do cadastro
NOME, TELEFONE, CIDADE, CATEGORIA, DESCRICAO = range(5)

# Menu principal
menu = ReplyKeyboardMarkup(
    [
        ["🔎 Procurar Prestador"],
        ["📝 Cadastrar Prestador"],
        ["💰 Planos"],
    ],
    resize_keyboard=True,
)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    verificar_vencimentos()

    await update.message.reply_text(
        "🏠 *HELP SERVIÇOS MAIAX*\n\n"
        "Conectamos você aos melhores prestadores da sua cidade.\n\n"
        "Escolha uma opção:",
        reply_markup=menu,
        parse_mode="Markdown",
    )

# ================= MENU =================
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if "Procurar" in texto:
        await update.message.reply_text("Digite a cidade:")
        context.user_data["busca"] = "cidade"

    elif "Cadastrar" in texto:
        await update.message.reply_text("Digite seu nome:")
        return NOME

    elif "Planos" in texto:
        await update.message.reply_text(
            "💰 *PLANOS HELP SERVIÇOS MAIAX*\n\n"
            "🆓 Grátis – 15 dias\n"
            "⭐ Destaque – R$ 19,99 / mês\n\n"
            "Para contratar o plano destaque, fale com o administrador.",
            parse_mode="Markdown",
        )

# ================= CADASTRO =================
async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nome"] = update.message.text
    await update.message.reply_text("Telefone:")
    return TELEFONE

async def telefone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefone"] = update.message.text
    await update.message.reply_text("Cidade:")
    return CIDADE

async def cidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cidade"] = update.message.text
    await update.message.reply_text("Categoria (ex: eletricista, diarista, pedreiro):")
    return CATEGORIA

async def categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["categoria"] = update.message.text
    await update.message.reply_text("Descrição do serviço:")
    return DESCRICAO

async def descricao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["descricao"] = update.message.text

    cadastrar_prestador(
        context.user_data["nome"],
        context.user_data["telefone"],
        context.user_data["cidade"],
        context.user_data["categoria"],
        context.user_data["descricao"],
    )

    await update.message.reply_text(
        "✅ Cadastro realizado com sucesso!\n"
        "Você recebeu 15 dias grátis.",
        reply_markup=menu,
    )

    return ConversationHandler.END

# ================= BUSCA =================
async def busca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("busca") == "cidade":
        context.user_data["cidade"] = update.message.text
        context.user_data["busca"] = "categoria"
        await update.message.reply_text("Digite a categoria:")
        return

    elif context.user_data.get("busca") == "categoria":
        cidade = context.user_data["cidade"]
        categoria = update.message.text

        resultados = buscar_prestadores(cidade, categoria)

        if not resultados:
            await update.message.reply_text("Nenhum prestador encontrado.")
            return

        texto = "📋 *PRESTADORES ENCONTRADOS*\n\n"

        for r in resultados:
            texto += (
                f"ID: {r[0]}\n"
                f"👤 {r[1]}\n"
                f"📞 {r[2]}\n"
                f"📝 {r[3]}\n"
                f"⭐ Plano: {r[4]} | {r[5]}\n\n"
            )

        await update.message.reply_text(texto, parse_mode="Markdown")

# ================= ADMIN =================
async def destacar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        id_prestador = int(context.args[0])
        colocar_destaque(id_prestador)
        await update.message.reply_text("⭐ Prestador colocado em destaque!")
    except:
        await update.message.reply_text("Use: /destacar ID")

async def liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        id_prestador = int(context.args[0])
        liberar_15_dias(id_prestador)
        await update.message.reply_text("⏳ +15 dias liberados!")
    except:
        await update.message.reply_text("Use: /liberar ID")

# ================= MAIN =================
def main():
    criar_tabelas()

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Cadastrar"), menu_handler)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome)],
            TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefone)],
            CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cidade)],
            CATEGORIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, categoria)],
            DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, descricao)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("destacar", destacar))
    app.add_handler(CommandHandler("liberar", liberar))

    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, busca))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
