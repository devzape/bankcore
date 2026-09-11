[![Tests](https://github.com/devzape/bankcore/actions/workflows/tests.yml/badge.svg)](https://github.com/devzape/bankcore/actions/workflows/tests.yml)
# 🏦 BankCore

Motor de cuentas y transacciones estilo fintech, construido con **FastAPI** y **SQLAlchemy**. Simula el corazón de un sistema bancario real: cuentas, transferencias con doble entrada contable, auditoría inmutable, control de acceso por roles, y protección contra fuerza bruta.

No es un CRUD más — está pensado para reflejar decisiones de diseño que se esperan en sistemas financieros reales.

---

## 🛠️ Tecnologías utilizadas

- **FastAPI**: framework para construir la API.
- **SQLAlchemy**: ORM para persistencia en SQLite.
- **Pydantic**: validación y tipado de esquemas.
- **JWT (python-jose)**: autenticación basada en tokens.
- **Passlib + bcrypt**: hasheo seguro de contraseñas.
- **SlowAPI**: rate limiting contra ataques de fuerza bruta.
- **Pytest**: suite de tests automatizados (11 tests, cubriendo auth, cuentas y transferencias).

---

## ✨ Funcionalidades principales

- **Autenticación JWT** con roles (`user` / `admin`).
- **Cuentas múltiples por usuario**, con control de acceso estricto (protección contra IDOR: nadie puede ver ni operar cuentas ajenas).
- **Transferencias con doble entrada contable**: cada movimiento de dinero genera dos registros (débito/crédito), nunca se edita un saldo "a mano" sin dejar rastro.
- **Bloqueo de filas (`row locking`)** en operaciones de saldo, para prevenir condiciones de carrera en transferencias simultáneas.
- **Log de auditoría inmutable**: cada login, depósito, transferencia y cambio administrativo queda registrado con usuario, detalle y timestamp.
- **Rate limiting** en el login (5 intentos/minuto) para frenar fuerza bruta.
- **Panel de administración**: ver todas las cuentas/transacciones del sistema, congelar y descongelar cuentas.

---

## ⚙️ Cómo correr el proyecto localmente

1. **Clonar el repositorio:**

```bash
git clone https://github.com/devzape/bankcore.git
cd bankcore
```

2. **Crear y activar un entorno virtual:**

```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows (PowerShell)
source venv/bin/activate       # Mac/Linux
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Crear el archivo `.env`** en la raíz, con una clave secreta propia:

```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
```

5. **Levantar el servidor:**

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, con documentación interactiva (Swagger) en `http://127.0.0.1:8000/docs`.

---

## ✅ Correr los tests

```bash
pytest -v
```

Los tests usan una base de datos SQLite separada (`test_bankcore.db`), que se crea y destruye automáticamente en cada test — no afectan los datos de la base real.

---

## 📂 Estructura del proyecto

```
bankcore/
├── app/
│   ├── main.py              # arranca la app, conecta routers y middleware
│   ├── database.py          # configuración de SQLAlchemy
│   ├── models/               # User, Account, Transaction, Movement, AuditLog
│   ├── schemas/               # esquemas Pydantic de entrada/salida
│   ├── routers/               # auth, accounts, transactions, admin
│   └── core/                  # seguridad, JWT, dependencias, rate limiter, auditoría
├── tests/                     # suite de pytest
├── requirements.txt
└── API_CONTRACT.md            # documentación detallada de todos los endpoints
```

---

## 📖 Documentación de la API

Ver [`API_CONTRACT.md`](./API_CONTRACT.md) para el detalle completo de cada endpoint, con ejemplos de request/response.

---

## 🔐 Decisiones de seguridad destacadas

- Las contraseñas nunca se guardan en texto plano (bcrypt).
- El mensaje de error de login es idéntico si el email no existe o si la contraseña es incorrecta, para evitar enumeración de usuarios.
- Toda consulta de cuentas filtra por dueño **en la base de datos**, no en el código — evita fugas de datos por errores de lógica.
- El log de auditoría es append-only: no hay ningún endpoint que permita editrarlo o borrarlo.
