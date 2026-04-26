from dataclasses import dataclass, field


MAX_PLAYERS = 4


@dataclass
class Player:
    player_id: str
    name: str
    websocket: object
    ready: bool = False
    lobby_id: str | None = None


@dataclass
class Lobby:
    lobby_id: str
    captain_id: str
    players: dict = field(default_factory=dict)
    started: bool = False

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            raise Exception("Lobby is full. Maximum 4 players allowed.")

        self.players[player.player_id] = player
        player.lobby_id = self.lobby_id

    def remove_player(self, player_id):
        if player_id in self.players:
            self.players[player_id].lobby_id = None
            del self.players[player_id]

    def is_captain(self, player_id):
        return self.captain_id == player_id

    def player_count(self):
        return len(self.players)

    def is_full(self):
        return len(self.players) == MAX_PLAYERS

    def non_captain_players(self):
        return [
            player for player in self.players.values()
            if player.player_id != self.captain_id
        ]

    def all_team_members_ready(self):
        members = self.non_captain_players()
        return len(members) == 3 and all(player.ready for player in members)

    def lobby_status(self):
        return {
            "lobby_id": self.lobby_id,
            "captain_id": self.captain_id,
            "players_count": len(self.players),
            "max_players": MAX_PLAYERS,
            "players": [
                {
                    "player_id": player.player_id,
                    "name": player.name,
                    "role": "CAPTAIN" if player.player_id == self.captain_id else "MEMBER",
                    "ready": player.ready,
                    "online": True
                }
                for player in self.players.values()
            ]
        }