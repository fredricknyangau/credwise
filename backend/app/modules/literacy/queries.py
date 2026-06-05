"""
Raw SQL for literacy modules and lessons.
"""

# ─── Modules ─────────────────────────────────────────────────────────────────

LIST_MODULES = """
SELECT id, title, description, difficulty_level, estimated_minutes, is_published, created_at
FROM literacy_modules
WHERE is_published = TRUE
ORDER BY created_at ASC
LIMIT $1 OFFSET $2;
"""

COUNT_MODULES = """
SELECT COUNT(*) FROM literacy_modules WHERE is_published = TRUE;
"""

GET_MODULE_BY_ID = """
SELECT id, title, description, difficulty_level, estimated_minutes, is_published, created_at
FROM literacy_modules
WHERE id = $1;
"""

INSERT_MODULE = """
INSERT INTO literacy_modules (id, title, description, difficulty_level, estimated_minutes)
VALUES ($1, $2, $3, $4, $5)
RETURNING id, title, description, difficulty_level, estimated_minutes, is_published, created_at;
"""

PUBLISH_MODULE = """
UPDATE literacy_modules SET is_published = $2 WHERE id = $1
RETURNING id, is_published;
"""

# ─── Lessons ─────────────────────────────────────────────────────────────────

LIST_LESSONS_BY_MODULE = """
SELECT id, module_id, title, content, lesson_order, created_at
FROM module_lessons
WHERE module_id = $1
ORDER BY lesson_order ASC;
"""

GET_LESSON_BY_ID = """
SELECT id, module_id, title, content, lesson_order, created_at
FROM module_lessons
WHERE id = $1;
"""

INSERT_LESSON = """
INSERT INTO module_lessons (id, module_id, title, content, lesson_order)
VALUES ($1, $2, $3, $4, $5)
RETURNING id, module_id, title, content, lesson_order, created_at;
"""

# ─── Progress Tracking ────────────────────────────────────────────────────────

UPSERT_LESSON_COMPLETION = """
INSERT INTO lesson_completions (id, user_id, lesson_id, completed_at)
VALUES ($1, $2, $3, NOW())
ON CONFLICT (user_id, lesson_id) DO NOTHING
RETURNING id;
"""

GET_MODULE_PROGRESS = """
WITH module_lesson_count AS (
    SELECT COUNT(*) AS total
    FROM module_lessons
    WHERE module_id = $1
),
completed_count AS (
    SELECT COUNT(*) AS completed
    FROM lesson_completions lc
    JOIN module_lessons ml ON ml.id = lc.lesson_id
    WHERE ml.module_id = $1 AND lc.user_id = $2
)
SELECT
    $1::uuid AS module_id,
    $2::uuid AS user_id,
    mlc.total,
    cc.completed,
    CASE WHEN mlc.total = 0 THEN 0
         ELSE ROUND((cc.completed::numeric / mlc.total) * 100, 2)
    END AS percentage
FROM module_lesson_count mlc, completed_count cc;
"""

GET_ALL_MODULES_PROGRESS = """
WITH lesson_counts AS (
    SELECT module_id, COUNT(*) AS total_lessons
    FROM module_lessons
    GROUP BY module_id
),
user_completions AS (
    SELECT ml.module_id, COUNT(*) AS completed
    FROM lesson_completions lc
    JOIN module_lessons ml ON ml.id = lc.lesson_id
    WHERE lc.user_id = $1
    GROUP BY ml.module_id
)
SELECT
    m.id AS module_id,
    m.title,
    COALESCE(lc.total_lessons, 0) AS total_lessons,
    COALESCE(uc.completed, 0) AS completed,
    CASE WHEN COALESCE(lc.total_lessons, 0) = 0 THEN 0
         ELSE ROUND((COALESCE(uc.completed, 0)::numeric / lc.total_lessons) * 100, 2)
    END AS percentage
FROM literacy_modules m
LEFT JOIN lesson_counts lc ON lc.module_id = m.id
LEFT JOIN user_completions uc ON uc.module_id = m.id
WHERE m.is_published = TRUE
ORDER BY m.created_at ASC;
"""
