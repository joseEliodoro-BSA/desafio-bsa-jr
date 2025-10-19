
from app.server.db import get_db
from app.server.models import User
from typing import List
class UserService:
  
  async def find_users(self, connected=None) -> List[User]:
    with get_db() as db:
      
      if connected == False:
        return db.query(User).filter(User.connected == False).all()
      elif connected == True:
        return db.query(User).filter(User.connected == True).all()
      return db.query(User).all()
  
  async def find_username_connected(self, username) -> User:
    with get_db() as db:
      user = db.query(User).filter(User.username == username, User.connected == True).first()
    return user
  
  async def find_socketid_connected(self, socket_id) -> List[User]:
    with get_db() as db:
      user = user = db.query(User).filter(User.socket_id == socket_id, User.connected == True).first()
    return user
  
  async def disconnect_user(self, **kwargs) -> User:
    user = None
    if kwargs.get('username'):
      user = await self.find_username_connected(kwargs.get("username"))
    elif kwargs.get('socket_id'):
      user = await self.find_socketid_connected(kwargs.get("socket_id"))
    if not user:
      raise Exception({"message": "usuário não encontrado"})
    with get_db() as db:
      user.connected = False
      db.query(User).filter(User.id == user.id).update(
        {"connected": False}, 
        synchronize_session="fetch"
      )
      db.commit()
    return user
  
  async def disconnect_all(self):
    return "ok"
  
  
userService = UserService()