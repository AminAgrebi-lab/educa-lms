# Educa — E-Learning Platform 🎓

A full-featured e-learning platform built with Django 5: a course CMS with multi-type
content, student enrollment, real-time per-course chat over WebSockets, a REST API,
and a complete Docker-based production stack (NGINX + uWSGI + Daphne + PostgreSQL + Redis).

Capstone project of the *Django 5 By Example* specialization —
Course 3: *Django Advanced Applications: E-Learning, APIs & Deployment*.

---

## ✨ Features

- **Course CMS** — instructors build courses from modules with four content types:
  text, video, image, and file.
- **Student area** — enrollment workflow, subject-filtered catalog, and course view.
- **Real-time chat** — per-course chat rooms on Django Channels + Redis (WebSockets),
  with recent messages persisted in the database.
- **REST API** — subjects & courses endpoints with custom permissions, pagination,
  and nested content serialization (Django REST Framework).
- **Caching & monitoring** — Redis-backed cache plus `django-redisboard`
  for live Redis inspection inside the admin.
- **Production engineering**
  - Settings split into `base` / `local` / `prod` environments
  - Secrets via environment variables (`python-decouple` + `.env`, never in Git)
  - Docker Compose stack: PostgreSQL, Redis, uWSGI, Daphne, NGINX
  - TLS termination at NGINX with an HTTP→HTTPS 301 redirect
  - Custom middleware: subdomain routing (`<slug>.domain` → `/course/<slug>/`)
  - Custom management command: `enroll_reminder` (bulk e-mail reminders)

## 🏗️ Production Architecture

```
Browser
   │  HTTPS :443
   ▼
NGINX ── TLS termination + static/media serving
   ├── /static/, /media/  → served directly from disk
   ├── /ws/…              → Daphne (ASGI / WebSockets) :9001
   └── everything else    → uWSGI (WSGI / HTTP) via unix socket
                               │
                               ▼
                            Django 5
                               ├── PostgreSQL  (db service)
                               └── Redis       (cache + channel layer)
```

Two app servers on purpose: uWSGI serves short synchronous HTTP requests efficiently,
while Daphne holds long-lived WebSocket connections for the chat.
NGINX routes by path prefix and never exposes the app servers to the internet.

## 🧰 Tech Stack

| Layer     | Technology |
|-----------|------------|
| Backend   | Python 3.12, Django 5.2, Django REST Framework |
| Real-time | Django Channels 4, Daphne, channels-redis, WebSockets |
| Data      | SQLite (dev) / PostgreSQL 16 (prod), Redis 7 (cache + channel layer) |
| Servers   | uWSGI (WSGI), Daphne (ASGI), NGINX (reverse proxy, TLS, static) |
| Ops       | Docker Compose, wait-for-it, python-decouple, OpenSSL (self-signed cert) |

##  Project Structure

```
educa-lms/
├── educa/            # project package: settings/ (base·local·prod), asgi.py, wsgi.py
├── courses/          # CMS app (+ middleware.py — subdomain routing)
├── students/         # enrollment app (+ management/commands/enroll_reminder.py)
├── chat/             # Channels consumers, routing, room template
├── config/
│   ├── uwsgi/uwsgi.ini
│   └── nginx/default.conf.template
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Local Setup

Prerequisites: Python 3.12 and a running Redis server (native service or container).

```bash
git clone https://github.com/AminAgrebi-lab/educa-lms.git
cd educa-lms
python -m venv env
env\educa\Scripts\activate        # Windows
# source env/bin/activate         # Linux / macOS

pip install -r requirements.txt   # on Windows: comment out `uwsgi` first (no Windows build)

python manage.py migrate  --settings=educa.settings.local
python manage.py runserver --settings=educa.settings.local
```

Open http://127.0.0.1:8000/ — catalog, student area, chat rooms and API are live.

> The full production stack is described in `Dockerfile`, `docker-compose.yml`,
> `config/uwsgi/uwsgi.ini` and `config/nginx/default.conf.template`.
> Bring it up with `docker compose up` (requires Docker Desktop).

## 🐳 Production Stack (Docker-ready)

| Service  | Role |
|----------|------|
| `db`     | postgres:16.2 — persistent volume `./data/db` |
| `cache`  | redis:7.2.4 — persistent volume `./data/cache` |
| `web`    | uWSGI serving `educa.wsgi:application` over a unix socket |
| `daphne` | ASGI server for WebSockets on :9001 |
| `nginx`  | reverse proxy, TLS on 443, static/media, `/ws/` routing |

Startup order is guarded by `wait-for-it.sh`; Django reads database credentials
from environment variables injected by Compose via `python-decouple`.

## 📸 Screenshots

{{Add 3–4 images here: course catalog, course detail, chat room with two users,
admin + Redisboard. Keep them free of real e-mails or passwords.}}

## 🧠 Key Decisions & Lessons Learned

- **Settings as a package** (`base/local/prod`) — environments must be explicit;
  a missing setting fails fast instead of silently shipping dev defaults to prod.
- **Secrets never in Git** — `.env` + `python-decouple`; `.gitignore` guards
  `.env`, `ssl/`, `data/` and the SQLite file.
- **`DEBUG=False` changes everything** — Django stops serving static files;
  that "bald site" moment is exactly why NGINX owns static/media in production.
- **WSGI ≠ ASGI** — the chat died behind uWSGI until Daphne plus an NGINX `/ws/`
  location brought WebSockets back to life.
- **Host headers are a security boundary** — `ALLOWED_HOSTS` with subdomain
  wildcards, and `AllowedHostsOriginValidator` guarding WebSocket origins.

## 📄 License & Contact

Built by Amin Agrebi
