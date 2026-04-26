from core.exceptions import InvalidCommandException


class CommandValidator:

    @staticmethod
    def require_action(action):
        if not action:
            raise InvalidCommandException("Action is required")

    @staticmethod
    def validate_connect(data):
        name = data.get("name")

        if not name or not str(name).strip():
            raise InvalidCommandException("Player name is required")

    @staticmethod
    def validate_join_lobby(data):
        lobby_id = data.get("lobby_id")

        if not lobby_id or not str(lobby_id).strip():
            raise InvalidCommandException("Lobby ID is required")

    @staticmethod
    def validate_chat(data):
        message = data.get("message")

        if not message or not str(message).strip():
            raise InvalidCommandException("Message cannot be empty")