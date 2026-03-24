from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def executar_query(query, *args, fetch=False, commit=False):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    resultado = None

    try:
        cursor.execute(query, args)

        if commit:
            conn.commit()
        if fetch:
            resultado = cursor.fetchall()
    finally:
        conn.close()

    return resultado

# GET todos 
@app.route('/jogos', methods=['GET'])
def listar_jogos():
    jogos = executar_query("SELECT * FROM jogos", fetch=True)
    return jsonify([dict(j) for j in jogos]), 200

# GET por ID 
@app.route('/jogos/<int:id>', methods=['GET'])
def buscar_jogo(id):
    jogo = executar_query("SELECT * FROM jogos WHERE id = ?", id, fetch=True)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    return jsonify(dict(jogo[0])), 200

# POST 
@app.route('/jogos', methods=['POST'])
def criar_jogo():
    dados = request.get_json()

    executar_query(
        "INSERT INTO jogos (titulo, genero, plataforma, preco) VALUES (?, ?, ?, ?)",
        dados.get('titulo'),
        dados.get('genero'),
        dados.get('plataforma'),
        dados.get('preco'),
        commit=True
    )

    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201

# PUT 
@app.route('/jogos/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    dados = request.get_json()

    existe = executar_query("SELECT id FROM jogos WHERE id = ?", id, fetch=True)

    if not existe:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    executar_query(
        "UPDATE jogos SET titulo=?, genero=?, plataforma=?, preco=? WHERE id=?",
        dados.get('titulo'),
        dados.get('genero'),
        dados.get('plataforma'),
        dados.get('preco'),
        id,
        commit=True
    )

    return '', 204

# DELETE 
@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    existe = executar_query("SELECT id FROM jogos WHERE id = ?", id, fetch=True)

    if not existe:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    executar_query("DELETE FROM jogos WHERE id = ?", id, commit=True)

    return jsonify({"mensagem": "Jogo removido com sucesso!"}), 200

# rota inicial para testar se a API está funcionando
@app.route('/')
def home():
    return "API de Inventário de Jogos funcionando!"

if __name__ == '__main__':
    app.run(debug=True)