import asyncio
import json
import websockets

from config.settings import HOST, PORT
from infrastructure.logger import logger
from infrastructure.in_memory_repository import (
    InMemoryPlayerRepository,
    InMemoryLobbyRepository
)
from infrastructure.websocket_connection import WebSocketConnectionManager
from application.lobby_service import LobbyService
from application.command_dispatcher import CommandDispatcher


player_repo = InMemoryPlayerRepository()
lobby_repo = InMemoryLobbyRepository()
conn_mgr = WebSocketConnectionManager()

service = LobbyService(player_repo, lobby_repo, conn_mgr)
dispatcher = CommandDispatcher(service)


async def handle_client(websocket):
    player = None

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")

                result = await dispatcher.dispatch(
                    action=action,
                    data=data,
                    player=player,
                    ws=websocket
                )

                if result:
                    player = result

            except json.JSONDecodeError:
                await conn_mgr.send(websocket, "ERROR", {
                    "message": "Invalid JSON format."
                })

            except Exception as error:
                logger.exception(error)
                await conn_mgr.send(websocket, "ERROR", {
                    "message": str(error)
                })

    except websockets.exceptions.ConnectionClosed:
        logger.info("Client connection closed")

    finally:
        if player:
            await service.disconnect(player.player_id)


async def main():
    logger.info(f"Server running on ws://{HOST}:{PORT}")

    async with websockets.serve(
        handle_client,
        HOST,
        PORT,
        ping_interval=None
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())