from flask import Blueprint, jsonify, request
from database import conectar_banco

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/livros", methods=["GET"])  # listar livros
def listar_livros():
    conexao = conectar_banco()

    livros = conexao.execute(
        """
        SELECT livros.id, livros.titulo, livros.ano, livros.autorid,
               autores.nome AS autor,
               autores.nacionalidade
        FROM livros
        JOIN autores
          ON livros.autorid = autores.id
        ORDER BY livros.id
        """
    ).fetchall()

    conexao.close()

    resultado = []

    for livro in livros:
        resultado.append({
            "id": livro["id"],
            "titulo": livro["titulo"],
            "ano": livro["ano"],
            "autorid": livro["autorid"],
            "autor": livro["autor"],
            "nacionalidade": livro["nacionalidade"]
        })

    return jsonify(resultado)


@livros_bp.route("/livros", methods=["POST"])  # cadastrar livro
def criar_livro():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie um JSON no corpo da requisição"}), 400

    titulo = dados.get("titulo")
    ano = dados.get("ano")
    autorid = dados.get("autorid")

    if not titulo or not ano or not autorid:
        return jsonify({"erro": "Campos obrigatórios: titulo, ano, autorid"}), 400

    conexao = conectar_banco()

    # confere se o autor existe antes de cadastrar o livro
    autor = conexao.execute(
        "SELECT id FROM autores WHERE id = ?", (autorid,)
    ).fetchone()

    if autor is None:
        conexao.close()
        return jsonify({"erro": "Autor não encontrado"}), 404

    cursor = conexao.execute(
        "INSERT INTO livros (titulo, ano, autorid) VALUES (?, ?, ?)",
        (titulo, ano, autorid)
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()

    return jsonify({
        "mensagem": "Livro cadastrado com sucesso",
        "id": novo_id
    }), 201