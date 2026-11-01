# Importing the relevant libraries
import websockets
import asyncio
import json

# Server 
PORT = 12345

# Connected clients and their public keys stored by username
connected = {}
public_keys = {}



async def relay(websocket):
    print("A client just connected")
    user = None
    #for incoming messages
    try:
        async for raw in websocket: 
            msg = json.loads(raw) #users message

            #allows users to register | name recieved on  client.py
            if msg["type"] == "register":
                user = msg["user"]
                connected[user] = websocket
                public_keys[user] = msg["keys"]
                print(user + " registered")

            #when a user requests another users keys
            elif msg["type"] == "get_keys":
                await websocket.send(json.dumps({ #json.dumps converts py obj to json string
                    "type": "keys",
                    "user": msg["user"],
                    "keys": public_keys.get(msg["user"]),
                }))

            #forward handshake and messages without reading them
            elif msg.get("to") in connected: # read 'to' field and ensure they're connected
                await connected[msg["to"]].send(raw) # .send(raw) sends the message | await lets other users be served while the send finishes.
    #for disconnecting clients
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.pop(user, None)
        print("A client just disconnected")

#start the server
async def main():
    async with websockets.serve(relay, "localhost", PORT):
        print("Server is listening on port " + str(PORT))
        await asyncio.Future()  # run forever

asyncio.run(main())