# CCE e-Lab

A self-hosted programming lab platform for college labs. It provides student coding practice, automated judging through Judge0 CE, faculty question management, progress tracking, and verifiable completion certificates.

## Stack

- Django + Django REST Framework
- PostgreSQL
- Redis + Celery
- Judge0 CE
- Nginx reverse proxy
- Docker Compose deployment

## Quick Start On Server

```bash
git clone <your-repo-url> /opt/elab
cd /opt/elab
cp .env.example .env
# edit .env secrets, hosts, and passwords
docker compose up -d --build
docker compose exec app python manage.py migrate
docker compose exec app python manage.py collectstatic --noinput
docker compose exec app python manage.py seed_demo
docker compose exec app python manage.py createsuperuser
```

Open `http://SERVER_IP/`.

## Default Demo Data

After `seed_demo`, the app creates:

- Admin: username `admin`, password `admin12345` (email: `admin@elab.local`)
- Faculty: username `faculty`, password `faculty12345` (email: `faculty@elab.local`)
- Student: username `student`, password `student12345` (email: `student@elab.local`)

Change or remove these users before real deployment.

## Production Notes

- Use strong values in `.env`.
- Keep Judge0, Redis, and Postgres ports private to the Docker network when exposed internet access is not required.
- Put the server on the college LAN with a static IP or assign DNS such as `elab.cce.nmam.in`.
- For HTTPS, terminate TLS at Nginx or at a campus reverse proxy.
