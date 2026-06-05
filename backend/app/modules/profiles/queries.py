"""
Raw SQL for client financial profiles.
"""

UPSERT_PROFILE = """
INSERT INTO client_financial_profiles (
    id, user_id, monthly_income, savings_frequency,
    business_type, years_in_business, cooperative_member,
    existing_loans, updated_at
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
ON CONFLICT (user_id) DO UPDATE SET
    monthly_income      = EXCLUDED.monthly_income,
    savings_frequency   = EXCLUDED.savings_frequency,
    business_type       = EXCLUDED.business_type,
    years_in_business   = EXCLUDED.years_in_business,
    cooperative_member  = EXCLUDED.cooperative_member,
    existing_loans      = EXCLUDED.existing_loans,
    updated_at          = NOW()
RETURNING
    id, user_id, monthly_income, savings_frequency,
    business_type, years_in_business, cooperative_member,
    existing_loans, updated_at;
"""

GET_PROFILE_BY_USER = """
SELECT
    id, user_id, monthly_income, savings_frequency,
    business_type, years_in_business, cooperative_member,
    existing_loans, updated_at
FROM client_financial_profiles
WHERE user_id = $1;
"""
