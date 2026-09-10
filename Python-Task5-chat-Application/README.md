# OpenChat

A full-featured, real-time group chat web application built with **Python,
Flask, Flask-SocketIO (WebSockets), and SQLite**. Users can register, log in,
join or create named rooms, see live presence, load past message history, send
emoji shortcodes, and receive desktop notifications for background messages.

---

## ✨ Features

### Beginner Tier (all included)
- ✅ Server-side Flask app listening for incoming browser connections
- ✅ Real-time, bidirectional message exchange over WebSockets
- ✅ Timestamp prefix on every message, e.g. `[14:35]`
- ✅ Graceful disconnect handling — other users are notified when someone leaves
- ✅ Runs entirely on one machine via `localhost`

### Advanced Tier
- ✅ GUI chat window served as a web app (works in any browser)
- ✅ User registration & login (username + password hashed with Werkzeug/SHA-256)
- ✅ Multiple chat rooms — users can create or join named rooms
- ✅ Message history — past messages load from SQLite when you join a room
- ✅ Desktop (browser) notifications for messages while the window is unfocused
- ✅ In-app banner notification for background messages
- ✅ Emoji support — shortcodes like `:smile:` render as Unicode `😄`
- ✅ Live presence indicator showing who is in the current room

---

## 🗂️ Project Structure

```
chat-application/
├── app.py           # Flask app + SocketIO event handlers + routes
├── database.py      # SQLite layer (users, rooms, messages)
├── emoji.py         # Emoji shortcode → Unicode conversion
├── requirements.txt
├── chat.db          # SQLite database (created on first run)
├── templates/
│   ├── auth.html    # Login / register page
│   ├── index.html   # Rooms overview / home
│   └── chat.html    # Main chat window
└── static/
    ├── style.css
    └── chat.js      # Socket.IO client + emoji + notifications
```

---

## 🚀 Quick Start

```bash
# 1. Install Python 3.8+ and create a virtual environment (optional)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python app.py

# 4. Open a browser (open multiple tabs/windows for a multi-user test)
#    on the same machine:
http://localhost:5000
```

Register two accounts, then open two browser windows with different users,
join (or create) the same room, and chat in real time. 🎉

> `chat.db` is created automatically on first launch. Delete it to reset all
> users and message history.

---

## 🔐 Security Transparency (End-to-End Awareness)

It is important to be clear about **what this app does and does not protect**:

### How messages are stored
- All chat messages are stored **in plaintext** in the local SQLite database
  (`chat.db`), in the `messages` table.
- Passwords are **not** stored in plaintext. They are hashed with Werkzeug's
  `generate_password_hash` (PBKDF2-SHA256 with a per-user salt).

### What is NOT encrypted
- **Message content is stored in plaintext.** Anyone with read access to
  `chat.db` can read every message ever sent.
- **Traffic between browser and server is NOT encrypted** when running over
  plain HTTP (`localhost:5000`). For real deployment you must put the app
  behind HTTPS (e.g. Nginx with TLS, or a reverse proxy).
- **There is no end-to-end (E2E) encryption.** The server receives and stores
  every message in readable form. Unlike apps like Signal, the server operator
  CAN read messages.
- **Live traffic over WebSockets is likewise unencrypted** without TLS.

### Recommendations for real-world use
- Replace the hardcoded dev `SECRET_KEY` with a strong secret via the
  `SECRET_KEY` environment variable (set as `os.environ`).
- Serve behind HTTPS in production.
- This project is intended as a **learning exercise**, not for handling
  sensitive data.

---

## 🧩 How Real-Time Messaging Works

1. The browser opens a WebSocket via **Socket.IO** (`/socket.io/`).
2. On connect the client emits `join` with a room name; the server adds them
   to a Socket.IO room and broadcasts the new presence list.
3. When a user sends a message, the client emits a `message` event. The server:
   - resolves the room,
   - renders emoji shortcodes via `emoji.render_emoji`,
   - **persists the message to SQLite** (`database.save_message`),
   - re-broadcasts it to everyone in the room.
4. When someone disconnects, the server broadcasts a `leave` event and updates
   presence so remaining users are notified.
5. On entering a room page, the server fetches the last 100 messages
   (`database.get_message_history`) and renders them server-side.

The app uses the **eventlet** async runtime for real WebSocket support
(recommended for Flask-SocketIO). If eventlet is not installed it falls back to
Werkzeug's "threading" mode, which uses HTTP long-polling instead of WebSockets
(works, but with more latency and no WebSocket upgrades).

---

## 🎈 Emoji Support

Type a shortcode to send an emoji:

| You type   | You see |
|------------|---------|
| `:smile:`  | 😄       |
| `:heart:`  | ❤️       |
| `:rocket:` | 🚀       |
| `:fire:`   | 🔥       |
| `:party:`  | 🥳       |

The mapping is defined in `emoji.py` (server-side) and mirrored in
`static/chat.js` (client-side) so it renders instantly. Unknown shortcodes are
left as plain text.

---

## 🤝 Contributing / Extending

- **Add emojis**: extend the `EMOJI_MAP` dict in `emoji.py` and the matching
  map in `static/chat.js`.
- **Message history depth**: change the `limit` parameter in
  `database.get_message_history` (default 100).
- **Private rooms**: you could add per-room password or invite logic in
  `app.py`.

---

## 📚 References

- [Flask-SocketIO documentation](https://flask-socketio.readthedocs.io/)
- [Python socket programming tutorial](https://docs.python.org/3/howto/sockets.html)
- [Socket.IO official docs](https://socket.io/docs/v4/)
