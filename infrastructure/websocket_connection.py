import json


class WebSocketConnectionManager:

    async def send(self, websocket, event, data=None):
        await websocket.send(json.dumps({
            "event": event,
            "data": data or {}
        }))

    async def broadcast(self, players, event, data=None):
        for player in list(players):
            try:
                await self.send(player.websocket, event, data)
            except:
                pass