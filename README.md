# 🏦 BankCore

Fintech-style accounts and transactions engine built with **FastAPI** and **SQLAlchemy**. It simulates the core of a real banking system: accounts, double-entry transfers, immutable audit logging, role-based access control and brute-force protection.

It's not just another CRUD: it's designed around the kind of decisions you'd expect in real financial systems.

[![Tests](https://github.com/devzape/bankcore/actions/workflows/tests.yml/badge.svg)](https://github.com/devzape/bankcore/actions/workflows/tests.yml)

🔗 **[Try the live API (Swagger)](https://bankcore-sbdu.onrender.com/docs)**

> **Note on the demo:** it runs on a free tier, so the first request can take ~20 seconds while the service wakes up. Demo data may be reset periodically.

<!-- Add a short GIF or screenshot of Swagger here (login + transfer) -->

---

## 🛠️ Tech stack

- **FastAPI**: API framework.
- **SQLAlchemy**: ORM (SQLite).
- **Pydantic**: schema validation and typing.
- **JWT (python-jose)**: token-based authentication.
- **Passlib + bcrypt**: secure password hashing.
- **SlowAPI**: rate limiting against brute-force attacks.
- **Pytest**: automated test suite (11 tests covering auth, accounts and transfers).
- **Docker** + **GitHub Actions**: containerization and CI (tests on every push).
- **Render**: live deployment.

---

## ✨ Key features

- **JWT authentication** with roles (`user` / `admin`).
- **Multiple accounts per user**, with strict access control (IDOR protection: nobody can view or operate on someone else's accounts).
- **Double-entry transfers**: every money movement creates two records (debit/credit); a balance is never edited "by hand" without leaving a trace.
- **Row locking** on balance operations to prevent race conditions in concurrent transfers. *(Row-level locks are effective on PostgreSQL; on SQLite, writes are serialized at the database level.)*
- **Immutable audit log**: every login, deposit, transfer and administrative change is recorded with user, details and timestamp.
- **Rate limiting** on login (5 attempts/minute) to stop brute force.
- **Admin panel**: view every account and transaction in the system, freeze and unfreeze accounts.

<!--
## 🧪 Demo user
Email: [demo email]
Password: [demo password]
(Regular `user` role only. Never publish admin credentials.)
-->

---

## ⚙️ Running locally

1. **Clone the repository:**

```bash
git clone https://github.com/devzape/bankcore.git
cd bankcore
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows (PowerShell)
source venv/bin/activate       # Mac/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root with your own secret key:

```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
```

5. **Start the server:**

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive docs (Swagger) at `http://127.0.0.1:8000/docs`.

### 🐳 Running with Docker

```bash
docker build -t bankcore .
docker run -p 8000:8000 --env-file .env bankcore
```

---

## ✅ Running the tests

```bash
pytest -v
```

Tests use a separate SQLite database (`test_bankcore.db`) that is created and destroyed automatically for each test, so real data is never affected. The same suite runs on every push through **GitHub Actions**.

---

## 📂 Project structure

```
bankcore/
├── app/
│   ├── main.py              # starts the app, wires routers and middleware
│   ├── database.py          # SQLAlchemy configuration
│   ├── models/              # User, Account, Transaction, Movement, AuditLog
│   ├── schemas/             # Pydantic input/output schemas
│   ├── routers/             # auth, accounts, transactions, admin
│   └── core/                # security, JWT, dependencies, rate limiter, auditing
├── tests/                   # pytest suite
├── requirements.txt
└── API_CONTRACT.md          # detailed documentation of every endpoint
```

---

## 📖 API documentation

See [`API_CONTRACT.md`](./API_CONTRACT.md) for the full detail of each endpoint, with request/response examples.

---

## 🔐 Security decisions

- Passwords are never stored in plain text (bcrypt).
- The login error message is identical whether the email doesn't exist or the password is wrong, to prevent user enumeration.
- Every account query filters by owner **at the database level**, not in application code, which prevents data leaks caused by logic errors.
- The audit log is append-only: there is no endpoint that allows editing or deleting it.

---

## 👤 Author

**Benjamin Morales**: [GitHub](https://github.com/devzape) · [LinkedIn](https://www.linkedin.com/in/benjamin-morales-186231428/)
