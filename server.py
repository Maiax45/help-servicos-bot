from flask import Flask, render_template, request, redirect
from database import listar_prestadores, excluir_prestador, criar_tabela

app = Flask(__name__, template_folder="modelos")

criar_tabela()

@app.route("/")
def admin():
    prestadores = listar_prestadores()
    return render_template("admin.html", prestadores=prestadores)

@app.route("/excluir", methods=["POST"])
def excluir():
    nome = request.form["nome"]
    excluir_prestador(nome)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
