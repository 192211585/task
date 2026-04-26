# Real-Time Game Lobby Server (Python + WebSockets)

## 📌 Overview
This project is a real-time multiplayer lobby server built using Python and WebSockets.  
It simulates a game lobby where players can connect, create/join rooms, chat, set ready status, and start a match.

---

## 🚀 Features

- Real-time communication using WebSockets
- Create and join lobby using Lobby ID
- Maximum 4 players per lobby
- One player acts as Captain (host)
- Players can mark themselves as READY / NOT READY
- Captain starts the match
- Match starts only when:
  - 4 players are present
  - All non-captain players are READY
- Live chat between players
- Shows player list and status in real time

---

## 🏗️ Project Structure
game_lobby_enterprise/
│
├── server.py
├── client.py
├── requirements.txt
│
├── core/
├── application/
├── infrastructure/
└── config/


---

## ⚙️ Requirements

- Python 3.10+
- WebSockets library

Install dependencies:

```bash
pip install -r requirements.txt

▶️ How to Run
Step 1: Start Server
python server.py

Expected output:

Server running on ws://localhost:8765
Step 2: Start Clients (Open multiple terminals)
python client.py
🎮 How to Use
Player 1 (Captain)
Enter name
Choose:
1 → Create Lobby
Copy the Lobby ID
Player 2, 3, 4
Run client
Enter name
Choose:
2 → Join Lobby
Enter Lobby ID
Ready Up

Players (except captain):

3 → Ready
Start Match

Captain:

7 → Start Match



📊 Sample Output
EVENT: LOBBY_CREATED
LOBBY ID: ABC123

LOBBY STATUS:
Players: 1/4
vineeth | CAPTAIN | NOT READY
