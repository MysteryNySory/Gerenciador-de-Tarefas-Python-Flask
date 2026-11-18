# Gerenciador de Tarefas com Python e Redis

Sistema de gerenciamento de tarefas desenvolvido em Python, utilizando Redis como banco de dados NoSQL e Flask para disponibilizar uma interface web integrada a uma API REST.

O projeto permite cadastrar, consultar, listar, atualizar e excluir tarefas, oferecendo duas formas de interação: uma interface gráfica acessível pelo navegador e uma interface de linha de comando (CLI).

O objetivo é demonstrar a integração entre Python e Redis, a implementação de operações CRUD, a organização de responsabilidades no backend e a comunicação entre uma aplicação web e um banco de dados NoSQL.

## 📌 Funcionalidades

### Gerenciamento de tarefas (CRUD)

- **Create:** cadastro de novas tarefas com título, descrição e status inicial.
- **Read:** consulta individual de tarefas pelo identificador.
- **List:** visualização de todas as tarefas cadastradas.
- **Update:** edição de título, descrição e status.
- **Delete:** exclusão de tarefas com confirmação da operação.

### Interface Web

- Cadastro de tarefas diretamente pelo navegador.
- Exibição das tarefas em cartões organizados.
- Identificação visual dos status.
- Filtros para visualizar tarefas por situação.
- Contadores de tarefas totais e por status.
- Edição por meio de janela modal.
- Exclusão com confirmação.
- Notificações de sucesso e erro.
- Atualização dinâmica dos dados utilizando JavaScript e Fetch API.

### Interface CLI

- Menu interativo pelo terminal.
- Cadastro e consulta de tarefas.
- Listagem organizada por identificador.
- Atualização individual de campos.
- Exclusão com confirmação.
- Validação de entradas e tratamento de erros.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal e implementação das regras de negócio. |
| Redis | Banco de dados NoSQL utilizado para armazenar as tarefas. |
| Flask | Framework responsável pela aplicação web e API REST. |
| HTML5 | Estrutura da interface web. |
| CSS3 | Estilização e organização visual. |
| JavaScript | Interações dinâmicas e comunicação com a API. |
| redis-py | Biblioteca Python para comunicação com o Redis. |

## 🏗️ Arquitetura do projeto

A aplicação utiliza uma estrutura compartilhada de acesso aos dados, permitindo que as interfaces Web e CLI trabalhem sobre o mesmo repositório de tarefas.

```text
                    USUÁRIO
                       |
              +--------+--------+
              |                 |
          INTERFACE WEB     INTERFACE CLI
              |                 |
            Flask             Python
              |                 |
          API REST          Menu interativo
              |                 |
              +--------+--------+
                       |
                TarefaRepository
                  crud_redis.py
                       |
                  redis-py
                       |
                     REDIS
                  Banco NoSQL
```

A classe `TarefaRepository`, implementada em `crud_redis.py`, centraliza as operações de acesso aos dados. Dessa forma, as duas interfaces compartilham a mesma lógica de persistência e validação.

## 📂 Estrutura do projeto

```text
atividadeREDISpy/
│
├── app.py
│
├── crud_redis.py
│
├── config_redis.py
│
├── atividadeREDISpy.pyproj
│
├── teste_conexao.py
│
├── requirements.txt
│
└── templates/
    └── index.html
```

### Responsabilidade dos arquivos

- `app.py`: inicializa o Flask, configura as rotas HTTP e disponibiliza os endpoints da API.
- `crud_redis.py`: implementa a classe `TarefaRepository`, as operações CRUD, validações e a interface de terminal.
- `config_redis.py`: centraliza a configuração da conexão com o Redis.
- `templates/index.html`: contém a interface web, os estilos CSS e os scripts JavaScript.
- `teste_conexao.py`: disponibiliza um teste auxiliar de conectividade com o Redis.
- `requirements.txt`: lista as bibliotecas necessárias para executar a aplicação.

## 🗄️ Armazenamento no Redis

O Redis é utilizado como banco de dados NoSQL, armazenando cada tarefa em uma estrutura do tipo **Hash**.

Cada registro utiliza uma chave no seguinte padrão:

```text
tarefa:{id}
```

Exemplo de representação:

```text
tarefa:1
    titulo       = Estudar Python
    descricao    = Revisar operações CRUD
    data_criacao = 17/11/2026 20:00:00
    status       = Em Progresso
```

O identificador é gerado automaticamente por meio de um contador armazenado na chave:

```text
contador:tarefa
```

### Principais comandos Redis utilizados

| Comando | Finalidade |
|---|---|
| `INCR` | Gera identificadores sequenciais. |
| `HSET` | Cria ou atualiza campos de uma tarefa. |
| `HGETALL` | Recupera os dados de uma tarefa. |
| `SCAN` | Percorre as chaves existentes. |
| `EXISTS` | Verifica se uma tarefa existe. |
| `DEL` | Remove uma tarefa. |

Os status permitidos são:

- `Pendente`
- `Em Progresso`
- `Concluída`

O sistema também realiza validações para impedir títulos vazios, campos inválidos e status não reconhecidos.

## 🚀 Como executar o projeto

### 1. Pré-requisitos

Antes de começar, instale:

- Python.
- Redis local ou uma instância Redis Cloud.
- Git.
- Um editor de código, como Visual Studio Code.

### 2. Clonar o repositório

Abra o terminal e execute:

```bash
git clone URL_DO_SEU_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd atividadeREDISpy
```

### 3. Criar um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual.

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

As dependências principais são:

```text
flask
redis
```

### 5. Configurar a conexão com o Redis

O projeto utiliza a variável de ambiente `REDIS_URL` para definir o endereço de conexão.

Para um Redis local, utilize:

```text
redis://localhost:6379/0
```

Para uma instância Redis Cloud, utilize o endereço fornecido pelo serviço:

```text
redis://default:SUA_SENHA@SEU_HOST:SUA_PORTA
```

Caso a instância utilize TLS, utilize `rediss://`.

**Windows (PowerShell):**

```powershell
$env:REDIS_URL="redis://localhost:6379/0"
```

**Linux / macOS:**

```bash
export REDIS_URL="redis://localhost:6379/0"
```

Certifique-se de que o arquivo `config_redis.py` esteja configurado para utilizar essa variável de ambiente.

**Importante:** nunca publique senhas, tokens ou credenciais de acesso ao Redis no GitHub. Utilize variáveis de ambiente e mantenha arquivos com informações sensíveis fora do controle de versão.

### 6. Executar a interface Web

Com o ambiente virtual ativado e o Redis configurado, execute:

```bash
python app.py
```

O Flask iniciará o servidor local e abrirá o navegador automaticamente.

Acesse:

```text
http://127.0.0.1:5000
```

A aplicação ficará disponível enquanto o processo do servidor estiver em execução.

### 7. Executar a interface CLI

Para utilizar o gerenciador diretamente pelo terminal:

```bash
python crud_redis.py
```

Será apresentado um menu com as opções de cadastro, consulta, listagem, atualização e exclusão de tarefas.

**Observação:** a conexão com o Redis precisa estar disponível para ambas as interfaces.

## 🔗 API REST

A interface web se comunica com o backend por meio de requisições HTTP, utilizando endpoints disponibilizados pelo Flask.

| Método HTTP | Endpoint | Descrição |
|---|---|---|
| GET | `/tarefas` | Lista todas as tarefas. |
| GET | `/tarefas/{id}` | Consulta uma tarefa específica. |
| POST | `/tarefas` | Cadastra uma nova tarefa. |
| PUT | `/tarefas/{id}` | Atualiza um campo da tarefa. |
| DELETE | `/tarefas/{id}` | Exclui uma tarefa. |

### Exemplo de requisição POST

```json
{
  "titulo": "Estudar Redis",
  "descricao": "Aprender estruturas de dados NoSQL",
  "status": "Pendente"
}
```

### Exemplo de resposta

```json
{
  "id": 1
}
```

A API também possui respostas de erro em formato JSON para situações como registros inexistentes, dados inválidos e indisponibilidade do Redis.

## 🧠 Conceitos aplicados

O desenvolvimento do projeto envolve conceitos importantes da área de Análise e Desenvolvimento de Sistemas:

- Operações CRUD e persistência de dados.
- Banco de dados NoSQL e estrutura Hash.
- Integração entre Python e Redis.
- Desenvolvimento de aplicações web com Flask.
- Construção e consumo de API REST.
- Métodos HTTP e comunicação cliente-servidor.
- Separação de responsabilidades no backend.
- Reutilização de código por meio de uma camada de repositório.
- Validação de dados e tratamento de exceções.
- Manipulação dinâmica do DOM com JavaScript.

## 📚 Objetivo educacional

Este projeto foi desenvolvido como atividade prática para explorar a utilização do Redis em aplicações Python, compreendendo como um banco de dados NoSQL pode ser integrado a diferentes interfaces e utilizado para manter informações persistentes.

A implementação também permite compreender a comunicação entre frontend, backend e banco de dados, além da importância de organizar o código para facilitar sua manutenção e reutilização.

## 🔮 Possíveis melhorias futuras

- Implementação de autenticação e gerenciamento de usuários.
- Separação das rotas em módulos utilizando Blueprints do Flask.
- Implementação de testes automatizados.
- Paginação e pesquisa de tarefas.
- Registro de datas de atualização.
- Utilização de Docker e Docker Compose.
- Implementação de logs estruturados.
- Melhorias na configuração e segurança da aplicação.
- Documentação interativa da API.

## 👨‍💻 Autor

**Arthur Pozzeti**

Estudante de Análise e Desenvolvimento de Sistemas, interessado em desenvolvimento de software, bancos de dados, integração de sistemas e tecnologias backend.

---

Desenvolvido com Python, Flask e Redis.
