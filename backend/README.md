# Credwise Platform Backend

Production-grade, modular, and surveillance-free financial literacy and ethical credit-readiness backend platform. Specifically tailored to microfinance institutions (MFIs) and unbanked users in East Africa (farmers, informal workers, small traders, savings groups).

## 🚀 Key Architectural & Tech Choices
- **FastAPI**: Asynchronous web framework for high-concurrency capability.
- **Raw SQL + asyncpg**: Absolute avoidance of ORMs (SQLAlchemy ORM, Tortoise, etc.) for direct control, query optimization, connection pooling, and explicit transaction management (`BEGIN` / `COMMIT` / `ROLLBACK`).
- **Alembic Migrations**: Relational schema migrations managed purely through SQL files.
- **Pydantic v2**: High-performance request/response data validation and sanitization.
- **JWT Authentication & RBAC**: Fully-featured JWT tokens with role-based access control (Platform Admin, MFI Admin, Client).
- **Dockerized**: Containerized PostgreSQL database, migration runners, API nodes, and seed triggers.

---

## 🏗️ Folder Structure (Modular Monolith)
The backend is organized as a Feature-Based Modular Monolith:
```
backend/
├── app/
│   ├── core/                  # Settings, Security, Database Pool, Exceptions
│   ├── modules/               # Domain-driven features
│   │   ├── auth/              # Registration, Login, Token Rotation
│   │   ├── users/             # Client management & activation
│   │   ├── institutions/      # MFI settings & status
│   │   ├── literacy/          # Lessons, Modules, Progress tracking
│   │   ├── quizzes/           # Quiz building & grading engine
│   │   ├── credit_scoring/    # Ethical Credit Readiness Engine
│   │   └── analytics/         # MFI dashboard metrics
│   ├── shared/                # Pagination, responses, validation
│   └── main.py                # App factory
├── migrations/                # Alembic SQL-based migrations
├── tests/                     # Pytest suite (Unit & Integration)
├── scripts/                   # Seeding utility
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

---

## 🧮 Ethical Credit Readiness Scoring Engine
Credwise rejects surveillance-based metrics (smartphone metadata, contact scraping, GPS tracking, and social media activity) in favor of ethical financial indicators.

Our engine scores users from `0` to `100` and assigns ratings (`High`, `Moderate`, `Developing`, or `Low` Readiness) across 5 dimensions:
1. **Financial Literacy (30% weight)**: Combines module completion rate (60%) and quiz score performance (40%).
2. **Savings Consistency (25% weight)**: Maps frequency (e.g., daily savings score = 100, weekly = 85, bi-weekly = 70, monthly = 50, irregular = 20).
3. **Business Stability (20% weight)**: Blends business age (longevity up to 5 years) and monthly income level.
4. **Repayment Behaviour (15% weight)**: Monitors current outstanding loan volume (zero existing loans = 100, 1 active loan = 80, multiple active loans penalize the score).
5. **Cooperative Participation (10% weight)**: Adds 100 points for savings cooperative/group membership.

All factors influencing the final score are output transparently to the user.

---

## 🛠️ Setup & Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.12 (optional, if running tests locally)

### Running the Stack
Launch the database, migrations, and API server:
```bash
docker compose up --build
```

### Seeding Demo Data
To populate the database with test data (1 platform admin, 2 MFIs, 2 MFI admins, 10 clients, 3 literacy modules, quizzes, questions, profiles, and score input templates), run:
```bash
docker compose --profile seed up
```

### Environment Variables
Environment settings are stored in `.env`. Copy `.env.example` to start:
```bash
cp .env.example .env
```

---

## 🧪 Testing with Pytest
Run the test suite using a dedicated test database:
```bash
# Set up a local test database and run:
PYTHONPATH=. pytest tests/
```
The test suite utilizes PostgreSQL transaction rollbacks per test to ensure full test isolation and database consistency.

---

## 🔍 Troubleshooting Port Conflicts & Stale Volumes

### 1. Port 5432 or 8000 is Already in Use
If Docker Compose fails because port `5432` or `8000` is already in use, you can free them up on your host machine:

- **Free up PostgreSQL Port 5432:**
  ```bash
  sudo systemctl stop postgresql
  # Or find and kill the process:
  sudo fuser -k 5432/tcp
  ```

- **Free up Web Server Port 8000:**
  ```bash
  # Find and kill any process running on port 8000:
  sudo fuser -k 8000/tcp
  ```

### 2. Password Authentication Failed for User "credwise"
If the migration container exits with `InvalidPasswordError`, it is caused by a leftover PostgreSQL volume from a previous deployment or another database.
Reset the volumes using:
```bash
docker compose down -v
docker compose up -d
```
