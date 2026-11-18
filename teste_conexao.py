"""
Teste de conexão com o Redis, passo a passo.
Rode no cmd (fora do Visual Studio):   python teste_conexao.py
Não trava: cada passo tem limite de tempo e mostra onde falhou.
A senha é pedida na hora (não aparece na tela e não fica no arquivo).
"""
import getpass
import socket
import sys
import time

import redis

HOST = "song-fold-lace-22620.db.redis.io"
PORT = 15309
USUARIO = "default"
LIMITE = 8  # segundos

print(f"Python:   {sys.version.split()[0]}")
print(f"redis-py: {redis.__version__}")
print(f"Destino:  {HOST}:{PORT}\n")

senha = getpass.getpass("Senha do Redis (não aparece ao digitar): ")

# Passo 1: DNS
print("\n[1] Resolvendo o endereço...")
try:
    print("    OK ->", socket.gethostbyname(HOST))
except OSError as e:
    print("    FALHOU:", e)
    sys.exit(1)

# Passo 2: conexão TCP simples
print("[2] Abrindo conexão TCP...")
try:
    t0 = time.time()
    socket.create_connection((HOST, PORT), timeout=LIMITE).close()
    print(f"    OK ({time.time() - t0:.2f}s)")
except OSError as e:
    print("    FALHOU:", e)
    print("    -> Algo bloqueia o Python nessa porta (firewall/antivírus/rede).")
    sys.exit(1)

# Passo 3: PING pelo redis-py, nos dois protocolos
for protocolo in (2, 3):
    print(f"[3] PING com redis-py (protocolo RESP{protocolo})...")
    try:
        cliente = redis.Redis(
            host=HOST, port=PORT, username=USUARIO, password=senha,
            protocol=protocolo, decode_responses=True,
            socket_connect_timeout=LIMITE, socket_timeout=LIMITE,
        )
        t0 = time.time()
        resposta = cliente.ping()
        print(f"    OK -> {resposta} ({time.time() - t0:.2f}s)")
    except Exception as e:
        print(f"    FALHOU: {type(e).__name__}: {e}")

print("\nFim do teste.")