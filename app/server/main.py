    
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session, joinedload

from typing import List
from app.server.db import SessionLocal, engine
from app.server.websocket_manage import manager, broadcast_message_time
# Cria as tabelas no banco caso elas não existam
import asyncio
from contextlib import asynccontextmanager
import random
import json

import app.server.utils as utils
import app.server.models as models
from app.server.service import userService
from app.server.schemas import UserSchema
from typing import List

models.Base.metadata.create_all(bind=engine)

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
  socket_id = f"user-{random.randint(1,(10*100))}"
  
  # estabelecer conexão com o websocket
  user = await manager.connect(
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
          try: 
            result_fib = await async_fibonacci(n)
            # await websocket.send_text("fibonacci(%d) = %d" % (n, result_fib))
            await manager.send_private_message("fibonacci(%d) = %d" % (n, result_fib), user.socket_id)
          except TypeError as e:
            await manager.send_private_message("Erro: {}".format(e), user.socket_id)
            # await websocket.send_text("Erro: {}".format(e))
      
  except WebSocketDisconnect:
    await manager.disconnect(socket_id)
  


class Tags:
  LOG_CONNECTION = "logs de conexão"

@app.get(
  "/users/", 
  response_model=List[UserSchema], 
  tags=[Tags.LOG_CONNECTION], 
  description="Retorna logs de quando cada usuário se conectou"
  )
async def list_all_logs():
  return await userService.find_users()

@app.get(
  "/users/connected", 
  response_model=List[UserSchema],
  description="Retorna logs de usuários com conexões ativa",
  tags=[Tags.LOG_CONNECTION], 
  )
async def list_user_connections():
  return await userService.find_users(True)

@app.get(
  "/users/disconnected", 
  response_model=List[UserSchema],
  tags=[Tags.LOG_CONNECTION], 
  description="Retorna logs de usuários com conexões ativa",
  )
async def list_user_connections():
  return await userService.find_users(False)

@app.patch(
  "/users/disconnect", 
  tags=[Tags.LOG_CONNECTION], 
  description="Desconecta usuário ativo",
  )
async def disconnect_user(username: str|None=None, socket_id: str|None = None):
  user: models.User|None = None
  try:
    if username:
      user =  await userService.disconnect_user(username=username)
    elif socket_id:
      user = await userService.disconnect_user(socket_id=socket_id)

    await manager.disconnect_user(user.socket_id)
    
    return {"message": f"usuário {user.username} deslogado"}
  except:
    return HTTPException(400, {"message": "usuário não encontrado"})