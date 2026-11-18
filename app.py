"""
Interface web (Flask) do sistema de tarefas.
Usa a MESMA camada de dados (TarefaRepository) da versão em linha de comando,
então a regra de negócio e as validações ficam em um lugar só (crud_redis.py).

Dependências:  pip install flask redis
"""

import os
import threading
import webbrowser

import redis
from flask import Flask, jsonify, request, send_file

from crud_redis import CAMPOS_EDITAVEIS, TarefaRepository, criar_cliente

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
repo = TarefaRepository(criar_cliente())


def erro(mensagem, codigo):
    return jsonify({"erro": mensagem}), codigo


@app.errorhandler(redis.exceptions.RedisError)
def redis_indisponivel(e):
    return erro(f"Erro ao acessar o Redis: {e}", 503)


@app.route("/")
def index():
    """Entrega a página HTML (em 'templates/' ou ao lado do app.py)."""
    candidatos = [os.path.join(BASE_DIR, "templates", "index.html"),
                  os.path.join(BASE_DIR, "index.html")]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return send_file(caminho)
    return (f"index.html não encontrado. Procurei em:\n" + "\n".join(candidatos), 500,
            {"Content-Type": "text/plain; charset=utf-8"})


@app.route("/tarefas", methods=["GET"])
def listar():
    return jsonify(repo.listar())


@app.route("/tarefas/<int:id_tarefa>", methods=["GET"])
def ler(id_tarefa):
    tarefa = repo.ler(id_tarefa)
    return jsonify(tarefa) if tarefa else erro("Tarefa não encontrada.", 404)


@app.route("/tarefas", methods=["POST"])
def criar():
    d = request.get_json(silent=True) or {}
    try:
        novo_id = repo.criar(str(d.get("titulo") or ""), str(d.get("descricao") or ""),
                             str(d.get("status") or "Pendente"))
    except ValueError as e:
        return erro(e.args[0], 400)
    return jsonify({"id": novo_id}), 201


@app.route("/tarefas/<int:id_tarefa>", methods=["PUT"])
def atualizar(id_tarefa):
    d = request.get_json(silent=True) or {}
    try:
        repo.atualizar(id_tarefa, d.get("campo"), str(d.get("valor") or ""))
    except KeyError as e:
        return erro(e.args[0], 404)
    except ValueError as e:
        return erro(e.args[0], 400)
    return jsonify({"ok": True})


@app.route("/tarefas/<int:id_tarefa>", methods=["DELETE"])
def deletar(id_tarefa):
    try:
        repo.deletar(id_tarefa)
    except KeyError as e:
        return erro(e.args[0], 404)
    return jsonify({"ok": True})


if __name__ == "__main__":
    # Abre o navegador sozinho (você usa a página; o terminal só fica rodando o servidor).
    threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False)
