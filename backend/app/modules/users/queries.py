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
    u.id, u.institution_id, u.role, u.full_name, u.phone_number,
    u.is_active, u.created_at,
    COALESCE(ls.score, 0) AS readiness_score,
    COALESCE(ls.rating, 'Low Readiness') AS category,
    COALESCE(p.business_type, 'N/A') AS business_type,
    COALESCE(p.cooperative_member, FALSE) AS cooperative_member,
    COALESCE(lc.pct, 0) AS literacy_progress
FROM users u
LEFT JOIN (
    SELECT DISTINCT ON (user_id) user_id, score, rating
    FROM credit_readiness_scores
    ORDER BY user_id, generated_at DESC
) ls ON ls.user_id = u.id
LEFT JOIN client_financial_profiles p ON p.user_id = u.id
LEFT JOIN (
    SELECT
        u2.id AS user_id,
        CASE WHEN total.cnt = 0 THEN 0
             ELSE ROUND((done.cnt::numeric / total.cnt) * 100, 2)
        END AS pct
    FROM users u2
    CROSS JOIN (
        SELECT COUNT(*) AS cnt FROM literacy_modules WHERE is_published = TRUE
    ) total
    LEFT JOIN LATERAL (
        SELECT COUNT(DISTINCT lc2.lesson_id) AS cnt
        FROM lesson_completions lc2
        JOIN module_lessons ml ON ml.id = lc2.lesson_id
        WHERE lc2.user_id = u2.id
    ) done ON TRUE
    WHERE u2.role = 'client'
) lc ON lc.user_id = u.id
WHERE u.institution_id = $1 AND u.role = 'client'
ORDER BY u.created_at DESC
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
