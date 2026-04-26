import asyncio
import json
import websockets


async def async_input(message):
    return await asyncio.to_thread(input, message)


async def receiver(ws):
    try:
        async for msg in ws:
            data = json.loads(msg)

            print("\n\n========== SERVER ==========")
            print("EVENT:", data.get("event"))

            response = data.get("data", {})

            if "message" in response:
                print("MESSAGE:", response["message"])

            if "lobby_id" in response:
                print("LOBBY ID:", response["lobby_id"])

            if "players" in response:
                print("\nPLAYERS ONLINE:")
                for player in response["players"]:
                    print(
                        f"- {player['name']} | {player['role']} | "
                        f"Ready: {player['ready']} | Online: {player['online']}"
                    )

            if data.get("event") == "LOBBY_CHAT":
                print(f"CHAT FROM {response.get('from')}: {response.get('message')}")

            print("============================")

    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from server")


async def main():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as ws:
        name = await async_input("Enter name: ")

        await ws.send(json.dumps({
            "action": "connect",
            "name": name
        }))

        asyncio.create_task(receiver(ws))

        while True:
            print("\n========== PUBG STYLE LOBBY ==========")
            print("1. Create Lobby")
            print("2. Join Lobby")
            print("3. Ready")
            print("4. Unready")
            print("5. Chat")
            print("6. Show Lobby Players")
            print("7. Start Match Captain Only")
            print("8. Exit")

            choice = await async_input("Choice: ")

            if choice == "1":
                await ws.send(json.dumps({
                    "action": "create_lobby"
                }))

            elif choice == "2":
                lobby_id = await async_input("Enter Lobby ID: ")
                await ws.send(json.dumps({
                    "action": "join_lobby",
                    "lobby_id": lobby_id
                }))

            elif choice == "3":
                await ws.send(json.dumps({
                    "action": "ready"
                }))

            elif choice == "4":
                await ws.send(json.dumps({
                    "action": "unready"
                }))

            elif choice == "5":
                msg = await async_input("Message: ")
                await ws.send(json.dumps({
                    "action": "chat",
                    "message": msg
                }))

            elif choice == "6":
                await ws.send(json.dumps({
                    "action": "lobby_info"
                }))

            elif choice == "7":
                await ws.send(json.dumps({
                    "action": "start_match"
                }))

            elif choice == "8":
                print("Exiting...")
                break

            else:
                print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())