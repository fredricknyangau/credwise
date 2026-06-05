"""
Raw SQL for credit readiness scores.
"""

GET_SCORE_BY_USER = """
SELECT
    id, user_id, score, rating,
    literacy_weight, savings_weight, stability_weight,
    repayment_weight, cooperative_weight,
    factors, generated_at
FROM credit_readiness_scores
WHERE user_id = $1
ORDER BY generated_at DESC
LIMIT 1;
"""

GET_SCORE_HISTORY = """
SELECT
    id, user_id, score, rating, factors, generated_at
FROM credit_readiness_scores
WHERE user_id = $1
ORDER BY generated_at DESC
LIMIT $2 OFFSET $3;
"""

INSERT_SCORE = """
INSERT INTO credit_readiness_scores (
    id, user_id, score, rating,
    literacy_weight, savings_weight, stability_weight,
    repayment_weight, cooperative_weight, factors
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb)
RETURNING
    id, user_id, score, rating,
    literacy_weight, savings_weight, stability_weight,
    repayment_weight, cooperative_weight,
    factors, generated_at;
"""

# Data needed by the scoring engine — aggregated from several tables
GET_SCORING_INPUTS = """
WITH literacy_data AS (
    SELECT
        COUNT(DISTINCT ml.id) AS total_modules,
        COUNT(DISTINCT CASE WHEN prog.pct = 100 THEN ml.id END) AS completed_modules
    FROM literacy_modules ml
    LEFT JOIN (
        SELECT ml2.module_id,
               CASE WHEN total.cnt = 0 THEN 0
                    ELSE ROUND((done.cnt::numeric / total.cnt) * 100, 2)
               END AS pct
        FROM (
            SELECT module_id, COUNT(*) AS cnt FROM module_lessons GROUP BY module_id
        ) total
        LEFT JOIN (
            SELECT ml3.module_id, COUNT(*) AS cnt
            FROM lesson_completions lc
            JOIN module_lessons ml3 ON ml3.id = lc.lesson_id
            WHERE lc.user_id = $1
            GROUP BY ml3.module_id
        ) done USING (module_id)
        LEFT JOIN module_lessons ml2 USING (module_id)
    ) prog ON prog.module_id = ml.id
    WHERE ml.is_published = TRUE
),
quiz_data AS (
    SELECT COALESCE(AVG(qa.score), 0) AS avg_quiz_score
    FROM quiz_attempts qa
    WHERE qa.user_id = $1
),
profile_data AS (
    SELECT
        monthly_income,
        savings_frequency,
        business_type,
        years_in_business,
        cooperative_member,
        existing_loans
    FROM client_financial_profiles
    WHERE user_id = $1
    LIMIT 1
)
SELECT
    ld.total_modules,
    ld.completed_modules,
    qd.avg_quiz_score,
    pd.monthly_income,
    pd.savings_frequency,
    pd.business_type,
    pd.years_in_business,
    pd.cooperative_member,
    pd.existing_loans
FROM literacy_data ld, quiz_data qd
LEFT JOIN profile_data pd ON TRUE;
"""
