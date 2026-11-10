from flask import Blueprint, jsonify, request
from database import conectar_banco

autores_bp = Blueprint("autores", __name__)

@autores_bp.route("/autores", methods=["GET"])
def listarautores():
    conexao = conectar_banco()
    autores = conexao.execute("SELECT * FROM autores").fetchall()
    conexao.close()
    return jsonify([dict(a) for a in autores])

@autores_bp.route("/autores", methods=["POST"])
def criarautor():
    dados = request.get_json()
    nome = dados.get("nome")
    nacionalidade = dados.get("nacionalidade")

    if not nome or not nacionalidade:
        return jsonify({"erro": "nome e nacionalidade são obrigatórios"}), 400

    conexao = conectar_banco()
    cursor = conexao.execute(
        "INSERT INTO autores (nome, nacionalidade) VALUES (?, ?)",
        (nome, nacionalidade)
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()

    return jsonify({"id": novo_id, "nome": nome, "nacionalidade": nacionalidade}), 201