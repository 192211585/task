class LobbyException(Exception):
    pass


class InvalidCommandException(LobbyException):
    pass


class PlayerNotFoundException(LobbyException):
    pass


class LobbyNotFoundException(LobbyException):
    pass


class GameAlreadyStartedException(LobbyException):
    pass


class PlayerNotInLobbyException(LobbyException):
    pass