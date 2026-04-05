from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import datetime

TOKEN = "8625636756:AAHRL7_-JLbf5jPSknlkR2gSB6QblvKiBhw"

# ================= BANCO =================
def conectar():
    conn = sqlite3.connect("banco.db")
    return conn

def criar_banco():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        servico TEXT,
        cidade TEXT,
        telefone TEXT,
        vencimento TEXT,
        destaque INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

# ================= COMANDOS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo ao Help Serviços Maiax\n\n"
        "Digite:\n"
        "Cadastrar Prestador\n"
        "Procurar Prestador"
    )

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    if texto == "Cadastrar Prestador":
        await update.message.reply_text("Digite:\nNome - Serviço - Cidade - Telefone")

    elif "-" in texto:
        dados = texto.split("-")
        nome = dados[0].strip()
        servico = dados[1].strip()
        cidade = dados[2].strip()
        telefone = dados[3].strip()

        vencimento = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime("%Y-%m-%d")

        conn = conectar()
        c = conn.cursor()
        c.execute("INSERT INTO prestadores (nome, servico, cidade, telefone, vencimento) VALUES (?,?,?,?,?)",
                  (nome, servico, cidade, telefone, vencimento))
        conn.commit()
        conn.close()

        await update.message.reply_text("Prestador cadastrado com 15 dias grátis!")

    elif texto == "Procurar Prestador":
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT nome, servico, cidade, telefone FROM prestadores WHERE destaque = 1")
        dados = c.fetchall()
        conn.close()

        if dados:
            resposta = "Prestadores em destaque:\n\n"
            for d in dados:
                resposta += f"Nome: {d[0]}\nServiço: {d[1]}\nCidade: {d[2]}\nTelefone: {d[3]}\n\n"
        else:
            resposta = "Nenhum prestador em destaque."

        await update.message.reply_text(resposta)

# ================= ADMIN =================
async def destacar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_prestador = context.args[0]

    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE prestadores SET destaque = 1 WHERE id = ?", (id_prestador,))
    conn.commit()
    conn.close()

    await update.message.reply_text("Prestador colocado em destaque!")

async def liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_prestador = context.args[0]
    nova_data = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE prestadores SET vencimento = ? WHERE id = ?", (nova_data, id_prestador))
    conn.commit()
    conn.close()

    await update.message.reply_text("Plano renovado por 30 dias!")

# ================= MAIN =================
def main():
    criar_banco()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("destacar", destacar))
    app.add_handler(CommandHandler("liberar", liberar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))

    print("Bot rodando...")
    app.run_polling()
