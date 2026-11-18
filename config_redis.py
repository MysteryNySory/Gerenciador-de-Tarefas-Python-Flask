"""
Configuração da conexão com o Redis (usada pela versão em linha de comando e pela web).

Formato:  redis://default:SENHA@HOST:PORTA        (com TLS: rediss://...)
Se a senha tiver caracteres especiais, troque: @ por %40, : por %3A, / por %2F, # por %23.

ATENÇÃO: não publique este arquivo (GitHub, entrega pública) com a senha preenchida.
"""

import os

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://default:COLE_A_SENHA_AQUI@song-fold-lace-22620.db.redis.io:15309",
)
