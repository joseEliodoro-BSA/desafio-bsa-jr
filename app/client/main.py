# clients/ws_client.py
import asyncio
import websockets
import json

async def client():
  uri = "ws://localhost:8000/ws?username=cliente1"
  async with websockets.connect(uri) as ws:
    async def receiver():
      async for msg in ws:
        print("RETURNO:", msg)

    # async def sender():
    #   await ws.send(json.dumps({"cmd":"fib","n":int(input())}))
    #   await asyncio.sleep(2)

    await asyncio.gather(receiver())

if __name__ == "__main__":
  asyncio.run(client())
