
from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol
import asyncio
import websockets
import json
import sys
import os
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
    print(Message.SERVER_DISCONNECTED +": "+ str(e))
    os._exit(0)
  except Exception as e:
    print(Message.UNEXPECTED_ERROR_SERVER +": "+ str(e))
    os._exit(0)

async def receiver(ws: WebSocketClientProtocol):
  """Recebe recebe as mensagens vindas do servidor"""
  try:
    async for msg in ws:
      print(f"\rSERVIDOR: {msg}\nVocê: ", end="", flush=True)
  except ConnectionClosed as e:
    print(Message.SERVER_DISCONNECTED +": "+ str(e))
    os._exit(0)
  except Exception as e:
    print(Message.UNEXPECTED_ERROR_SERVER +": "+ str(e))
    os._exit(0)

async def client_connection(username: str = "client2"):
  url = "ws://localhost:8000/ws?username=%s"%username
  try:
    async with websockets.connect(url) as ws:
      loop = asyncio.get_event_loop()
      
      await asyncio.gather(receiver(ws), sender(ws, loop))
  except Exception as e:
    print(Message.CONNECT_ERROR +": "+ str(e))
    os._exit(0)


if __name__ == "__main__":
  try:
    if len(sys.argv) > 1:
      asyncio.run(client_connection(sys.argv[1]))
    else:
      asyncio.run(client_connection())
  except KeyboardInterrupt:
    print(Message.CLIENT_DISCONNECTED)