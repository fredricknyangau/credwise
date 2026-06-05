"""
Raw SQL for institution management.
"""

GET_INSTITUTION_BY_ID = """
SELECT id, name, email, phone, location, is_active, created_at
FROM mfi_institutions
WHERE id = $1;
"""

LIST_INSTITUTIONS = """
SELECT id, name, email, phone, location, is_active, created_at
FROM mfi_institutions
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;
"""

COUNT_INSTITUTIONS = """
SELECT COUNT(*) FROM mfi_institutions;
"""

UPDATE_INSTITUTION_STATUS = """
UPDATE mfi_institutions SET is_active = $2
WHERE id = $1
RETURNING id, name, is_active;
"""

GET_INSTITUTION_SUMMARY = """
SELECT
    i.id,
    i.name,
    i.email,
    i.location,
    i.is_active,
    i.created_at,
    COUNT(DISTINCT u.id) FILTER (WHERE u.role = 'client') AS client_count,
    COUNT(DISTINCT u.id) FILTER (WHERE u.role = 'mfi_admin') AS admin_count
FROM mfi_institutions i
LEFT JOIN users u ON u.institution_id = i.id
WHERE i.id = $1
GROUP BY i.id, i.name, i.email, i.location, i.is_active, i.created_at;
"""
