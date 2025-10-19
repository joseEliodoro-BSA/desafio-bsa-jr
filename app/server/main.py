    
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException

import asyncio
from contextlib import asynccontextmanager
import random
import json
from uuid import uuid4
from app.server.websocket_manage import manager, broadcast_message_time
from app.server.router_user_manage import router
import app.server.models as models
from app.server.db import engine
import app.server.utils as utils

# Cria as tabelas no banco caso elas não existam
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

app.include_router(router, prefix="/user")

async def async_fibonacci(n: int) -> int:
  """Rodar a função fibonacci de forma assíncrona"""
  loop = asyncio.get_event_loop()
  return await loop.run_in_executor(None, utils.fibonacci, n)


# Rota para receber comando de uma conexão estabelecida
@app.websocket("/ws")
async def testa(websocket: WebSocket):
  username = websocket.query_params.get("username")
  socket_id = str(uuid4())

  # estabelecer conexão com o websocket
  try:
    
    user = await manager.connect(
      socket_id=socket_id, 
      websocket=websocket, 
      username=username
    )
    
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
  
  except Exception as e:
    return HTTPException(400, e)