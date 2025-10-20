# Desafio
Você deve desenvolver um sistema que ofereça uma conexão via WebSocket para clientes, com funcionalidades específicas de envio de dados, processamento de algoritmos e gestão de clientes conectados.

##  do desafio
1. Conexão via WebSocket
Desenvolver um client WebSocket para testar a conexão com o servidor.
Desenvolver um servidor WebSocket que permita a conexão de múltiplos clientes.
2. Envio de Data Atual
Implementar uma rotina no servidor para enviar a data e hora atuais a cada segundo para todos os clientes conectados.
3. Gestão de Usuários Conectados
Salvar em um banco de dados todos os usuários atualmente conectados ao sistema.
Atualizar o banco de dados sempre que um cliente se conectar ou desconectar.
4. Processamento de Comandos
Desenvolver no sistema a capacidade de receber comandos via WebSocket para processar algoritmos de Fibonacci.
O cliente enviará um valor 'n' na mensagem, e o resultado do cálculo de Fibonacci(n) deverá ser enviado apenas ao cliente que fez a solicitação.
5. Ambiente de Desenvolvimento
Docker:
Utilizar Docker para criar o ambiente de desenvolvimento e execução do sistema.
Criar um Dockerfile para o sistema.
Utilizar Docker Compose (opcional) para orquestrar múltiplos serviços (ex: aplicação e banco de dados).
6. Tecnologias Recomendadas
Linguagem: Python.
Programação Assíncrona: Utilizar frameworks e bibliotecas que suportem operações assíncronas.
Banco de Dados: Qualquer sistema de banco de dados relacional ou não relacional (ex: PostgreSQL, SQL Server, MongoDB, Redis).

## 📋 Pré-requisitos
tenha em sua máquina os seguintes sistemas:

- [Python](https://www.python.org/) 
- [PostgrSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

## Start
1. Certifique-se de estar no diretório raiz do projeto (desafio-bsa-jr) e execute os comandos abaixo para construir e iniciar os containers app (FastAPI) e db (PostgreSQL):
```bash
# Acesse o diretório do projeto
$ cd desafio-bsa-jr

# Construa os containers
$ docker compose --build  

# Inicie os containers em segundo plano
$ docker compose up -d          
```
2. Ainda no diretório do projeto, crie um ambiente virtual para rodar o cliente localmente e instalar as dependências:
```bash
# Criar venv windows
$ python -m venv venv
$ venv/scripts/activate

# Linux/MacOs
$ python3 -m venv venv
$ source venv/bin/activate

# Baixar dependências
$ pip install requirements.txt 
```
3. execute o programa `app/client/main.py` ainda no diretorio `desafio`
```bash
$ python app/client/main.py nome_do_usuario 
```
4. Durante a execução, os valores digitados podem desaparecer momentaneamente do terminal conforme as mensagens de broadcast são exibidas. Não se preocupe, tudo que você digitar será armazenado em cache e enviado corretamente ao servidor ao pressionar Enter

<div align="center">
  <video src="/video.mp4" controls width="600">
    Seu navegador não suporta o vídeo.
  </video>
</div>

## Features

- Conexão WebSocket
  - Servidor WebSocket assíncrono (arquivo/endpoint: defina o caminho do servidor).
  - Cliente de teste fornecido (script para conectar e enviar/receber mensagens).

- Envio de data/hora
  - O servidor transmite a data e hora atuais para todos os clientes conectados a cada segundo.

- Gestão de usuários conectados
  - Usuários conectados são persistidos em banco de dados.
  - O registro é atualizado automaticamente em conexões e desconexões.

- Processamento de comandos (Fibonacci)
  - Recebe via WebSocket um valor n e processa Fibonacci(n).
  - Resultado é enviado apenas ao cliente solicitante.

- Ambiente com Docker
  - Dockerfile incluído para construir a imagem da aplicação.
  - docker-compose para configuração total do ambiente.

- Tecnologias
  - Linguagem: Python.
  - Biblioteca/stack assíncrona utilizada: FastAPI, websockets, asyncio.
  - Banco de dados: PostgreSQL.


