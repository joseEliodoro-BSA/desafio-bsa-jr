
from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol
import asyncio
import websockets
import json
import sys

from message import Message

async def sender(ws: WebSocketClientProtocol, loop): 
  """Envia mensagem para o servidor"""
  try:
    while True:
      
      user_input = await loop.run_in_executor(None, input, "Você: ")
      
      if user_input.strip().lower() == "sair":
          print(Message.CLIENT_DISCONNECTED)
          await ws.close()
          break
      await ws.send(json.dumps({"cmd": "fib", "n": int(user_input)}))
      
  except ConnectionClosed as e:
    print(Message.SERVER_DISCONNECTED)
  except Exception as e:
    print(Message.UNEXPECTED_ERROR_SERVER)

async def receiver(ws: WebSocketClientProtocol):
  """Recebe recebe as mensagens vindas do servidor"""
  try:
    async for msg in ws:
      print(f"\rSERVIDOR: {msg}\nVocê: ", end="", flush=True)
  except ConnectionClosed as e:
    print(Message.SERVER_DISCONNECTED)
  except Exception as e:
    print(Message.UNEXPECTED_ERROR_SERVER)

async def client_connection(username: str = "client2"):
  url = "ws://localhost:8000/ws?username=%s"%username
  try:
    async with websockets.connect(url) as ws:
      loop = asyncio.get_event_loop()
      
      await asyncio.gather(receiver(ws), sender(ws, loop))
  except Exception as e:
    print(Message.CONNECT_ERROR +": "+ e)


if __name__ == "__main__":
  try:
    if len(sys.argv) > 1:
      asyncio.run(client_connection(sys.argv[1]))
    else:
      asyncio.run(client_connection())
  except KeyboardInterrupt:
    print(Message.CLIENT_DISCONNECTED)