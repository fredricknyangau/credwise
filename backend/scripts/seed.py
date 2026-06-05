#!/usr/bin/env python3
"""
Seed script — creates demo data for development and testing.

Run with: python scripts/seed.py

Creates:
  - 1 Platform Admin user
  - 2 MFI institutions with their admins
  - 5 clients per institution
  - 3 literacy modules with lessons
  - Quizzes for each module
  - Financial profiles and credit scores for clients
"""
from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone

import asyncpg

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.security import hash_password

DB_URL = os.getenv("DATABASE_URL", "postgresql://credwise:credwise@localhost:5432/credwise")
# Strip asyncpg driver prefix for asyncpg direct use
DB_URL = DB_URL.replace("postgresql+asyncpg://", "postgresql://")


async def seed() -> None:
    conn = await asyncpg.connect(DB_URL)
    try:
        await _seed_all(conn)
        print("✅ Seed complete")
    finally:
        await conn.close()


async def _seed_all(conn: asyncpg.Connection) -> None:
    # ── Institutions ──────────────────────────────────────────────────────────
    inst1_id = uuid.uuid4()
    inst2_id = uuid.uuid4()

    await conn.execute("""
        INSERT INTO mfi_institutions (id, name, email, phone, location)
        VALUES
            ($1, 'Kilimo MFI', 'admin@kilimomfi.co.ke', '+254700111222', 'Nakuru, Kenya'),
            ($2, 'Umoja Savings', 'admin@umojasavings.co.ke', '+254700333444', 'Kisumu, Kenya')
        ON CONFLICT DO NOTHING;
    """, inst1_id, inst2_id)
    print("  ✓ Institutions created")

    # ── Platform admin ─────────────────────────────────────────────────────────
    await conn.execute("""
        INSERT INTO users (id, institution_id, role, full_name, phone_number, password_hash)
        VALUES ($1, NULL, 'platform_admin', 'Platform Admin', '+254700000001', $2)
        ON CONFLICT DO NOTHING;
    """, uuid.uuid4(), hash_password("Admin1234"))
    print("  ✓ Platform admin created (phone: +254700000001, password: Admin1234)")

    # ── MFI Admins ─────────────────────────────────────────────────────────────
    admin1_id = uuid.uuid4()
    admin2_id = uuid.uuid4()
    await conn.execute("""
        INSERT INTO users (id, institution_id, role, full_name, phone_number, password_hash)
        VALUES
            ($1, $3, 'mfi_admin', 'Peter Kamau', '+254711100001', $5),
            ($2, $4, 'mfi_admin', 'Grace Akinyi', '+254711100002', $5)
        ON CONFLICT DO NOTHING;
    """, admin1_id, admin2_id, inst1_id, inst2_id, hash_password("MfiAdmin1"))
    print("  ✓ MFI admins created")

    # ── Clients ───────────────────────────────────────────────────────────────
    client_ids: list[uuid.UUID] = []
    for i in range(1, 11):
        inst_id = inst1_id if i <= 5 else inst2_id
        phone = f"+254722{i:06d}"
        c_id = uuid.uuid4()
        client_ids.append(c_id)
        await conn.execute("""
            INSERT INTO users (id, institution_id, role, full_name, phone_number, password_hash)
            VALUES ($1, $2, 'client', $3, $4, $5)
            ON CONFLICT DO NOTHING;
        """, c_id, inst_id, f"Client User {i}", phone, hash_password("Client123"))
    print(f"  ✓ {len(client_ids)} clients created")

    # ── Literacy Modules ───────────────────────────────────────────────────────
    modules: list[tuple[uuid.UUID, str]] = [
        (uuid.uuid4(), "Introduction to Savings"),
        (uuid.uuid4(), "Managing Your Business Cash Flow"),
        (uuid.uuid4(), "Understanding Credit"),
    ]
    for mod_id, title in modules:
        await conn.execute("""
            INSERT INTO literacy_modules (id, title, description, difficulty_level, estimated_minutes, is_published)
            VALUES ($1, $2, $3, 'beginner', 30, TRUE)
            ON CONFLICT DO NOTHING;
        """, mod_id, title, f"Learn about {title.lower()} in simple, practical terms.")

        # 3 lessons per module
        for order in range(1, 4):
            lesson_id = uuid.uuid4()
            await conn.execute("""
                INSERT INTO module_lessons (id, module_id, title, content, lesson_order)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT DO NOTHING;
            """,
            lesson_id, mod_id,
            f"{title} — Part {order}",
            f"This is the content for lesson {order} of '{title}'. "
            "In this lesson we cover essential financial concepts relevant to the Kenyan informal sector.",
            order)

        # Quiz per module
        quiz_id = uuid.uuid4()
        await conn.execute("""
            INSERT INTO quizzes (id, module_id, title)
            VALUES ($1, $2, $3)
            ON CONFLICT DO NOTHING;
        """, quiz_id, mod_id, f"Quiz: {title}")

        # 3 questions per quiz
        import json
        for q_num in range(1, 4):
            await conn.execute("""
                INSERT INTO quiz_questions (id, quiz_id, question, options, correct_answer)
                VALUES ($1, $2, $3, $4::jsonb, $5)
                ON CONFLICT DO NOTHING;
            """,
            uuid.uuid4(), quiz_id,
            f"Question {q_num} about {title}?",
            json.dumps(["Option A", "Option B", "Correct Option", "Option D"]),
            "Correct Option")

    print(f"  ✓ {len(modules)} modules with lessons and quizzes created")

    # ── Financial Profiles ────────────────────────────────────────────────────
    profiles = [
        ("daily", "farming", 3.5, True, 0, 25000),
        ("weekly", "trading", 2.0, False, 1, 18000),
        ("monthly", "services", 1.0, True, 2, 10000),
        ("bi_weekly", "trading", 4.0, True, 0, 35000),
        ("irregular", "none", 0.5, False, 3, 5000),
    ]
    for i, c_id in enumerate(client_ids[:5]):
        freq, btype, yrs, coop, loans, income = profiles[i]
        await conn.execute("""
            INSERT INTO client_financial_profiles
                (id, user_id, monthly_income, savings_frequency, business_type,
                 years_in_business, cooperative_member, existing_loans)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (user_id) DO NOTHING;
        """, uuid.uuid4(), c_id, income, freq, btype, yrs, coop, loans)
    print("  ✓ Financial profiles created for first 5 clients")


if __name__ == "__main__":
    asyncio.run(seed())
