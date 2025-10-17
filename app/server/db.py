from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.server.config import DATABASE_URI

# DATABASE_URI = "postgresql://root:root@localhost:5432/desafio"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine) # conexão entre o banco é o código

Base = declarative_base()