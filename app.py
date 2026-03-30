from flask import Flask, jsonify, request

# ALTERAÇÃO: import do SQLAlchemy (ORM)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ALTERAÇÃO: configuração do banco de dados via SQLAlchemy
# antes: conexão manual com sqlite3
# agora: string de conexão centralizada
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ALTERAÇÃO: criação do objeto db (responsável pelo ORM)
db = SQLAlchemy(app)

# ALTERAÇÃO: criação do modelo da tabela (substitui SQL manual)
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# ALTERAÇÃO: criação automática do banco
# antes: script separado (init_db.py)
with app.app_context():
    db.create_all()

# GET - listar jogos
@app.route('/jogos', methods=['GET'])
def listar_jogos():
    # ALTERAÇÃO: uso do ORM ao invés de SELECT SQL
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

# GET por ID
@app.route('/jogos/<int:id>', methods=['GET'])
def buscar_jogo(id):
    # ALTERAÇÃO: substitui SELECT WHERE
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

    # ALTERAÇÃO: criação de objeto ao invés de INSERT SQL
    novo = Jogo(
        titulo=dados['titulo'],
        genero=dados['genero'],
        plataforma=dados['plataforma'],
        preco=dados['preco']
    )

    # ALTERAÇÃO: uso de session do SQLAlchemy
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

    # ALTERAÇÃO: atualização via atributos do objeto
    jogo.titulo = dados['titulo']
    jogo.genero = dados['genero']
    jogo.plataforma = dados['plataforma']
    jogo.preco = dados['preco']

    db.session.commit()

    return jsonify({"mensagem": "Atualizado com sucesso!"})

# DELETE - remover
@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    jogo = Jogo.query.get(id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    # ALTERAÇÃO: delete via ORM (sem SQL)
    db.session.delete(jogo)
    db.session.commit()

    return jsonify({"mensagem": "Jogo removido com sucesso!"})

# Rota inicial
@app.route('/')
def index():
    return jsonify({"mensagem": "API de Jogos online!"})

if __name__ == '__main__':
    app.run(debug=True)