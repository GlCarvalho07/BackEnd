from flask import Flask, jsonify

from database import criar_tabelas
from routes.autores import autores_bp
from routes.livros import livros_bp


def criar_app():
    app = Flask(__name__)

    app.register_blueprint(autores_bp)
    app.register_blueprint(livros_bp)

    @app.route("/", methods=["GET"])
    def inicio():
        return jsonify({
            "Informações": "API Geral de Livros",
            "Versao": "2.0"
        })

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return jsonify({"erro": "Rota não encontrada"}), 404

    return app


criar_tabelas()
app = criar_app()

if __name__ == "__main__":
    print(app.url_map)  # lista todas as rotas registradas
    app.run(debug=True)