from flask import Flask, render_template, request, redirect
import sqlite3
from collections import defaultdict

app = Flask(__name__)

# ---------- BANCO ----------
def get_db():
    conn = sqlite3.connect("financeiro.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            tipo TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

# ---------- ROTAS ----------
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cursor = conn.cursor()

    # adicionar
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO lancamentos (descricao, valor, tipo, data) VALUES (?, ?, ?, ?)",
            (
                request.form["descricao"],
                float(request.form["valor"]),
                request.form["tipo"],
                request.form["data"]
            )
        )
        conn.commit()
        return redirect("/")

    mes = request.args.get("mes")

    if mes:
        cursor.execute(
            "SELECT * FROM lancamentos WHERE substr(data,1,7)=? ORDER BY data",
            (mes,)
        )
    else:
        cursor.execute("SELECT * FROM lancamentos ORDER BY data")

    lancamentos = cursor.fetchall()

    # totais
    total_ganhos = sum(l["valor"] for l in lancamentos if l["tipo"] == "ganho")
    total_despesas = sum(l["valor"] for l in lancamentos if l["tipo"] == "gasto")
    total_reservas = sum(l["valor"] for l in lancamentos if l["tipo"] == "reserva")
    saldo = total_ganhos - total_despesas

    # ---------- DADOS DO GRÁFICO ----------
    grafico = defaultdict(lambda: {"ganho": 0, "gasto": 0, "reserva": 0})

    for l in lancamentos:
        mes_label = l["data"][:7]  # YYYY-MM
        grafico[mes_label][l["tipo"]] += l["valor"]

    labels = list(grafico.keys())
    ganhos = [grafico[m]["ganho"] for m in labels]
    gastos = [grafico[m]["gasto"] for m in labels]
    reservas = [grafico[m]["reserva"] for m in labels]

    conn.close()

    return render_template(
        "index.html",
        lancamentos=lancamentos,
        total_ganhos=total_ganhos,
        total_despesas=total_despesas,
        total_reservas=total_reservas,
        saldo=saldo,
        mes=mes,
        labels=labels,
        ganhos=ganhos,
        gastos=gastos,
        reservas=reservas
    )

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lancamentos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
