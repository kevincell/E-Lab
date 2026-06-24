# CCE e-Lab — Programming with C

Continuous Practical Learning and Automated Skill Certification System for First-Year Students.

---

## Overview

CCE e-Lab is a web-based platform for first-year Computer & Communication Engineering students to practice C programming through hands-on coding exercises. The system features automated code evaluation, progress tracking, and auto-generated certificates.

## Features

- **Run & Submit code** — Test against sample cases, then submit for full evaluation
- **Automated code evaluation** — Submit C code, get instant feedback
- **Progress tracking** — Visual dashboard showing module completion
- **Auto-generated certificates** — Earned upon ≥60% completion
- **Faculty monitoring** — Track student progress and manage questions
- **Self-paced learning** — Work through 5 levels of difficulty at your own speed
- **LeetCode import** — Import questions directly from LeetCode!

## Architecture

- **Backend:** Django 5.0 + Django REST Framework
- **Database:** PostgreSQL 15
- **Cache/Queue:** Redis 7
- **Task Runner:** Celery
- **Code Execution:** Custom Docker sandbox (no external dependencies)
- **Web Server:** Nginx
- **Frontend:** HTML templates + Bootstrap

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Docker | 24.0+ | Container runtime |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Git | 2.30+ | Version control |

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/VazShalvin/E-Lab.git
cd E-Lab
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DEBUG=true
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,your-server-ip

POSTGRES_DB=elab_db
POSTGRES_USER=elab
POSTGRES_PASSWORD=change-this-password

REDIS_URL=redis://elab-redis:6379/0
CELERY_BROKER_URL=redis://elab-redis:6379/1
CELERY_RESULT_BACKEND=redis://elab-redis:6379/2

SITE_NAME=CCE e-Lab
SITE_BASE_URL=http://localhost
CERTIFICATE_THRESHOLD=60
```

### 3. Build and Start

```bash
docker build -t elab-sandbox -f sandbox/Dockerfile sandbox/
docker compose up -d --build
```

### 4. Initialize Database

```bash
docker compose exec app python manage.py migrate
docker compose exec app python manage.py collectstatic --noinput
docker compose exec app python manage.py seed_demo
```

### 5. Optional: Import LeetCode Questions
You can import questions from LeetCode using their public API!
```bash
# Import by slug
docker compose exec app python manage.py import_leetcode --question two-sum --module "LeetCode Problems" --difficulty easy --csv-level 1

# Import by ID
docker compose exec app python manage.py import_leetcode --question 1 --module "LeetCode Problems" --difficulty easy
```

### 6. Create Admin User

```bash
docker compose exec app python manage.py createsuperuser
```

### 7. Access the Application

| URL | Description |
|-----|-------------|
| `http://localhost` | Student dashboard |
| `http://localhost/admin/` | Django admin panel |
| `http://localhost/login/` | Login page |

## Development Workflow

```bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f app
docker compose logs -f worker

# Restart after code changes
docker compose restart app worker
```

## Project Structure

```
E-Lab/
├── config/              # Django settings, URLs, WSGI
├── core/                # Main application
│   ├── models.py        # User, Module, Question, Submission
│   ├── views.py         # Request handlers
│   ├── services.py      # Business logic
│   ├── sandbox.py       # Docker-based C code execution
│   └── tasks.py         # Celery background jobs
├── sandbox/             # Docker image for C compiler
│   └── Dockerfile
├── deploy/              # Nginx configuration
├── templates/           # HTML templates
├── static/              # CSS, JS
├── docker-compose.yml   # Service definitions
├── Dockerfile           # Django app image
└── requirements.txt     # Python dependencies
```

## Code Execution Sandbox

The custom Docker sandbox replaces Judge0 for C code compilation and execution:

- **Isolated containers** — Each submission runs in a fresh container
- **Resource limits** — Memory, CPU, process count restricted
- **No network access** — `--network none`
- **Capability dropping** — `--cap-drop ALL`
- **Time limits** — Enforced via `timeout` command
- **No cgroup v1 dependency** — Works on Ubuntu 22.04, 24.04, 26.04

## User Roles

| Role | Permissions |
|------|-------------|
| **Student** | Solve problems, track progress, download certificates |
| **Faculty** | Create modules/questions, view student progress |
| **Admin** | Full Django admin access, user management |

## Certification Criteria

Students receive auto-generated certificates when they:

1. Achieve **≥60% overall score**
2. Complete **all mandatory modules**
3. Maintain **participation throughout the semester**

## Modules (5 Levels)

| Level | Topics |
|-------|--------|
| Level 1 — Fundamentals | Input/Output, Variables, Operators |
| Level 2 — Control Structures | if-else, switch, loops, pattern programs |
| Level 3 — Functions & Arrays | Arrays, Functions, Searching/Sorting |
| Level 4 — Advanced Basics | Pointers, Structures, Strings, File Handling |
| Level 5 — Problem Solving | Mini coding challenges, Application-oriented problems |

## Deployment to Production Server

### Server Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 6+ cores |
| RAM | 8 GB | 16 GB |
| Storage | 100 GB SSD | 200 GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04/24.04 LTS |

### Production Setup

```bash
git clone https://github.com/VazShalvin/E-Lab.git
cd E-Lab
cp .env.example .env
# Edit .env: DEBUG=false, strong SECRET_KEY, production ALLOWED_HOSTS

docker build -t elab-sandbox -f sandbox/Dockerfile sandbox/
docker compose up -d --build

docker compose exec app python manage.py migrate
docker compose exec app python manage.py collectstatic --noinput
docker compose exec app python manage.py createsuperuser
```

## Troubleshooting

### Site shows "Bad Request (400)"

Check `ALLOWED_HOSTS` in `.env` includes your server's IP or domain.

### "Internal Error" on code submission

```bash
docker compose logs worker --tail 20
```

Ensure Docker socket is mounted in `docker-compose.yml`.

### Database connection failed

```bash
docker compose ps
docker compose logs db
```

### Static files not loading

```bash
docker compose exec app python manage.py collectstatic --noinput
docker compose restart nginx
```

## License

Academic use — NMAM Institute of Technology, Nitte.

For issues or contributions, contact the CCE department faculty coordinator.
```
