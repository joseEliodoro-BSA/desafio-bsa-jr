from fastapi import WebSocket
from typing import Dict, List
from app.server.db import get_db
from app.server.models import User
from datetime import datetime
import asyncio
import json

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
    
    with get_db() as db:
      user = User(
        email = f'{username}@test.com',
        username = username,
        socket_id = socket_id,
        )
      user_exists  = db.query(
        db.query(User)
        .filter(User.username == username, User.connected == True)
        .exists()
      ).scalar()
      if user_exists:
        raise Exception("usuário já está conectado")
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
  # async def send_personal_message(self, message: str, websocket: WebSocket):
  #   await websocket.send_text(message)
  
  async def disconnect_all(self):
    async with self.lock:
      self.active_connections.pop(socket_id)
    for socket_id in self.active_connections.keys():
      await self.disconnect(socket_id=socket_id)

  async def broadcast(self, message: str):
    async with self.lock:
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
    
         