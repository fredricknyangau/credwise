"""
Raw SQL for user management.
"""

GET_USER_BY_ID = """
SELECT
    id, institution_id, role, full_name, phone_number,
    is_active, created_at
FROM users
WHERE id = $1;
"""

LIST_USERS_BY_INSTITUTION = """
SELECT
    id, institution_id, role, full_name, phone_number,
    is_active, created_at
FROM users
WHERE institution_id = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;
"""

COUNT_USERS_BY_INSTITUTION = """
SELECT COUNT(*) FROM users WHERE institution_id = $1;
"""

INSERT_CLIENT_USER = """
INSERT INTO users (
    id, institution_id, role, full_name, phone_number, password_hash, is_active
)
VALUES ($1, $2, 'client', $3, $4, $5, TRUE)
RETURNING id, institution_id, role, full_name, phone_number, is_active, created_at;
"""

UPDATE_USER_STATUS = """
UPDATE users SET is_active = $2 WHERE id = $1
RETURNING id, is_active;
"""

CHECK_PHONE_EXISTS = """
SELECT id FROM users WHERE phone_number = $1 AND id != $2 LIMIT 1;
"""
