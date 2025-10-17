from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USER = str(os.getenv("DATABASE_USER", "root"))
DATABASE_PASSWORD = str(os.getenv("DATABASE_PASSWORD", "root"))
DATABASE_HOST = str(os.getenv("DATABASE_HOST", "localhost"))
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
DATABASE_DB = str(os.getenv("DATABASE_DB", "desafio"))

# Conexão ao banco como administrador (root)
DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

# "postgresql://root:root@localhost:5432/desafio"