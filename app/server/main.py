    
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session, joinedload

from typing import List
from app.server.db import SessionLocal, engine
import app.server.models as models
from time import sleep
import app.server.utils as utils
from app.server.websocket_manage import manager
# Cria as tabelas no banco caso elas não existam
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
import random
@app.websocket("/ws")
async def testa(websocket: WebSocket):
  username = websocket.query_params.get("username")
  socket_id = f"user-{random.randint(1,10*10)}"
  
  await manager.connect(
    socket_id=socket_id, 
    websocket=websocket, 
    username=username
    )
  
  await manager.disconnect(socket_id)

    
@app.get("/{id}")
def test(id: int):
  return {"test": utils.fibonacci(id)}