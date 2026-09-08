import os
import functools

from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, send

import database
from emoji import render_emoji

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# Eventlet provides a WSGI server with real WebSocket support ("threading"
# mode runs on Werkzeug, which cannot upgrade connections to WebSocket).
# Fall back to "threading" if eventlet is unavailable.
try:
    import eventlet  # noqa: F401
    socketio = SocketIO(app, async_mode="eventlet")
except ImportError:
    socketio = SocketIO(app, async_mode="threading")

# Track active users per room for presence notifications.
# room_name -> set of usernames
ROOM_USERS = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def current_username():
    return session.get("username")


def broadcast_presence(room_name):
    """Tell every client in a room who is currently present."""
    users = sorted(ROOM_USERS.get(room_name, set()))
    emit("presence", {"room": room_name, "users": users}, room=room_name)


def add_room_user(room_name, username):
    """Return True if the user was newly added (was not already present)."""
    room_set = ROOM_USERS.setdefault(room_name, set())
    was_present = username in room_set
    room_set.add(username)
    return not was_present


def remove_room_user(room_name, username):
    room_set = ROOM_USERS.get(room_name)
    if room_set:
        room_set.discard(username)
        if not room_set:
            ROOM_USERS.pop(room_name, None)


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if current_username() is None:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# HTTP routes
# ---------------------------------------------------------------------------

@app.route("/")
@login_required
def index():
    rooms = database.list_rooms()
    return render_template("index.html", username=current_username(), rooms=rooms)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_username():
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not username or not password:
            flash("Username and password are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            user = database.create_user(username, password)
            if user is None:
                flash("That username is already taken.", "error")
            else:
                session["username"] = user["username"]
                session["user_id"] = user["id"]
                flash(f"Welcome, {user['username']}!", "success")
                return redirect(url_for("index"))
    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_username():
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = database.verify_user(username, password)
        if user is None:
            flash("Invalid username or password.", "error")
        else:
            session["username"] = user["username"]
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("index"))
    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/room/<name>")
@login_required
def room_page(name):
    user_id = session.get("user_id")
    room = database.get_or_create_room(name, user_id)
    if room is None:
        flash("Room names cannot be empty.", "error")
        return redirect(url_for("index"))
    history = database.get_message_history(room["id"])
    rooms = database.list_rooms()
    return render_template(
        "chat.html",
        username=current_username(),
        room=room["name"],
        room_id=room["id"],
        history=history,
        rooms=rooms,
    )


# ---------------------------------------------------------------------------
# Socket events
# ---------------------------------------------------------------------------

@socketio.on("join")
def on_join(data):
    room_name = data.get("room", "").strip()
    username = current_username()
    if not room_name or not username:
        return

    user_id = session.get("user_id")
    room = database.get_or_create_room(room_name, user_id)
    if room is None:
        return

    join_room(room["name"])
    is_new = add_room_user(room["name"], username)
    broadcast_presence(room["name"])

    if is_new:
        send(
            {"event": "join", "username": username, "room": room["name"]},
            room=room["name"],
        )


@socketio.on("leave")
def on_leave(data):
    username = current_username()
    room_name = data.get("room", "").strip()
    if not username or not room_name:
        return
    leave_room(room_name)
    remove_room_user(room_name, username)
    broadcast_presence(room_name)
    send(
        {"event": "leave", "username": username, "room": room_name},
        room=room_name,
    )


@socketio.on("message")
def handle_message(data):
    username = current_username()
    room_name = data.get("room", "").strip()
    content = data.get("content", "").strip()
    if not username or not room_name or not content:
        return
    if len(content) > 2000:
        content = content[:2000]

    user_id = session.get("user_id")
    room = database.get_or_create_room(room_name, user_id)
    if room is None:
        return

    emoji_rendered = render_emoji(content)
    row = database.save_message(room["id"], user_id, username, content, emoji_rendered)
    payload = database.format_message_for_client(row)
    payload["room"] = room["name"]

    send({"event": "message", "message": payload}, room=room["name"])


@socketio.on("connect")
def on_connect():
    pass


@socketio.on("disconnect")
def on_disconnect():
    # Clean up any rooms this user silently abandoned
    username = current_username()
    if not username:
        return
    for room_name in list(ROOM_USERS.keys()):
        if username in ROOM_USERS.get(room_name, set()):
            remove_room_user(room_name, username)
            broadcast_presence(room_name)
            send(
                {"event": "leave", "username": username, "room": room_name},
                room=room_name,
            )


if __name__ == "__main__":
    database.init_db()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
