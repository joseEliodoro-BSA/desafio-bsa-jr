from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.server.config import DATABASE_URI
from contextlib import contextmanager
from typing import Iterator
# DATABASE_URI = "postgresql://root:root@localhost:5432/desafio"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine) # conexão entre o banco é o código

Base = declarative_base()

@contextmanager
def get_db() -> Iterator[Session]:
  """Função de conexão com o banco de dados"""
  db = SessionLocal()
  try: 
    yield db
  finally:
    db.close()
