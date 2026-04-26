import asyncio
import uuid
from core.models import Player, Lobby


class LobbyService:

    def __init__(self, player_repo, lobby_repo, conn_mgr):
        self.player_repo = player_repo
        self.lobby_repo = lobby_repo
        self.conn_mgr = conn_mgr

    def _id(self):
        return str(uuid.uuid4())[:6].upper()

    async def connect(self, ws, name):
        player = Player(
            player_id=self._id(),
            name=name,
            websocket=ws
        )

        self.player_repo.save(player)

        await self.conn_mgr.send(ws, "CONNECTED", {
            "player_id": player.player_id,
            "name": player.name,
            "message": "Connected successfully."
        })

        return player

    async def create_lobby(self, player_id):
        player = self.player_repo.find(player_id)

        lobby = Lobby(
            lobby_id=self._id(),
            captain_id=player.player_id
        )

        lobby.add_player(player)
        self.lobby_repo.save(lobby)

        await self.conn_mgr.send(player.websocket, "LOBBY_CREATED", {
            "message": "Lobby created. You are the captain.",
            **lobby.lobby_status()
        })

    async def join(self, player_id, lobby_id):
        player = self.player_repo.find(player_id)
        lobby = self.lobby_repo.find(lobby_id)

        if not lobby:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Lobby not found. Enter correct lobby ID."
            })
            return

        if lobby.started:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Match already started."
            })
            return

        try:
            lobby.add_player(player)
        except Exception as error:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": str(error)
            })
            return

        self.lobby_repo.save(lobby)

        await self.conn_mgr.broadcast(
            lobby.players.values(),
            "PLAYER_JOINED",
            {
                "message": f"{player.name} joined the lobby.",
                **lobby.lobby_status()
            }
        )

    async def ready(self, player_id, value):
        player = self.player_repo.find(player_id)

        if not player.lobby_id:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "You are not inside any lobby."
            })
            return

        lobby = self.lobby_repo.find(player.lobby_id)

        if lobby.is_captain(player_id):
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Captain cannot ready. Captain can start match."
            })
            return

        player.ready = value
        self.player_repo.save(player)
        self.lobby_repo.save(lobby)

        await self.conn_mgr.broadcast(
            lobby.players.values(),
            "READY_STATUS_CHANGED",
            {
                "message": f"{player.name} is {'READY' if value else 'NOT READY'}.",
                **lobby.lobby_status()
            }
        )

    async def chat(self, player_id, message):
        player = self.player_repo.find(player_id)

        if not player.lobby_id:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Join lobby before chatting."
            })
            return

        lobby = self.lobby_repo.find(player.lobby_id)

        await self.conn_mgr.broadcast(
            lobby.players.values(),
            "LOBBY_CHAT",
            {
                "from": player.name,
                "message": message
            }
        )

    async def lobby_info(self, player_id):
        player = self.player_repo.find(player_id)

        if not player.lobby_id:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "You are not inside any lobby."
            })
            return

        lobby = self.lobby_repo.find(player.lobby_id)

        await self.conn_mgr.send(player.websocket, "LOBBY_INFO", lobby.lobby_status())

    async def start_match(self, player_id):
        player = self.player_repo.find(player_id)

        if not player.lobby_id:
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "You are not inside any lobby."
            })
            return

        lobby = self.lobby_repo.find(player.lobby_id)

        if not lobby.is_captain(player_id):
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Only captain can start the match."
            })
            return

        if not lobby.is_full():
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "Need 4 players to start the match."
            })
            return

        if not lobby.all_team_members_ready():
            await self.conn_mgr.send(player.websocket, "ERROR", {
                "message": "All 3 team members must be ready before starting."
            })
            return

        lobby.started = True
        self.lobby_repo.save(lobby)

        await self.conn_mgr.broadcast(
            lobby.players.values(),
            "MATCH_STARTING",
            {
                "message": "Captain started the match. Match starting in 3 seconds...",
                **lobby.lobby_status()
            }
        )

        await asyncio.sleep(3)

        await self.conn_mgr.broadcast(
            lobby.players.values(),
            "MATCH_STARTED",
            {
                "message": "Match started successfully. Good luck team!"
            }
        )

    async def disconnect(self, player_id):
        player = self.player_repo.find(player_id)

        if not player:
            return

        lobby_id = player.lobby_id

        if lobby_id:
            lobby = self.lobby_repo.find(lobby_id)

            if lobby:
                was_captain = lobby.is_captain(player_id)

                lobby.remove_player(player_id)

                if len(lobby.players) == 0:
                    self.lobby_repo.delete(lobby_id)
                else:
                    if was_captain:
                        new_captain = next(iter(lobby.players.values()))
                        lobby.captain_id = new_captain.player_id

                    self.lobby_repo.save(lobby)

                    await self.conn_mgr.broadcast(
                        lobby.players.values(),
                        "PLAYER_LEFT",
                        {
                            "message": f"{player.name} left the lobby.",
                            **lobby.lobby_status()
                        }
                    )

        self.player_repo.delete(player_id)