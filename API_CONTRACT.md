# 📖 API Contract — BankCore

Base URL local: `http://127.0.0.1:8000`

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <access_token>
```

---

## 🔐 Autenticación (`/auth`)

### `POST /auth/register`
Registra un nuevo usuario.

**Request:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Response `200`:**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "role": "user",
  "is_active": true
}
```

**Errores:** `400` si el email ya está registrado.

---

### `POST /auth/token`
Login. Devuelve un JWT. **Rate limit: 5 intentos por minuto por IP.**

**Request (form-data, no JSON):**
```
username: usuario@ejemplo.com
password: contraseña123
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errores:** `401` credenciales incorrectas · `403` usuario inactivo · `429` límite de intentos excedido.

---

### `GET /auth/me` 🔒
Devuelve los datos del usuario autenticado.

**Response `200`:**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "role": "user",
  "is_active": true
}
```

---

## 💰 Cuentas (`/accounts`)

### `POST /accounts/` 🔒
Crea una cuenta para el usuario autenticado. El saldo inicial siempre es `0`.

**Request:**
```json
{
  "alias": "Caja de ahorro",
  "currency": "ARS"
}
```

**Response `200`:**
```json
{
  "id": 1,
  "alias": "Caja de ahorro",
  "balance": 0.0,
  "currency": "ARS",
  "is_active": true
}
```

---

### `GET /accounts/` 🔒
Lista únicamente las cuentas del usuario autenticado.

**Response `200`:** array de cuentas (mismo formato que arriba).

---

### `GET /accounts/{account_id}` 🔒
Consulta una cuenta puntual.

**Errores:** `404` no existe · `403` la cuenta no pertenece al usuario.

---

## 💸 Transacciones (`/transactions`)

### `POST /transactions/deposit` 🔒
Simula el ingreso de dinero externo a una cuenta propia.

**Request:**
```json
{
  "account_id": 1,
  "amount": 500,
  "description": "Depósito en efectivo"
}
```

**Response `200`:** objeto `Transaction` con su movimiento asociado.

---

### `POST /transactions/transfer` 🔒
Transfiere dinero entre dos cuentas, generando doble entrada contable (débito + crédito).

**Request:**
```json
{
  "from_account_id": 1,
  "to_account_id": 2,
  "amount": 200,
  "description": "Pago de alquiler"
}
```

**Response `200`:**
```json
{
  "id": 3,
  "amount": 200.0,
  "description": "Pago de alquiler",
  "created_at": "2026-09-10T21:07:27",
  "movements": [
    { "id": 5, "amount": -200.0, "balance_after": 300.0, "account_id": 1 },
    { "id": 6, "amount": 200.0, "balance_after": 200.0, "account_id": 2 }
  ]
}
```

**Errores:** `400` cuentas iguales, o saldo insuficiente · `403` la cuenta de origen no es tuya, o alguna cuenta está inactiva · `404` cuenta inexistente.

---

## 🛡️ Administración (`/admin`) — Requiere rol `admin`

### `GET /admin/accounts`
Lista **todas** las cuentas del sistema, sin filtrar por dueño.

### `GET /admin/transactions`
Lista **todas** las transacciones del sistema.

### `PATCH /admin/accounts/{account_id}/freeze`
Congela una cuenta (`is_active = false`). Idempotente: llamarlo varias veces no genera múltiples registros de auditoría.

### `PATCH /admin/accounts/{account_id}/unfreeze`
Descongela una cuenta. Mismo comportamiento idempotente.

**Errores comunes a los 4:** `403` si el usuario autenticado no es admin · `404` cuenta inexistente (en los de freeze/unfreeze).

---

## 🔎 Notas generales

- Todos los endpoints con 🔒 requieren JWT válido; devuelven `401` si falta o expiró.
- Las validaciones de monto (`amount`) rechazan automáticamente valores `<= 0`.
- Cada operación relevante (login, depósito, transferencia, freeze/unfreeze) genera una entrada en el log de auditoría interno (no expuesto por API en esta versión).