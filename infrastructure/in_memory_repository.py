class InMemoryPlayerRepository:
    def __init__(self):
        self.players = {}

    def save(self, player):
        self.players[player.player_id] = player

    def find(self, player_id):
        return self.players.get(player_id)

    def delete(self, player_id):
        self.players.pop(player_id, None)


class InMemoryLobbyRepository:
    def __init__(self):
        self.lobbies = {}

    def save(self, lobby):
        self.lobbies[lobby.lobby_id] = lobby

    def find(self, lobby_id):
        return self.lobbies.get(lobby_id)

    def delete(self, lobby_id):
        self.lobbies.pop(lobby_id, None)