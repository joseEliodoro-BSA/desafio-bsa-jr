# clients/ws_client.py
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
import json
import random
import sys
from message import Message

async def client(username: str = "client2"):
  uri = "ws://localhost:8000/ws?username=%s"%username
  try:
    async with websockets.connect(uri) as ws:
      async def receiver():
        try:
          async for msg in ws:
            print("SERVIDOR:", msg)
        except ConnectionClosed as e:
          print(Message.SERVER_DISCONNECTED)
        except Exception as e:
          print(Message.UNEXPECTED_ERROR_SERVER)

      async def sender():
        try:
          await ws.send(json.dumps({"cmd": "fib", "n": random.randint(1, 100)}))
          await asyncio.sleep(2)
        except ConnectionClosed as e:
          print(Message.SERVER_DISCONNECTED)
        except Exception as e:
          print(Message.UNEXPECTED_ERROR_SERVER)

      await asyncio.gather(receiver(), sender())
  except Exception as e:
    print(Message.CONNECT_ERROR)

if __name__ == "__main__":
  try:
    if len(sys.argv) > 1:
      asyncio.run(client(sys.argv[1]))
    else:
      asyncio.run(client())
  except KeyboardInterrupt:
    print(Message.CLIENT_DISCONNECTED)