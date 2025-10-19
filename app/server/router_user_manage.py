    
from fastapi import HTTPException


from typing import List

from app.server.websocket_manage import manager

from app.server.models import User
from app.server.service import userService
from app.server.schemas import UserSchema

from fastapi import APIRouter

router = APIRouter()


class Tags:
  LOG_CONNECTION = "logs de conexão"

@router.get(
  "/", 
  response_model=List[UserSchema], 
  tags=[Tags.LOG_CONNECTION], 
  description="Retorna logs de quando cada usuário se conectou"
  )
async def list_all_logs():
  return await userService.find_users()

@router.get(
  "/connected", 
  response_model=List[UserSchema],
  description="Retorna logs de usuários com conexões ativa",
  tags=[Tags.LOG_CONNECTION], 
  )
async def list_user_connections():
  return await userService.find_users(True)

@router.get(
  "/disconnected", 
  response_model=List[UserSchema],
  tags=[Tags.LOG_CONNECTION], 
  description="Retorna logs de usuários com conexões ativa",
  )
async def list_user_connections():
  return await userService.find_users(False)

@router.patch(
  "/disconnect", 
  tags=[Tags.LOG_CONNECTION], 
  description="Desconecta usuário ativo",
  )
async def disconnect_user(username: str|None=None, socket_id: str|None = None):
  user: User|None = None
  try:
    if username:
      user =  await userService.disconnect_user(username=username)
    elif socket_id:
      user = await userService.disconnect_user(socket_id=socket_id)

    # await manager.send_private_message("{'message': deslogado}", user.socket_id)
    await manager.disconnect(user.socket_id)
    
    return {"message": f"usuário {user.username} deslogado"}
  except:
    return HTTPException(400, {"message": "usuário não encontrado"})
  
@router.patch(
"/disconnect/all", 
tags=[Tags.LOG_CONNECTION], 
description="Desconecta todos os usuário ativo",
)
async def disconnect_all():
  await manager.disconnect_all()