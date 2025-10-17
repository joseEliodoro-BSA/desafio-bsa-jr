from fastapi import WebSocket
from typing import Dict, List
from app.server.db import get_db
from app.server.models import User
from datetime import datetime
import asyncio

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
        print(user)
        user.connected = False
        user.last_seen = datetime.now()
        db.add(user)
        db.commit()
  # async def send_personal_message(self, message: str, websocket: WebSocket):
  #   await websocket.send_text(message)

  # async def broadcast(self, message: str):
  #   for connection in self.active_connections:
  #     await connection.send_text(message)
  
manager = WebSocketManager()