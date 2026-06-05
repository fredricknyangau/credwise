"""
Ethical credit scoring engine.

Design principles:
- No surveillance signals (GPS, contacts, social media, device fingerprinting).
- Fully transparent — every factor is explicitly labelled in the response.
- Modular weights — can be configured per-MFI in the future.
- Scores range 0–100 and map to human-readable ratings.

Scoring dimensions (weights must sum to 1.0):
  literacy     0.30  — module completion + quiz performance
  savings      0.25  — frequency and consistency
  stability    0.20  — business age and income level
  repayment    0.15  — existing loan behaviour (0 = clean, 1 active = small penalty)
  cooperative  0.10  — savings group / cooperative membership
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Weights — sum to 1.0. Can be made configurable per MFI later.
# ---------------------------------------------------------------------------

WEIGHTS: dict[str, float] = {
    "literacy": 0.30,
    "savings": 0.25,
    "stability": 0.20,
    "repayment": 0.15,
    "cooperative": 0.10,
}

RATING_THRESHOLDS: list[tuple[float, str]] = [
    (80, "High Readiness"),
    (60, "Moderate Readiness"),
    (40, "Developing Readiness"),
    (0, "Low Readiness"),
]


@dataclass
class ScoringResult:
    score: float
    rating: str
    literacy_weight: float
    savings_weight: float
    stability_weight: float
    repayment_weight: float
    cooperative_weight: float
    factors: list[str] = field(default_factory=list)


def _get_rating(score: float) -> str:
    for threshold, label in RATING_THRESHOLDS:
        if score >= threshold:
            return label
    return "Low Readiness"


def _literacy_score(
    total_modules: int,
    completed_modules: int,
    avg_quiz_score: float,
) -> tuple[float, list[str]]:
    """
    Blends module completion rate (60%) with average quiz score (40%).
    Returns a 0–100 sub-score and a list of human-readable factor strings.
    """
    factors: list[str] = []

    completion_rate = (
        (completed_modules / total_modules) if total_modules > 0 else 0.0
    )
    sub = (completion_rate * 60) + (avg_quiz_score * 0.4)
    sub = min(sub, 100.0)

    if completion_rate >= 1.0:
        factors.append("Completed all literacy modules")
    elif completion_rate >= 0.5:
        factors.append(f"Completed {completed_modules}/{total_modules} literacy modules")
    else:
        factors.append("Literacy progress below 50%")

    if avg_quiz_score >= 80:
        factors.append("Strong quiz performance")
    elif avg_quiz_score >= 50:
        factors.append("Moderate quiz performance")

    return sub, factors


def _savings_score(savings_frequency: str | None) -> tuple[float, list[str]]:
    """Maps savings frequency to a 0–100 score."""
    freq_map = {
        "daily": 100,
        "weekly": 85,
        "bi_weekly": 70,
        "monthly": 50,
        "irregular": 20,
    }
    score = freq_map.get(savings_frequency or "irregular", 20)
    factors: list[str] = []
    if score >= 70:
        factors.append("Strong savings consistency")
    elif score >= 50:
        factors.append("Regular savings behaviour")
    else:
        factors.append("Irregular savings pattern — room to improve")
    return float(score), factors


def _stability_score(
    years_in_business: float,
    monthly_income: float,
) -> tuple[float, list[str]]:
    """
    Business longevity (up to 60 pts) + income level (up to 40 pts).
    Thresholds calibrated for the Kenyan informal sector context.
    """
    factors: list[str] = []

    # Longevity — cap at 5 years for max score
    longevity_score = min(years_in_business / 5.0, 1.0) * 60
    if years_in_business >= 3:
        factors.append("Stable business history (3+ years)")
    elif years_in_business >= 1:
        factors.append("Growing business (1–3 years)")

    # Income — KES thresholds for informal sector
    if monthly_income >= 50_000:
        income_score = 40
        factors.append("Above-average monthly income")
    elif monthly_income >= 20_000:
        income_score = 30
        factors.append("Moderate monthly income")
    elif monthly_income >= 5_000:
        income_score = 20
    else:
        income_score = 10
        factors.append("Low income — potential vulnerability")

    return longevity_score + income_score, factors


def _repayment_score(existing_loans: int) -> tuple[float, list[str]]:
    """
    Penalises excessive existing debt. 0 loans = full score.
    We reward having 1 active loan (demonstrates credit access + repayment),
    then penalise further accumulation.
    """
    factors: list[str] = []
    if existing_loans == 0:
        factors.append("No existing loan obligations")
        return 100.0, factors
    elif existing_loans == 1:
        factors.append("Managing 1 active loan responsibly")
        return 80.0, factors
    elif existing_loans == 2:
        return 55.0, factors
    else:
        factors.append("Multiple active loans — high debt load")
        return max(0.0, 100 - (existing_loans * 20)), factors


def _cooperative_score(cooperative_member: bool | None) -> tuple[float, list[str]]:
    if cooperative_member:
        return 100.0, ["Member of a savings cooperative or group"]
    return 0.0, ["Not a cooperative or savings group member"]


def compute_score(raw: dict[str, Any]) -> ScoringResult:
    """
    Entry point for the scoring engine.

    Args:
        raw: dict from GET_SCORING_INPUTS query

    Returns:
        ScoringResult with component scores, weighted total, rating, and factors.
    """
    total_modules = int(raw.get("total_modules") or 0)
    completed_modules = int(raw.get("completed_modules") or 0)
    avg_quiz_score = float(raw.get("avg_quiz_score") or 0)
    monthly_income = float(raw.get("monthly_income") or 0)
    savings_frequency = raw.get("savings_frequency")
    years_in_business = float(raw.get("years_in_business") or 0)
    cooperative_member = raw.get("cooperative_member")
    existing_loans = int(raw.get("existing_loans") or 0)

    lit_sub, lit_factors = _literacy_score(
        total_modules, completed_modules, avg_quiz_score
    )
    sav_sub, sav_factors = _savings_score(savings_frequency)
    stab_sub, stab_factors = _stability_score(years_in_business, monthly_income)
    rep_sub, rep_factors = _repayment_score(existing_loans)
    coop_sub, coop_factors = _cooperative_score(cooperative_member)

    weighted_score = round(
        lit_sub * WEIGHTS["literacy"]
        + sav_sub * WEIGHTS["savings"]
        + stab_sub * WEIGHTS["stability"]
        + rep_sub * WEIGHTS["repayment"]
        + coop_sub * WEIGHTS["cooperative"],
        2,
    )

    all_factors = lit_factors + sav_factors + stab_factors + rep_factors + coop_factors

    return ScoringResult(
        score=weighted_score,
        rating=_get_rating(weighted_score),
        literacy_weight=round(lit_sub * WEIGHTS["literacy"], 2),
        savings_weight=round(sav_sub * WEIGHTS["savings"], 2),
        stability_weight=round(stab_sub * WEIGHTS["stability"], 2),
        repayment_weight=round(rep_sub * WEIGHTS["repayment"], 2),
        cooperative_weight=round(coop_sub * WEIGHTS["cooperative"], 2),
        factors=all_factors,
    )
