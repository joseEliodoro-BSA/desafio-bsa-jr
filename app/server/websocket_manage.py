from fastapi import WebSocket
from typing import Dict, List
from app.server.db import get_db
from app.server.models import User
from datetime import datetime
import asyncio
import json
from app.server.service import userService

class WebSocketManager():
  """ Classe para gerenciamento dos clientes conectados no websocket """
  def __init__(self):
    self.active_connections: Dict[str, WebSocket] = {}  # socket_id -> websocket
    self.lock = asyncio.Lock()
    
  async def connect(self, socket_id: str, websocket: WebSocket, username: str):
    await websocket.accept()
    
    # adicionar o objeto do websocket na lista de conexões ativas
    async with self.lock:
      self.active_connections[socket_id] = websocket
    
    if await userService.find_username_connected(username):
      await websocket.send_text('{"message": "Usuário já conectado"}')
      self.active_connections.pop(socket_id)
      await websocket.close()
      raise Exception({"message": "Usuário já conectado"})
    
    with get_db() as db:
      user = User(
        username = username,
        socket_id = socket_id,
        )
      db.add(user)
      db.commit()
      db.refresh(user)
      return user

  async def disconnect(self, socket_id: str):
    async with self.lock:
      self.active_connections.pop(socket_id)
    with get_db() as db:
      user = db.query(User).where(User.socket_id==socket_id).first()
      if user:
        user.connected = False
        user.last_seen = datetime.now()
        db.add(user)
        db.commit()
      #self.active_connections.pop(socket_id)
  
  async def send_private_message(self, message: Dict, socket_id: str):
    if not self.active_connections.get(socket_id):
      raise Exception("'conexão inativa")
    if not await userService.find_socketid_connected(socket_id):
      raise Exception({"message": "Usuário nnão conectado"})
    await self.active_connections.get(socket_id).send_text(json.dumps(message))
  
  async def disconnect_user(self, socket_id: str):
    if self.active_connections.get(socket_id):
      await self.active_connections.get(socket_id).close()
  
  async def disconnect_all(self):
    for socket_id in list(self.active_connections.keys()):
      await self.disconnect(socket_id=socket_id)

  async def broadcast(self, message: str):
    
    async with self.lock:
      users: User = await userService.find_users(True)
      socket_ids = [user.socket_id for user in users]
    
      for socket_id in self.active_connections.keys():
        if socket_id not in socket_ids:
          self.active_connections.pop(socket_id)
          
      connections = list(self.active_connections.values())
      
    
    coros = [ws.send_text(message) for ws in connections]
    if coros:
      await asyncio.gather(*coros, return_exceptions=True)
 
manager = WebSocketManager()

async def broadcast_message_time():
  """Envia uma mensage de broadcast com data e hora atual a cada segundo"""

  while True:
    try:
      await manager.broadcast(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception:
      pass
    await asyncio.sleep(1)
    
         