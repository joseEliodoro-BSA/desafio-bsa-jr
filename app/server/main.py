    
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session, joinedload

from typing import List
from app.server.db import SessionLocal, engine
import app.server.models as models
import app.server.utils as utils
from app.server.websocket_manage import manager, broadcast_message_time
# Cria as tabelas no banco caso elas não existam
models.Base.metadata.create_all(bind=engine)
import asyncio
from contextlib import asynccontextmanager
import random
import json


broadcast_task = None

# função executada no inicio do ciclo de vida da aplicação e no final
@asynccontextmanager
async def lifespan(app: FastAPI):
  
  global broadcast_task

  # antes do app iniciar
  broadcast_task = asyncio.create_task(broadcast_message_time())

  yield 
  broadcast_task.cancel()
  manager.disconnect_all()

# iniciando aplicação
app = FastAPI(lifespan=lifespan)

async def async_fibonacci(n: int) -> int:
  """Rodar a função fibonacci de forma assíncrona"""
  loop = asyncio.get_event_loop()
  return await loop.run_in_executor(None, utils.fibonacci, n)

@app.websocket("/ws")
async def testa(websocket: WebSocket):
  username = websocket.query_params.get("username")
  socket_id = f"user-{random.randint(1,10*10)}"
  
  # estabelecer conexão com o websocket
  await manager.connect(
    socket_id=socket_id, 
    websocket=websocket, 
    username=username
  )

  try:
    while True:
      data: dict = await websocket.receive_text()
      data = json.loads(data)
      if(data.get('cmd') == 'fib'):
        n = data.get('n')
        if n:
          result_fib = await async_fibonacci(n)
          await websocket.send_text("fibonacci(%d) = %d" % (n, result_fib))
      
      
  except WebSocketDisconnect:
    await manager.disconnect(socket_id)
  

    
@app.get("/{id}")
def test(id: int):
  return {"test": utils.fibonacci(id)}