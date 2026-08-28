# CCE e-Lab - Programming Practice Platform

A self-hosted web platform for Computer & Communication Engineering students to practice programming with automated evaluation, progress tracking, and skill certification. Supports up to 400 concurrent users.

---

## 🚀 Key Features

- ✅ **Interactive Code Editor** — Monaco/VS Code editor with syntax highlighting for C, C++, Java, and Python
- ✅ **Automated Evaluation** — Instant feedback via isolated Docker sandbox containers
- ✅ **Multi-Language Support** — C (GCC C11), C++ (G++ C++17), Java (OpenJDK 17), Python (CPython 3)
- ✅ **Adaptive Question Bank** — Tiered questions (Easy/Medium/Hard) with mandatory problem guarantees
- ✅ **Progress Tracking** — Real-time dashboards showing module completion, scores, and rankings
- ✅ **Skill Certification** — Automated certificate generation with QR verification for qualifying students
- ✅ **Faculty & HOD Portals** — Create modules/questions, review submissions, manage certificate approvals
- ✅ **Quizzes & Assignments** — Timed quizzes and take-home open-ended assignments
- ✅ **LeetCode Integration** — Bulk import 1,500+ public problems with test cases from local dataset
- ✅ **RAG Question Generator** — Faculty can generate custom questions offline using local DSA knowledge base (300+ problems, no LLM/GPU required)
- ✅ **Semester Auto-Advance** — Students automatically advance semesters on Jan 1 and Jul 1 via Celery beat
- ✅ **Course Access Control** — Courses unlock based on student semester (C→sem 1, Python/Java/Placement→sem 3, C++/Advanced Placement→sem 5)
- ✅ **Proctoring System** — Tab-switch detection, copy/paste blocking, fullscreen enforcement for assessment questions
- ✅ **Redis-backed Cache** — High-performance caching and session management for 400+ concurrent users

---

## 🏗️ Architecture

- **Backend:** Django 5.0 + Django REST Framework
- **Database:** PostgreSQL 15 (`elab-db`)
- **Cache & Message Broker:** Redis 7 (`elab-redis`)
- **Task Runner:** Celery Worker (`elab-worker`) with prefork pool
- **Scheduler:** Celery Beat (`elab-beat`) for periodic tasks
- **Execution Sandbox:** Custom isolated Docker container (`elab-sandbox`) supporting C, C++, Java, and Python
- **Reverse Proxy:** Nginx (`elab-nginx`) with gzip compression and keepalive
- **RAG Engine:** ChromaDB + Sentence Transformers for semantic search (local, offline)
- **Frontend:** Responsive HTML5 templates + Monaco Editor + CSS animations

---

## 📋 Prerequisites

| Software | Minimum Version | Purpose |
|----------|-----------------|---------|
| Docker Engine / Desktop | 24.0+ | Container runtime & execution sandbox |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Git | 2.30+ | Version control |
| curl | — | Health checks |

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/VazShalvin/E-Lab.git
cd E-Lab
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and set secure values:
```ini
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your.domain.com

# Database Configuration
POSTGRES_DB=elab_db
POSTGRES_USER=elab
POSTGRES_PASSWORD=change-this-password

# Redis & Celery
REDIS_URL=redis://elab-redis:6379/0
CELERY_BROKER_URL=redis://elab-redis:1
CELERY_RESULT_BACKEND=redis://elab-redis:2

# Sandbox Settings
DOCKER_SANDBOX_IMAGE=elab-sandbox
DOCKER_SANDBOX_DIR=/var/elab-sandbox

# Email (optional - for certificate notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Build Sandbox & Start Services
```bash
# 1. Build the multi-language execution sandbox image
docker build -t elab-sandbox -f sandbox/Dockerfile sandbox/

# 2. Start all services
docker compose up -d --build

# 3. Wait for services to be healthy
docker compose ps
```

### 4. Initialize Database, Static Files & Questions
```bash
# Apply database migrations
docker compose exec app python manage.py migrate

# Collect static files
docker compose exec app python manage.py collectstatic --noinput

# Seed course catalog (C, Python, Java, C++, Placement Training)
docker compose exec app python manage.py seed_courses

# Import default question bank (creates courses and modules)
docker compose exec app python manage.py import_questions

# Bulk import 1,500 LeetCode questions with test cases
docker compose exec app python manage.py import_leetcode_problems

# Enrich all questions to ~8 test cases each
docker compose exec app python manage.py enrich_test_cases

# Seed demo users (HOD, Faculty, First-Year & Second-Year Students)
docker compose exec app python manage.py seed_demo
```

### 5. Setup RAG (Required for Question Generator)
```bash
# Ingest 300+ DSA questions into ChromaDB (one-time, may take a few minutes)
docker compose exec app python manage.py rag_ingest

# Generate a sample question
docker compose exec app python manage.py generate_question --topic "two pointers" --difficulty easy
```

### 6. Access the Application
The web app is available at `http://localhost` (or your server IP):

| URL | Description |
|-----|-------------|
| `http://localhost` | Main Portal / Student Dashboard |
| `http://localhost/login/` | Authentication Page |
| `http://localhost/admin/` | Django Admin Panel |
| `http://localhost/health/` | Health Check Endpoint |

---

## 🔑 Demo & Test Accounts

Created automatically via `docker compose exec app python manage.py seed_demo`:

| Role | Username | Password | Notes |
|------|----------|----------|-------|
| **HOD** | `hod` | `hodpassword` | Certificate approval, department overview |
| **Faculty (CS)** | `faculty_cs` | `faculty123` | Module & question management |
| **Faculty (IT)** | `faculty_it` | `faculty123` | Module & question management |
| **Student (1st Yr)** | `student_fy_01` | `student123` | Semester 1 student |
| **Student (1st Yr)** | `student_fy_02` | `student123` | Semester 1 student |
| **Student (1st Yr)** | `student_fy_03` | `student123` | Semester 2 student |
| **Student (2nd Yr)** | `student_sy_01` | `student123` | Semester 3 student |
| **Student (2nd Yr)** | `student_sy_02` | `student123` | Semester 3 student |
| **Student (2nd Yr)** | `student_sy_03` | `student123` | Semester 4 student |
| **Student (3rd Yr)** | `student_ty_01` | `student123` | Semester 5 student |
| **Student (3rd Yr)** | `student_ty_02` | `student123` | Semester 6 student |

---

## 🛠️ Management Commands Reference

All commands should be executed against the `app` container:
```bash
docker compose exec app python manage.py <command> [options]
```

### Seed Demo Data
Populates faculty, students, sample submissions, and student progress records:
```bash
docker compose exec app python manage.py seed_demo
```

### Course & Curriculum Seeding
Populate the database with predefined courses, modules, and questions:
```bash
# Seed Course Catalog (C, Python, Java, C++, Placement Training, Advanced Placement Training)
docker compose exec app python manage.py seed_courses

# Import first-year questions (C Programming - default)
docker compose exec app python manage.py import_questions

# Seed Java Programming course (Lab manual & RAG generated pool)
docker compose exec -T app python manage.py shell < scripts/reseed_java.py

# Seed C++ Programming course (15 modules + LeetCode pool bypass)
docker compose exec -T app python manage.py shell < scripts/reseed_cpp.py
docker compose exec app python scripts/seed_leetcode_cpp.py

# Seed Python Programming course (15 modules + LeetCode pool bypass)
docker compose exec app python scripts/reseed_python.py
docker compose exec app python scripts/seed_leetcode_python.py

# Import second-year placement questions
docker compose exec app python manage.py seed_placement_training

# Import third-year advanced placement questions
docker compose exec app python manage.py advanced_seed_placement_training
```

### Generate Student Certificates
Scans student progress and issues certificates to eligible students:
```bash
# Generate certificates (default threshold: 80%)
docker compose exec app python manage.py generate_certificates

# Custom threshold (e.g. 60%)
docker compose exec app python manage.py generate_certificates --threshold 60

# Dry-run mode (preview eligible students without writing records)
docker compose exec app python manage.py generate_certificates --dry-run
```

### Import Questions from LeetCode
```bash
# Full bulk import (idempotent, skips existing)
docker compose exec app python manage.py import_leetcode_problems

# Test run on first 50 questions
docker compose exec app python manage.py import_leetcode_problems --limit 50

# Import a single question by slug
docker compose exec app python manage.py import_leetcode --question two-sum --module "LeetCode Problems" --difficulty easy --csv-level 1

# Import by numeric ID
docker compose exec app python manage.py import_leetcode --question 1 --module "LeetCode Problems" --difficulty easy
```

### Enrich Questions with More Test Cases
```bash
# Enrich all DSA module questions to ~8 test cases each
docker compose exec app python manage.py enrich_test_cases

# Test on first 10 questions
docker compose exec app python manage.py enrich_test_cases --limit 10

# Dry-run to preview changes
docker compose exec app python manage.py enrich_test_cases --dry-run

# Custom target (default: 8)
docker compose exec app python manage.py enrich_test_cases --target 10
```

### Clean & Format Test Cases
```bash
# Clean up LeetCode JSON test cases (removes commas and brackets to match standard competitive programming formats)
docker compose exec app python scripts/clean_testcases.py
```



### Semester Management
```bash
# Auto-advance student semesters (only acts on Jan 1 and Jul 1)
docker compose exec app python manage.py auto_advance_semesters

# Dry-run to see what would happen
docker compose exec app python manage.py auto_advance_semesters --dry-run
```

### Create Users
```bash
# Create dedicated HOD user
docker compose exec app python manage.py create_hod

# Create Django Superuser (for admin panel)
docker compose exec app python manage.py createsuperuser

# Create a student user
docker compose exec app python manage.py shell -c "
from core.models import User
u = User.objects.create_user(username='new_student', password='pass123', role='student', semester=3)
print(f'Created: {u}')
"
```

---

## 🤖 Offline Question Generator (RAG + Problem Adaptation)

Generate custom programming questions by adapting problems from the local DSA knowledge base (300+ problems from `data/DSA_Topics/`). **No internet, no LLMs, no GPUs required — everything runs locally inside Docker.**

### Setup RAG Database
```bash
# Ingest all 300+ DSA questions from the repository into ChromaDB (one-time)
docker compose exec app python manage.py rag_ingest
```

### Generate & Save a New Question
```bash
# Basic generation — generates question and saves it directly to the selected module
docker compose exec app python manage.py generate_question --topic "dynamic programming" --difficulty medium --module "Dynamic Programming"

# With custom instructions
docker compose exec app python manage.py generate_question \
  --topic "binary search" \
  --difficulty hard \
  --prompt "Focus on search on answer space problems" \
  --module "Binary Search"

# Preview only (dry run — does not save to database)
docker compose exec app python manage.py generate_question \
  --topic "graph traversal" \
  --difficulty easy \
  --dry-run

# Save output to file
docker compose exec app python manage.py generate_question \
  --topic "two pointers" \
  --difficulty easy \
  --output generated_question.json

# Save to specific module by ID
docker compose exec app python manage.py generate_question \
  --topic "hash maps" \
  --difficulty medium \
  --module-id 15
```

### Bulk Generate Questions
```bash
# From comma-separated topics
docker compose exec app python manage.py bulk_generate_questions \
  --topics "sorting,linked lists,trees" --difficulty easy --module-id 1

# From file (one topic per line)
docker compose exec app python manage.py bulk_generate_questions \
  --file /tmp/topics.txt --difficulty hard --module-id 1 --output /tmp/questions.json
```

### Available Topics
The RAG system covers 20 DSA topics with 15 problems each (300+ total):
- Array, String, Linked List, Stack, Queue
- Binary Trees, Binary Search, Heap/Priority Queue
- HashMap/Hashing, Graph (BFS/DFS)
- Dynamic Programming, Backtracking, Greedy
- Two Pointers/Sliding Window, Bit Manipulation
- Sorting Algorithms, Matrix, Trie, Recursion
- Math/Number Theory

### How It Works (Completely Offline)

1. **RAG Retrieval**: Your topic is embedded using a local Sentence Transformer model (`all-MiniLM-L6-v2`) and similar questions are retrieved from ChromaDB (300+ curated DSA problems from `data/DSA_Topics/`)

2. **Problem Adaptation**: Instead of an LLM, the system **adapts existing curated problems** to create new variants:
   - Selects the most relevant reference problems from the DSA database
   - Adjusts difficulty level (Easy/Medium/Hard) by modifying constraints and complexity
   - Generates appropriate starter code with function signatures
   - Creates 5-8 test cases including edge cases for harder difficulties
   - References the original problem in the description for transparency

3. **Validation & Save**: The adapted question (matching E-Lab's JSON schema) is validated and saved directly to the specified module with all test cases

**Performance**: ~1-2 seconds per question (no LLM, no GPU, no internet required)

---

## 📦 Docker Sandbox Execution

The custom Docker sandbox executes code submissions in fully isolated containers:

| Language | `language_id` | Toolchain | Strictness / Options |
|----------|---------------|-----------|----------------------|
| **C** | 50 | GCC (`gcc -std=c11`) | `-Wall -Wextra -Werror=return-type -Werror=main` |
| **C++** | 54 | GCC (`g++ -std=c++17`) | `-Wall -Wextra -Werror=return-type -Werror=main` |
| **Java** | 62 | OpenJDK 17 (`javac`/`java`) | Auto-detects public class name |
| **Python** | 71 | CPython 3 (`python3`) | Direct execution, syntax-checked |

### Sandbox Security Flags
- **No Network:** `--network none` — submissions cannot access external resources
- **Dropped Capabilities:** `--cap-drop ALL` — no special Linux capabilities
- **Resource Limits:** Memory (128MB), CPU (0.5 cores), PID (64 processes)
- **Ephemeral:** Fresh container per submission, cleaned up automatically
- **Base64 Encoding:** Source code and stdin are base64-encoded to prevent injection
- **tmpfs:** `/tmp` is an in-memory filesystem (50MB) for temporary files

---

## 🔧 Useful Docker & Maintenance Commands

```bash
# View live logs
docker compose logs -f app
docker compose logs -f worker
docker compose logs -f elab-db

# Restart services after configuration change
docker compose restart app worker nginx

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes all data)
docker compose down -v

# Run test suite
docker compose exec app python manage.py test

# Backup database
docker compose exec elab-db pg_dump -U elab elab_db > backup_$(date +%Y%m%d).sql

# Restore database
docker compose exec -T elab-db psql -U elab elab_db < backup_20250101.sql

# Regenerate static files
docker compose exec app python manage.py collectstatic --noinput

# Check container health
docker compose ps

# Access PostgreSQL shell
docker compose exec elab-db psql -U elab -d elab_db

# Access Redis CLI
docker compose exec elab-redis redis-cli
```

---

## 📊 Production Tuning for 400 Concurrent Users

The following settings are configured for high concurrency:

| Component | Setting | Value |
|-----------|---------|-------|
| Gunicorn | Workers | 16 (gthread) |
| Gunicorn | Threads | 4 per worker |
| Gunicorn | Timeout | 120s |
| Celery Worker | Concurrency | 16 (prefork) |
| Celery Worker | Max tasks per child | 200 |
| PostgreSQL | Max Connections | 500 |
| PostgreSQL | Shared Buffers | 256MB |
| Redis | Max Memory | 512MB |
| Nginx | Proxy Read Timeout | 120s |
| Nginx | Buffer Size | 256k |

---

## 🔍 Troubleshooting

### 1. `DisallowedHost` or `Bad Request (400)`
- Ensure `ALLOWED_HOSTS` in `.env` includes `localhost,127.0.0.1` and your server's domain/IP.
- Restart app: `docker compose restart app`.

### 2. Database Connection Error
- Ensure container `elab-db` is running: `docker compose ps`.
- Check database logs: `docker compose logs elab-db`.
- Verify database credentials in `.env` match `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`.

### 3. Static Files Not Loading / Unstyled UI
- Run static collection:
  ```bash
  docker compose exec app python manage.py collectstatic --noinput
  docker compose restart nginx
  ```

### 4. Sandbox Execution Errors
- Ensure the sandbox image is built:
  ```bash
  docker build -t elab-sandbox -f sandbox/Dockerfile sandbox/
  ```
- Verify Docker socket is accessible: `ls -la /var/run/docker.sock`
- Check sandbox directory permissions: `chmod 777 sandbox_data`

### 5. Celery Worker Not Processing Tasks
- Check worker logs: `docker compose logs -f worker`
- Verify Redis is reachable: `docker compose exec elab-redis redis-cli ping`
- Restart worker: `docker compose restart worker`

### 6. Question Generator Issues
- Ensure RAG is ingested: `docker compose exec app python manage.py rag_ingest`
- Check RAG agent logs: `docker compose logs app`

### 7. Certificate PDF Generation Fails
- Ensure `weasyprint` dependencies are installed (included in Dockerfile)
- Check media directory permissions: `chmod -R 777 media/`

---

## 📄 License

Academic use — Department of Computer & Communication Engineering (CCE), NMAM Institute of Technology, Nitte.
