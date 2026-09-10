(function () {
    "use strict";

    const body = document.body;
    const ROOM = body.dataset.room;
    const USERNAME = body.dataset.username;

    const messagesEl = document.getElementById("messages");
    const inputEl = document.getElementById("message-input");
    const presenceList = document.getElementById("presence-list");
    const connStatus = document.getElementById("conn-status");
    const emojiRow = document.getElementById("emoji-row");

    // A few shortcut buttons for the picker
    const QUICK_EMOJIS = [
        ":smile:", ":joy:", ":heart:", ":thumbsup:", ":fire:",
        ":rocket:", ":party:", ":tada:", ":wink:", ":eyes:",
    ];

    // ------------------------------------------------------------------
    // Emoji shortcode rendering (mirrors the server, client-side too so
    // shortcodes typed live render even before a round trip).
    // ------------------------------------------------------------------
    const EMOJI_MAP = {
        ":smile:": "\u{1F604}", ":joy:": "\u{1F602}", ":heart:": "\u2764\uFE0F",
        ":thumbsup:": "\u{1F44D}", ":fire:": "\u{1F525}", ":rocket:": "\u{1F680}",
        ":party:": "\u{1F973}", ":tada:": "\u{1F389}", ":wink:": "\u{1F609}",
        ":eyes:": "\u{1F440}", ":sob:": "\u{1F62D}", ":angry:": "\u{1F620}",
        ":sunglasses:": "\u{1F60E}", ":thinking:": "\u{1F914}", ":star:": "\u2B50",
        ":sparkles:": "\u2728", ":wave:": "\u{1F44B}", ":clap:": "\u{1F44F}",
        ":cry:": "\u{1F622}", ":laughing:": "\u{1F606}", ":zap:": "\u26A1",
    };
    let emojiPattern = new RegExp(Object.keys(EMOJI_MAP)
        .sort((a, b) => b.length - a.length)
        .map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
        .join("|"), "g");

    function renderEmoji(text) {
        return text.replace(emojiPattern, (m) => EMOJI_MAP[m]);
    }

    // ------------------------------------------------------------------
    // Notification / banner (works even without permission)
    // ------------------------------------------------------------------
    function notify(title, text) {
        // Browser notification when permission granted AND window unfocused
        if (document.visibilityState === "hidden" && "Notification" in window &&
            Notification.permission === "granted") {
            try { new Notification(title, { body: text, icon: "https://emojicdn.elk.sh/\u{1F4AC}" }); }
            catch (e) { /* ignore */ }
        }
        // Always show an in-app banner when we're in the background
        if (document.visibilityState === "hidden") {
            showBanner(title + ": " + text);
        }
    }

    let bannerTimer = null;
    function showBanner(text) {
        const el = document.createElement("div");
        el.className = "notification-banner";
        el.textContent = text;
        document.body.appendChild(el);
        clearTimeout(bannerTimer);
        bannerTimer = setTimeout(() => el.remove(), 4000);
    }

    function requestNotificationPermission() {
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission().catch(() => {});
        }
    }

    // ------------------------------------------------------------------
    // Message rendering
    // ------------------------------------------------------------------
    function appendSystemText(text) {
        const div = document.createElement("div");
        div.className = "msg msg-system";
        div.textContent = text;
        messagesEl.appendChild(div);
        scrollToBottom();
    }

    function appendMessage(msg) {
        const mine = msg.username === USERNAME;
        const div = document.createElement("div");
        div.className = "msg" + (mine ? " mine" : "");
        div.dataset.username = msg.username;

        const meta = document.createElement("div");
        meta.className = "msg-meta";

        const name = document.createElement("span");
        name.className = "msg-name";
        name.textContent = msg.username;

        const time = document.createElement("span");
        time.className = "msg-time";
        if (msg.created_at && msg.created_at.length >= 16) {
            time.textContent = "[" + msg.created_at.substring(11, 16) + "]";
        }

        meta.appendChild(name);
        meta.appendChild(time);

        const text = document.createElement("div");
        text.className = "msg-text";
        text.textContent = renderEmoji(msg.emoji_rendered || msg.content);

        div.appendChild(meta);
        div.appendChild(text);
        messagesEl.appendChild(div);
        scrollToBottom();

        // Notify if from someone else and not focused
        if (!mine && document.visibilityState === "hidden") {
            notify(msg.username, text.textContent);
        }
    }

    function scrollToBottom() {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    // ------------------------------------------------------------------
    // Emoji picker
    // ------------------------------------------------------------------
    function buildEmojiPicker() {
        QUICK_EMOJIS.forEach((code) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "emoji-btn";
            btn.textContent = renderEmoji(code);
            btn.title = code;
            btn.addEventListener("click", () => {
                inputEl.value += " " + renderEmoji(code) + " ";
                inputEl.focus();
            });
            emojiRow.appendChild(btn);
        });
    }

    // ------------------------------------------------------------------
    // Socket
    // ------------------------------------------------------------------
    const socket = io();

    function sendMessage(event) {
        event.preventDefault();
        const content = inputEl.value.trim();
        if (!content) return;
        socket.emit("message", { room: ROOM, content: content });
        inputEl.value = "";
        inputEl.focus();
    }
    // Expose for the inline onsubmit handler in chat.html
    window.sendMessage = sendMessage;

    socket.on("connect", () => {
        connStatus.textContent = "connected";
        connStatus.className = "conn-status on";
        socket.emit("join", { room: ROOM });
    });

    socket.on("disconnect", () => {
        connStatus.textContent = "disconnected";
        connStatus.className = "conn-status off";
    });

    socket.on("message", (data) => {
        if (data.event === "join") {
            appendSystemText(data.username + " joined the room 👋");
        } else if (data.event === "leave") {
            appendSystemText(data.username + " left the room 👋");
        } else if (data.event === "message") {
            appendMessage(data.message);
        }
    });

    socket.on("presence", (data) => {
        presenceList.innerHTML = "";
        data.users.forEach((u) => {
            const li = document.createElement("li");
            const dot = document.createElement("span");
            dot.className = "dot";
            li.appendChild(dot);
            li.appendChild(document.createTextNode(u));
            presenceList.appendChild(li);
        });
        if (data.users.length === 0) {
            presenceList.innerHTML = '<li style="color:var(--muted);font-size:13px">No one else here</li>';
        }
    });

    // Leave room on page unload
    window.addEventListener("beforeunload", () => {
        socket.emit("leave", { room: ROOM });
    });

    // ------------------------------------------------------------------
    // Init
    // ------------------------------------------------------------------
    requestNotificationPermission();
    buildEmojiPicker();
    scrollToBottom();
    inputEl.focus();
})();
