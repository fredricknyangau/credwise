"""
Analytics queries — uses CTEs, aggregates, and window functions.
All queries are scoped to an institution_id for data isolation.
"""

INSTITUTION_DASHBOARD = """
WITH client_stats AS (
    SELECT
        COUNT(*) AS total_clients,
        COUNT(*) FILTER (WHERE is_active) AS active_clients
    FROM users
    WHERE institution_id = $1 AND role = 'client'
),
literacy_stats AS (
    SELECT
        ROUND(AVG(progress.pct), 2) AS avg_completion_rate
    FROM (
        SELECT
            u.id AS user_id,
            CASE WHEN total.cnt = 0 THEN 0
                 ELSE ROUND((done.cnt::numeric / total.cnt) * 100, 2)
            END AS pct
        FROM users u
        CROSS JOIN (
            SELECT COUNT(*) AS cnt FROM literacy_modules WHERE is_published = TRUE
        ) total
        LEFT JOIN LATERAL (
            SELECT COUNT(DISTINCT lc.lesson_id) AS cnt
            FROM lesson_completions lc
            JOIN module_lessons ml ON ml.id = lc.lesson_id
            WHERE lc.user_id = u.id
        ) done ON TRUE
        WHERE u.institution_id = $1 AND u.role = 'client'
    ) progress
),
score_stats AS (
    SELECT ROUND(AVG(crs.score), 2) AS avg_readiness_score
    FROM credit_readiness_scores crs
    JOIN users u ON u.id = crs.user_id
    WHERE u.institution_id = $1
      AND crs.generated_at = (
          SELECT MAX(s2.generated_at) FROM credit_readiness_scores s2
          WHERE s2.user_id = crs.user_id
      )
)
SELECT
    cs.total_clients,
    cs.active_clients,
    COALESCE(ls.avg_completion_rate, 0) AS avg_literacy_completion,
    COALESCE(ss.avg_readiness_score, 0) AS avg_readiness_score
FROM client_stats cs, literacy_stats ls, score_stats ss;
"""

HIGH_RISK_CLIENTS = """
WITH latest_scores AS (
    SELECT DISTINCT ON (user_id)
        user_id, score, rating, generated_at
    FROM credit_readiness_scores
    ORDER BY user_id, generated_at DESC
)
SELECT
    u.id,
    u.full_name,
    u.phone_number,
    ls.score,
    ls.rating,
    ls.generated_at AS scored_at
FROM users u
JOIN latest_scores ls ON ls.user_id = u.id
WHERE u.institution_id = $1
  AND ls.score < 40
ORDER BY ls.score ASC
LIMIT $2;
"""

LITERACY_TREND = """
WITH daily_completions AS (
    SELECT
        DATE_TRUNC('week', lc.completed_at) AS week,
        COUNT(*) AS completions
    FROM lesson_completions lc
    JOIN users u ON u.id = lc.user_id
    WHERE u.institution_id = $1
      AND lc.completed_at >= NOW() - INTERVAL '12 weeks'
    GROUP BY DATE_TRUNC('week', lc.completed_at)
)
SELECT week, completions
FROM daily_completions
ORDER BY week ASC;
"""

MODULE_COMPLETION_RATES = """
SELECT
    m.id AS module_id,
    m.title,
    COUNT(DISTINCT u.id) AS enrolled_clients,
    COUNT(DISTINCT CASE
        WHEN lesson_done.cnt = lesson_total.cnt AND lesson_total.cnt > 0
        THEN u.id
    END) AS completed_clients,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN lesson_done.cnt = lesson_total.cnt AND lesson_total.cnt > 0
            THEN u.id
        END)::numeric
        / NULLIF(COUNT(DISTINCT u.id), 0) * 100, 2
    ) AS completion_rate
FROM literacy_modules m
CROSS JOIN (
    SELECT id FROM users WHERE institution_id = $1 AND role = 'client'
) u
LEFT JOIN LATERAL (
    SELECT COUNT(*) AS cnt FROM module_lessons WHERE module_id = m.id
) lesson_total ON TRUE
LEFT JOIN LATERAL (
    SELECT COUNT(*) AS cnt
    FROM lesson_completions lc
    JOIN module_lessons ml ON ml.id = lc.lesson_id
    WHERE ml.module_id = m.id AND lc.user_id = u.id
) lesson_done ON TRUE
WHERE m.is_published = TRUE
GROUP BY m.id, m.title
ORDER BY completion_rate DESC;
"""
