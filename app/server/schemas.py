from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
  socket_id: str
  username: str
  connected: bool
  connected_at: datetime
  last_seen: datetime