"""
Unit tests for pagination utilities.
"""
import pytest

from app.shared.pagination import PaginatedResponse, PaginationParams


class TestPaginationParams:
    def test_offset_calculation(self):
        p = PaginationParams(page=3, page_size=10)
        assert p.offset == 20
        assert p.limit == 10

    def test_page_1_offset_is_zero(self):
        p = PaginationParams(page=1, page_size=20)
        assert p.offset == 0

    def test_invalid_page_raises(self):
        with pytest.raises(Exception):
            PaginationParams(page=0, page_size=10)

    def test_oversized_page_raises(self):
        with pytest.raises(Exception):
            PaginationParams(page=1, page_size=200)


class TestPaginatedResponse:
    def test_builds_correctly(self):
        params = PaginationParams(page=2, page_size=5)
        items = list(range(5))
        result = PaginatedResponse.build(items, total=17, params=params)

        assert result.page == 2
        assert result.page_size == 5
        assert result.total == 17
        assert result.total_pages == 4
        assert result.has_previous is True
        assert result.has_next is True

    def test_last_page_has_no_next(self):
        params = PaginationParams(page=3, page_size=5)
        result = PaginatedResponse.build([], total=15, params=params)
        assert result.has_next is False

    def test_first_page_has_no_previous(self):
        params = PaginationParams(page=1, page_size=10)
        result = PaginatedResponse.build([], total=5, params=params)
        assert result.has_previous is False
