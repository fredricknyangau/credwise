"""
Unit tests for the ethical credit scoring engine.
No database required — pure function tests.
"""
import pytest

from app.modules.credit_scoring.engine import (
    _cooperative_score,
    _literacy_score,
    _repayment_score,
    _savings_score,
    _stability_score,
    compute_score,
)


class TestLiteracyScore:
    def test_full_completion_with_strong_quiz(self):
        score, factors = _literacy_score(5, 5, 90)
        assert score == pytest.approx(96.0, abs=1)
        assert any("Completed all literacy modules" in f for f in factors)
        assert any("Strong quiz performance" in f for f in factors)

    def test_zero_modules(self):
        score, _ = _literacy_score(0, 0, 0)
        assert score == 0.0

    def test_partial_completion(self):
        score, factors = _literacy_score(4, 2, 60)
        assert 0 < score < 100
        assert any("2/4" in f for f in factors)


class TestSavingsScore:
    def test_daily_is_highest(self):
        daily, _ = _savings_score("daily")
        weekly, _ = _savings_score("weekly")
        assert daily > weekly

    def test_irregular_is_lowest(self):
        score, factors = _savings_score("irregular")
        assert score == 20.0
        assert any("Irregular" in f for f in factors)

    def test_none_defaults_to_irregular(self):
        score, _ = _savings_score(None)
        assert score == 20.0


class TestStabilityScore:
    def test_high_income_long_business(self):
        score, factors = _stability_score(5, 60_000)
        assert score == pytest.approx(100.0)
        assert any("Stable business" in f for f in factors)

    def test_zero_income_new_business(self):
        score, _ = _stability_score(0, 0)
        assert score < 30


class TestRepaymentScore:
    def test_no_loans_is_perfect(self):
        score, factors = _repayment_score(0)
        assert score == 100.0
        assert any("No existing loan" in f for f in factors)

    def test_one_loan_is_positive(self):
        score, _ = _repayment_score(1)
        assert score == 80.0

    def test_many_loans_penalised(self):
        score, factors = _repayment_score(5)
        assert score == 0.0
        assert any("Multiple" in f for f in factors)


class TestCooperativeScore:
    def test_member_gets_full_score(self):
        score, factors = _cooperative_score(True)
        assert score == 100.0
        assert any("cooperative" in f.lower() for f in factors)

    def test_non_member_gets_zero(self):
        score, _ = _cooperative_score(False)
        assert score == 0.0


class TestComputeScore:
    def _full_profile(self) -> dict:
        return {
            "total_modules": 5,
            "completed_modules": 5,
            "avg_quiz_score": 90,
            "monthly_income": 60_000,
            "savings_frequency": "daily",
            "years_in_business": 5,
            "cooperative_member": True,
            "existing_loans": 0,
        }

    def test_ideal_client_scores_high(self):
        result = compute_score(self._full_profile())
        assert result.score >= 85
        assert result.rating == "High Readiness"
        assert len(result.factors) > 0

    def test_empty_profile_scores_low(self):
        result = compute_score({})
        assert result.score < 40
        assert result.rating in ("Low Readiness", "Developing Readiness")

    def test_weights_sum_correctly(self):
        result = compute_score(self._full_profile())
        total = (
            result.literacy_weight
            + result.savings_weight
            + result.stability_weight
            + result.repayment_weight
            + result.cooperative_weight
        )
        assert total == pytest.approx(result.score, abs=0.1)
