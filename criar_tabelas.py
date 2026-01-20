import sqlite3

conn = sqlite3.connect("financeiro.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ganhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    valor REAL,
    data TEXT,
    categoria TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    valor REAL,
    data TEXT,
    categoria TEXT
)
""")

conn.commit()
conn.close()

print("Tabelas criadas com sucesso!")
