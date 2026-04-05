from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from database import (
    criar_tabela,
    adicionar_prestador,
    listar_por_servico,
    listar_todos,
    prestadores_vencendo,
    ativar_pagamento,
    excluir_prestador,
    tornar_destaque
)

TOKEN = "8625636756:AAHjtVORS0uNTX8q1VaFj3fRSjdzyrDW6TM"
ADMIN_ID = "8625636756"  # PEGAR NO @userinfobot

criar_tabela()

def menu(user_id):
    if user_id == ADMIN_ID:
        return ReplyKeyboardMarkup([
            ["🔎 Buscar Serviço"],
            ["📝 Cadastrar Prestador"],
            ["📖 Como Funciona"],
            ["👑 Admin"]
        ], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([
            ["🔎 Buscar Serviço"],
            ["📝 Cadastrar Prestador"],
            ["📖 Como Funciona"]
        ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(
        "🚀 Bem-vindo à Help Serviços Maiax!",
        reply_markup=menu(user_id)
    )

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    # COMO FUNCIONA
    if texto == "📖 Como Funciona":
        msg = """
👥 CLIENTE:
1. Clique em Buscar Serviço
2. Digite a profissão
3. Escolha o profissional
4. Entre em contato

👨‍🔧 PRESTADOR:
1. Clique em Cadastrar Prestador
2. Envie seus dados
3. Ganhe 15 dias grátis
4. Após isso, precisa renovar mensalmente
"""
        await update.message.reply_text(msg)

    # BUSCA
    elif texto == "🔎 Buscar Serviço":
        await update.message.reply_text("Digite o serviço:")
        context.user_data["busca"] = True

    elif context.user_data.get("busca"):
        resultados = listar_por_servico(texto)

        if not resultados:
            await update.message.reply_text("Nenhum prestador encontrado.")
            context.user_data["busca"] = False
            return

        for p in resultados:
            estrela = "⭐ DESTAQUE\n" if p[4] == 1 else ""
            msg = f"""
{estrela}🔧 {p[1].upper()}

👤 Nome: {p[0]}
📍 Cidade: {p[3]}
📞 Telefone: {p[2]}
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
            adicionar_prestador(nome, servico, telefone, cidade)

            await update.message.reply_text("Cadastro realizado! Você ganhou 15 dias grátis.")
            context.user_data["cadastro"] = False
        except:
            await update.message.reply_text("Formato inválido.")

    # ADMIN
    elif texto == "👑 Admin":
        if user_id != ADMIN_ID:
            return

        lista = listar_todos()
        vencendo = prestadores_vencendo()

        msg = "📋 Prestadores:\n\n"
        for p in lista:
            msg += f"{p[0]} - {p[1]} - {p[2]}\n"

        if vencendo:
            msg += "\n⚠️ Vencendo em breve:\n"
            for v in vencendo:
                msg += f"{v[0]} - {v[1]}\n"

        msg += "\nComandos:\n"
        msg += "Ativar: nome\n"
        msg += "Excluir: nome\n"
        msg += "Destaque: nome\n"

        await update.message.reply_text(msg)
        context.user_data["admin"] = True

    elif context.user_data.get("admin"):
        if user_id != ADMIN_ID:
            return

        if texto.startswith("Ativar"):
            nome = texto.replace("Ativar ", "")
            ativar_pagamento(nome)
            await update.message.reply_text("Pagamento ativado por 30 dias.")

        elif texto.startswith("Excluir"):
            nome = texto.replace("Excluir ", "")
            excluir_prestador(nome)
            await update.message.reply_text("Prestador excluído.")

        elif texto.startswith("Destaque"):
            nome = texto.replace("Destaque ", "")
            tornar_destaque(nome)
            await update.message.reply_text("Prestador colocado em destaque.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

print("Bot rodando...")
app.run_polling()
