# Usa imagem base com Python 3.12.3
FROM python:3.12.3-slim

# Define diretório de trabalho
WORKDIR /desafio

# Copia arquivos do projeto
COPY requirements.txt Dockerfile docker-compose.yml .env /desafio
COPY app /desafio/app

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y netcat-openbsd net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /desafio/app

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]



