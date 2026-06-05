"""
Initial schema migration — creates all tables.

Tables:
    mfi_institutions, users, refresh_tokens,
    literacy_modules, module_lessons, lesson_completions,
    quizzes, quiz_questions, quiz_attempts,
    client_financial_profiles, credit_readiness_scores
"""
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    """)

    # ── MFI Institutions ──────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE mfi_institutions (
            id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            name        VARCHAR(200) NOT NULL,
            email       VARCHAR(254) NOT NULL UNIQUE,
            phone       VARCHAR(20)  NOT NULL,
            location    VARCHAR(300) NOT NULL,
            is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_institutions_email ON mfi_institutions(email);")

    # ── Users ─────────────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE users (
            id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            institution_id  UUID        REFERENCES mfi_institutions(id) ON DELETE SET NULL,
            role            VARCHAR(20) NOT NULL CHECK (role IN ('platform_admin','mfi_admin','client')),
            full_name       VARCHAR(200) NOT NULL,
            phone_number    VARCHAR(20)  NOT NULL UNIQUE,
            password_hash   TEXT        NOT NULL,
            is_active       BOOLEAN     NOT NULL DEFAULT TRUE,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_users_institution ON users(institution_id);")
    op.execute("CREATE INDEX idx_users_phone ON users(phone_number);")
    op.execute("CREATE INDEX idx_users_role ON users(role);")

    # ── Refresh Tokens ────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE refresh_tokens (
            id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id     UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token_hash  TEXT        NOT NULL UNIQUE,
            expires_at  TIMESTAMPTZ NOT NULL,
            revoked     BOOLEAN     NOT NULL DEFAULT FALSE,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);")
    op.execute("CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);")

    # ── Literacy Modules ──────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE literacy_modules (
            id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            title               VARCHAR(200) NOT NULL,
            description         TEXT        NOT NULL,
            difficulty_level    VARCHAR(20) NOT NULL CHECK (difficulty_level IN ('beginner','intermediate','advanced')),
            estimated_minutes   INTEGER     NOT NULL CHECK (estimated_minutes > 0),
            is_published        BOOLEAN     NOT NULL DEFAULT FALSE,
            created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)

    # ── Module Lessons ────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE module_lessons (
            id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            module_id       UUID        NOT NULL REFERENCES literacy_modules(id) ON DELETE CASCADE,
            title           VARCHAR(200) NOT NULL,
            content         TEXT        NOT NULL,
            lesson_order    INTEGER     NOT NULL CHECK (lesson_order > 0),
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            UNIQUE (module_id, lesson_order)
        );
    """)
    op.execute("CREATE INDEX idx_lessons_module ON module_lessons(module_id);")

    # ── Lesson Completions ────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE lesson_completions (
            id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            lesson_id       UUID        NOT NULL REFERENCES module_lessons(id) ON DELETE CASCADE,
            completed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            UNIQUE (user_id, lesson_id)
        );
    """)
    op.execute("CREATE INDEX idx_completions_user ON lesson_completions(user_id);")
    op.execute("CREATE INDEX idx_completions_lesson ON lesson_completions(lesson_id);")

    # ── Quizzes ───────────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE quizzes (
            id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            module_id   UUID        NOT NULL REFERENCES literacy_modules(id) ON DELETE CASCADE UNIQUE,
            title       VARCHAR(200) NOT NULL,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)

    # ── Quiz Questions ────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE quiz_questions (
            id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            quiz_id         UUID        NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
            question        TEXT        NOT NULL,
            options         JSONB       NOT NULL,
            correct_answer  TEXT        NOT NULL,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_questions_quiz ON quiz_questions(quiz_id);")

    # ── Quiz Attempts ─────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE quiz_attempts (
            id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            quiz_id         UUID        NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
            score           NUMERIC(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
            answers         JSONB       NOT NULL DEFAULT '{}',
            completed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_attempts_user ON quiz_attempts(user_id);")
    op.execute("CREATE INDEX idx_attempts_quiz ON quiz_attempts(quiz_id);")

    # ── Client Financial Profiles ─────────────────────────────────────────────
    op.execute("""
        CREATE TABLE client_financial_profiles (
            id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id             UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
            monthly_income      NUMERIC(12,2) NOT NULL CHECK (monthly_income >= 0),
            savings_frequency   VARCHAR(20) NOT NULL,
            business_type       VARCHAR(50) NOT NULL,
            years_in_business   NUMERIC(4,1) NOT NULL CHECK (years_in_business >= 0),
            cooperative_member  BOOLEAN     NOT NULL DEFAULT FALSE,
            existing_loans      INTEGER     NOT NULL CHECK (existing_loans >= 0),
            updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_profiles_user ON client_financial_profiles(user_id);")

    # ── Credit Readiness Scores ───────────────────────────────────────────────
    op.execute("""
        CREATE TABLE credit_readiness_scores (
            id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id             UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            score               NUMERIC(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
            rating              VARCHAR(30) NOT NULL,
            literacy_weight     NUMERIC(5,2) NOT NULL,
            savings_weight      NUMERIC(5,2) NOT NULL,
            stability_weight    NUMERIC(5,2) NOT NULL,
            repayment_weight    NUMERIC(5,2) NOT NULL,
            cooperative_weight  NUMERIC(5,2) NOT NULL,
            factors             JSONB       NOT NULL DEFAULT '[]',
            generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    op.execute("CREATE INDEX idx_scores_user ON credit_readiness_scores(user_id);")
    op.execute("CREATE INDEX idx_scores_generated ON credit_readiness_scores(generated_at);")


def downgrade() -> None:
    tables = [
        "credit_readiness_scores",
        "client_financial_profiles",
        "quiz_attempts",
        "quiz_questions",
        "quizzes",
        "lesson_completions",
        "module_lessons",
        "literacy_modules",
        "refresh_tokens",
        "users",
        "mfi_institutions",
    ]
    for table in tables:
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
