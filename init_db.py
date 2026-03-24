import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    genero TEXT NOT NULL,
    plataforma TEXT NOT NULL,
    preco REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")