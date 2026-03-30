from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ALTERAÇÃO: configurando o banco via SQLAlchemy (não usamos mais sqlite3 direto)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ALTERAÇÃO: modelo da tabela usando ORM
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# ALTERAÇÃO: criação automática do banco (substitui init_db.py)
with app.app_context():
    db.create_all()

# GET - listar todos
@app.route('/jogos', methods=['GET'])
def listar_jogos():
    jogos = Jogo.query.all()
    return jsonify([
        {
            "id": j.id,
            "titulo": j.titulo,
            "genero": j.genero,
            "plataforma": j.plataforma,
            "preco": j.preco
        } for j in jogos
    ])

# GET - buscar por id
@app.route('/jogos/<int:id>', methods=['GET'])
def buscar_jogo(id):
    jogo = Jogo.query.get(id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    return jsonify({
        "id": jogo.id,
        "titulo": jogo.titulo,
        "genero": jogo.genero,
        "plataforma": jogo.plataforma,
        "preco": jogo.preco
    })

# POST - inserir
@app.route('/jogos', methods=['POST'])
def inserir_jogo():
    dados = request.get_json()

    novo = Jogo(
        titulo=dados['titulo'],
        genero=dados['genero'],
        plataforma=dados['plataforma'],
        preco=dados['preco']
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201

# PUT - atualizar
@app.route('/jogos/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    jogo = Jogo.query.get(id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    dados = request.get_json()

    jogo.titulo = dados['titulo']
    jogo.genero = dados['genero']
    jogo.plataforma = dados['plataforma']
    jogo.preco = dados['preco']

    db.session.commit()

    return '', 204

# DELETE - remover
@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    jogo = Jogo.query.get(id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    db.session.delete(jogo)
    db.session.commit()

    return jsonify({"mensagem": "Jogo removido com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)