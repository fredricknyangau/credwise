"""
Raw SQL queries for the auth module.

Rules:
- Only positional parameters ($1, $2, …) — no dynamic string concatenation.
- Every query is a named constant for easy referencing and testing.
"""

# ─── MFI Registration ────────────────────────────────────────────────────────

INSERT_INSTITUTION = """
INSERT INTO mfi_institutions (id, name, email, phone, location)
VALUES ($1, $2, $3, $4, $5)
RETURNING id, name, email, phone, location, created_at;
"""

INSERT_MFI_ADMIN_USER = """
INSERT INTO users (
    id, institution_id, role, full_name, phone_number, password_hash, is_active
)
VALUES ($1, $2, 'mfi_admin', $3, $4, $5, TRUE)
RETURNING id, institution_id, role, full_name, phone_number, is_active, created_at;
"""

INSERT_LEARNER_USER = """
INSERT INTO users (
    id, role, full_name, phone_number, password_hash, is_active
)
VALUES ($1, 'client', $2, $3, $4, TRUE)
RETURNING id, institution_id, role, full_name, phone_number, is_active, created_at;
"""

# ─── Login ────────────────────────────────────────────────────────────────────

FIND_USER_BY_PHONE = """
SELECT
    id,
    institution_id,
    role,
    full_name,
    phone_number,
    password_hash,
    is_active,
    created_at
FROM users
WHERE phone_number = $1
LIMIT 1;
"""

FIND_USER_BY_ID = """
SELECT
    id,
    institution_id,
    role,
    full_name,
    phone_number,
    password_hash,
    is_active,
    created_at
FROM users
WHERE id = $1
LIMIT 1;
"""

# ─── Refresh Tokens ───────────────────────────────────────────────────────────

INSERT_REFRESH_TOKEN = """
INSERT INTO refresh_tokens (id, user_id, token_hash, expires_at)
VALUES ($1, $2, $3, $4);
"""

FIND_REFRESH_TOKEN = """
SELECT id, user_id, token_hash, expires_at, revoked
FROM refresh_tokens
WHERE token_hash = $1
LIMIT 1;
"""

REVOKE_REFRESH_TOKEN = """
UPDATE refresh_tokens
SET revoked = TRUE
WHERE token_hash = $1;
"""

REVOKE_ALL_USER_TOKENS = """
UPDATE refresh_tokens
SET revoked = TRUE
WHERE user_id = $1 AND revoked = FALSE;
"""

# ─── Institution existence checks ─────────────────────────────────────────────

FIND_INSTITUTION_BY_EMAIL = """
SELECT id FROM mfi_institutions WHERE email = $1 LIMIT 1;
"""

FIND_USER_BY_PHONE_EXISTS = """
SELECT id FROM users WHERE phone_number = $1 LIMIT 1;
"""
