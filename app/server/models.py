from sqlalchemy import Column, Integer, String, String, Boolean, DateTime
from server.db import Base
from datetime import datetime

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  
  username = Column(String(255))
  socket_id = Column(String(100))
  connected= Column(Boolean, default=True)
  connected_at = Column(DateTime, default=datetime.now())
  last_seen = Column(DateTime, default=datetime.now())
  
  def __str__(self):
    return "User[username={}, socket_id={}]".format(self.username, self.socket_id)