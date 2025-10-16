# Desafio
Você deve desenvolver um sistema que ofereça uma conexão via WebSocket para clientes, com funcionalidades específicas de envio de dados, processamento de algoritmos e gestão de clientes conectados.

## Requisitos
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

