# SecurePass Generator

A Django-based random password generator web app with a sleek dark UI. Generates cryptographically secure passwords using Python's `secrets` module.

---

## Features

- Password length control (8–64 characters)
- Choose character types: uppercase, lowercase, numbers, symbols
- Exclude ambiguous characters (0, O, I, l, 1)
- Guaranteed representation of each selected character type
- Animated strength indicator (Weak / Medium / Strong / Very Secure)
- Estimated crack time display
- Copy to clipboard in one click
- Generation history (last 5 passwords)
- Fully responsive dark theme
- Clean separation of concerns (logic.py / views.py / script.js)

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python      | 3.8+    |
| Django      | 4.2+    |
| pip         | latest  |

No other external dependencies are needed.

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

### 6. Open in browser

Go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## How to Use

1. **Set length** — Drag the slider or type a number (min 8, max 64)
2. **Pick character types** — Check at least 2 boxes (uppercase, lowercase, numbers, symbols)
3. **Optional** — Tick "Exclude ambiguous characters" to skip confusing chars like `0`, `O`, `l`, `1`
4. **Click "Generate Password"** — Your password appears with a strength bar and crack time estimate
5. **Copy it** — Click "Copy to Clipboard" button
6. **Regenerate** — Hit generate again for a new password; last 5 show in history

---

## Architecture & Code Structure

The project follows a clean MVC-inspired pattern with separation of concerns:

```
.
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── db.sqlite3                     # SQLite database (auto-created)
│
├── password_generator/            # Django project config
│   ├── __init__.py
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
│
├── generator/                     # Main app
│   ├── __init__.py
│   ├── logic.py                   # Pure password generation logic (no Django deps)
│   ├── views.py                   # HTTP request/response handling only
│   ├── urls.py                    # App-level URL routes
│   ├── models.py                  # Database models (reserved for future use)
│   ├── admin.py                   # Admin panel config
│   ├── apps.py                    # App configuration
│   ├── tests.py                   # Unit tests
│   ├── migrations/                # Database migrations
│   ├── templates/
│   │   └── index.html             # Main page template
│   └── static/generator/
│       ├── style.css              # Dark theme styles
│       └── script.js              # Frontend interactivity
│
└── templates/                     # Global templates directory (unused)
```

### Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `logic.py` | Password generation algorithm, strength calculation, crack time estimation, parameter validation. Pure Python — no Django imports. |
| `views.py` | Handles Django HTTP requests, parses input, calls `logic.py`, returns JSON responses. No business logic lives here. |
| `script.js` | Frontend UI: slider sync, checkbox handling, fetch API calls, clipboard copy, history management, toast notifications. |
| `style.css` | Full dark theme with CSS custom properties, responsive grid layout, animated strength bar, custom checkboxes. |

---

## API Endpoint

### `POST /generate/`

Generates a cryptographically secure password.

**Request (form-data):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `length` | int | No | Password length (8–64, default: 16) |
| `char_types[]` | string[] | Yes | At least 2 of: `uppercase`, `lowercase`, `numbers`, `symbols` |
| `exclude_ambiguous` | string | No | `"true"` to exclude `0OIl1` |

**Response (JSON):**

```json
{
    "password": "aB3$kL9!xP2@wQ7#",
    "strength_label": "Very Secure",
    "strength_percent": 100,
    "strength_color": "#73daca",
    "crack_time": "Billions of years+"
}
```

**Error Response:**

```json
{
    "error": "Select at least 2 character types."
}
```

---

## License

MIT — free to use and modify.
