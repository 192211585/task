class CommandDispatcher:

    def __init__(self, service):
        self.service = service

    async def dispatch(self, action, data, player, ws):

        if action == "connect":
            return await self.service.connect(ws, data["name"])

        if not player:
            return

        if action == "create_lobby":
            await self.service.create_lobby(player.player_id)

        elif action == "join_lobby":
            await self.service.join(player.player_id, data["lobby_id"].upper())

        elif action == "ready":
            await self.service.ready(player.player_id, True)

        elif action == "unready":
            await self.service.ready(player.player_id, False)

        elif action == "chat":
            await self.service.chat(player.player_id, data["message"])

        elif action == "lobby_info":
            await self.service.lobby_info(player.player_id)

        elif action == "start_match":
            await self.service.start_match(player.player_id)