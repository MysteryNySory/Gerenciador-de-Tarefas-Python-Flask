"""
Sistema CRUD de tarefas em Python com Redis.

Cada tarefa é armazenada como um hash na chave 'tarefa:{id}' com os campos:
    titulo, descricao, data_criacao, status

O ID é gerado automaticamente com um contador no Redis ('contador:tarefa').
Interface: linha de comando (menu interativo).

Dependência:  pip install redis
"""

from datetime import datetime

import redis

from config_redis import REDIS_URL

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
# O endereço e a senha do Redis ficam em config_redis.py (REDIS_URL).

PREFIXO_CHAVE = "tarefa:"
CHAVE_CONTADOR = "contador:tarefa"

STATUS_VALIDOS = ("Pendente", "Em Progresso", "Concluída")
CAMPOS_EDITAVEIS = ("titulo", "descricao", "status")


# ---------------------------------------------------------------------------
# Camada de acesso a dados (backend)
# ---------------------------------------------------------------------------
class TarefaRepository:
    """Faz o CRUD de tarefas no Redis usando hashes."""

    def __init__(self, cliente):
        self.r = cliente

    @staticmethod
    def _chave(id_tarefa):
        return f"{PREFIXO_CHAVE}{id_tarefa}"

    def criar(self, titulo, descricao, status="Pendente"):
        """Cria uma tarefa nova (status inicial à escolha) e devolve o ID gerado."""
        titulo = titulo.strip()
        status = status.strip()
        if not titulo:
            raise ValueError("O título não pode ser vazio.")
        if status not in STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}.")

        id_tarefa = self.r.incr(CHAVE_CONTADOR)  # ID único e sequencial
        self.r.hset(
            self._chave(id_tarefa),
            mapping={
                "titulo": titulo,
                "descricao": descricao.strip(),
                "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "status": status,
            },
        )
        return id_tarefa

    def ler(self, id_tarefa):
        """Devolve um dicionário com a tarefa ou None se não existir."""
        dados = self.r.hgetall(self._chave(id_tarefa))
        if not dados:
            return None
        dados["id"] = id_tarefa
        return dados

    def listar(self):
        """Devolve a lista de todas as tarefas, ordenadas por ID."""
        tarefas = []
        for chave in self.r.scan_iter(match=f"{PREFIXO_CHAVE}*"):
            id_tarefa = int(chave.split(":", 1)[1])
            tarefa = self.ler(id_tarefa)
            if tarefa:
                tarefas.append(tarefa)
        return sorted(tarefas, key=lambda t: t["id"])

    def atualizar(self, id_tarefa, campo, novo_valor):
        """Atualiza um campo (titulo, descricao ou status) de uma tarefa."""
        if campo not in CAMPOS_EDITAVEIS:
            raise ValueError(
                f"Campo inválido. Use: {', '.join(CAMPOS_EDITAVEIS)}."
            )
        if not self.r.exists(self._chave(id_tarefa)):
            raise KeyError(f"Tarefa {id_tarefa} não encontrada.")

        novo_valor = novo_valor.strip()
        if campo == "titulo" and not novo_valor:
            raise ValueError("O título não pode ser vazio.")
        if campo == "status" and novo_valor not in STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}."
            )

        self.r.hset(self._chave(id_tarefa), campo, novo_valor)

    def deletar(self, id_tarefa):
        """Remove uma tarefa. Levanta KeyError se ela não existir."""
        if self.r.delete(self._chave(id_tarefa)) == 0:
            raise KeyError(f"Tarefa {id_tarefa} não encontrada.")


# ---------------------------------------------------------------------------
# Interface de linha de comando
# ---------------------------------------------------------------------------
def ler_id(mensagem="ID da tarefa: "):
    """Lê um ID inteiro positivo, repetindo até o usuário digitar certo."""
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("ID inválido. Digite um número inteiro positivo.")


def exibir_tarefa(t):
    print("-" * 40)
    print(f"ID:           {t['id']}")
    print(f"Título:       {t['titulo']}")
    print(f"Descrição:    {t['descricao']}")
    print(f"Criada em:    {t['data_criacao']}")
    print(f"Status:       {t['status']}")
    print("-" * 40)


def menu_criar(repo):
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    status = escolher_opcao("Status inicial:", [(s, s) for s in STATUS_VALIDOS])
    if status is None:
        print("Operação cancelada.")
        return
    id_tarefa = repo.criar(titulo, descricao, status)
    print(f"Tarefa criada com sucesso! ID: {id_tarefa}")


ROTULOS_CAMPOS = [("titulo", "Título"), ("descricao", "Descrição"), ("status", "Status")]


def escolher_opcao(titulo, opcoes):
    """Mostra uma lista numerada de (valor, rótulo) e devolve o valor escolhido (None = cancelar)."""
    print(f"\n{titulo}")
    for i, (_, rotulo) in enumerate(opcoes, start=1):
        print(f"  {i} - {rotulo}")
    print("  0 - Cancelar")
    while True:
        texto = input("Escolha: ").strip()
        if texto == "0":
            return None
        if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
            return opcoes[int(texto) - 1][0]
        print("Opção inválida. Digite um dos números da lista.")


def mostrar_resumo(repo):
    """Lista curta (ID - título [status]) para ajudar a escolher o ID. False se não há tarefas."""
    tarefas = repo.listar()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return False
    print("\nTarefas existentes:")
    for t in tarefas:
        print(f"  {t['id']} - {t['titulo']} [{t['status']}]")
    return True


def menu_ler(repo):
    if not mostrar_resumo(repo):
        return
    tarefa = repo.ler(ler_id())
    if tarefa:
        exibir_tarefa(tarefa)
    else:
        print("Tarefa não encontrada.")


def menu_listar(repo):
    tarefas = repo.listar()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for t in tarefas:
        exibir_tarefa(t)
    print(f"Total: {len(tarefas)} tarefa(s).")


def menu_atualizar(repo):
    if not mostrar_resumo(repo):
        return
    id_tarefa = ler_id()
    tarefa = repo.ler(id_tarefa)
    if not tarefa:
        print("Tarefa não encontrada.")
        return
    exibir_tarefa(tarefa)

    campo = escolher_opcao("Qual campo deseja alterar?", ROTULOS_CAMPOS)
    if campo is None:
        print("Operação cancelada.")
        return
    if campo == "status":
        novo_valor = escolher_opcao("Novo status:", [(s, s) for s in STATUS_VALIDOS])
        if novo_valor is None:
            print("Operação cancelada.")
            return
    else:
        novo_valor = input(f"Novo valor (atual: {tarefa[campo]}): ")
    repo.atualizar(id_tarefa, campo, novo_valor)
    print("Tarefa atualizada com sucesso!")


def menu_deletar(repo):
    if not mostrar_resumo(repo):
        return
    id_tarefa = ler_id()
    confirma = input(f"Excluir a tarefa {id_tarefa}? (s/n): ").strip().lower()
    if confirma == "s":
        repo.deletar(id_tarefa)
        print("Tarefa excluída com sucesso!")
    else:
        print("Operação cancelada.")


ACOES = {
    "1": menu_criar,
    "2": menu_ler,
    "3": menu_listar,
    "4": menu_atualizar,
    "5": menu_deletar,
}


def exibir_menu():
    print("\n===== GERENCIADOR DE TAREFAS (Redis) =====")
    print("1 - Criar tarefa")
    print("2 - Ler tarefa")
    print("3 - Listar todas as tarefas")
    print("4 - Atualizar tarefa")
    print("5 - Deletar tarefa")
    print("0 - Sair")


def criar_cliente():
    """Cria o cliente Redis (a conexão só acontece no primeiro comando)."""
    return redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,  # devolve str em vez de bytes
        protocol=2,             # RESP2: o RESP3 padrão demorou ~16s para responder
        socket_connect_timeout=8,
        socket_timeout=15,      # nunca fica preso esperando para sempre
    )


def conectar():
    """Cria o cliente e testa a conexão (usado pela linha de comando)."""
    cliente = criar_cliente()
    cliente.ping()
    return cliente


def main():
    print("Conectando ao Redis...")
    try:
        repo = TarefaRepository(conectar())
    except redis.exceptions.RedisError as erro:
        print("Não foi possível conectar ao Redis.")
        print(f"Detalhe: {erro}")
        print("Confira o endereço, a porta e a senha em config_redis.py e se o servidor está no ar.")
        input("\nPressione Enter para sair...")
        return
    print("Conectado!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Encerrando...")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        try:
            acao(repo)
        except (ValueError, KeyError) as erro:
            print(f"Erro: {erro.args[0]}")
        except redis.exceptions.RedisError as erro:
            print(f"Erro de comunicação com o Redis: {erro}")


if __name__ == "__main__":
    main()
