from abc import ABC, abstractmethod


class PlayerRepository(ABC):

    @abstractmethod
    def save(self, player):
        pass

    @abstractmethod
    def find_by_id(self, player_id):
        pass

    @abstractmethod
    def delete(self, player_id):
        pass


class LobbyRepository(ABC):

    @abstractmethod
    def save(self, lobby):
        pass

    @abstractmethod
    def find_by_id(self, lobby_id):
        pass

    @abstractmethod
    def delete(self, lobby_id):
        pass


class ConnectionManager(ABC):

    @abstractmethod
    async def send(self, websocket, event, data=None):
        pass

    @abstractmethod
    async def broadcast(self, players, event, data=None):
        pass