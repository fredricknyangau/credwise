"""
Unit tests for security utilities (JWT + password hashing).
"""
import time
from uuid import uuid4

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.core.exceptions import CredentialsException


class TestPasswordHashing:
    def test_hash_and_verify_roundtrip(self):
        plain = "StrongPass1"
        hashed = hash_password(plain)
        assert hashed != plain
        assert verify_password(plain, hashed)

    def test_wrong_password_fails_verify(self):
        hashed = hash_password("CorrectPass1")
        assert not verify_password("WrongPass1", hashed)

    def test_same_password_different_hashes(self):
        """bcrypt generates unique salts per hash."""
        h1 = hash_password("SamePass1")
        h2 = hash_password("SamePass1")
        assert h1 != h2


class TestJWT:
    def test_create_and_decode_access_token(self):
        user_id = uuid4()
        token = create_access_token(subject=user_id, role="mfi_admin")
        payload = decode_access_token(token)
        assert payload["sub"] == str(user_id)
        assert payload["role"] == "mfi_admin"
        assert payload["type"] == "access"

    def test_invalid_token_raises_credentials_exception(self):
        with pytest.raises(CredentialsException):
            decode_access_token("not.a.valid.token")

    def test_institution_id_embedded_in_token(self):
        inst_id = uuid4()
        token = create_access_token(
            subject=uuid4(), role="mfi_admin", institution_id=inst_id
        )
        payload = decode_access_token(token)
        assert payload["institution_id"] == str(inst_id)


class TestRefreshToken:
    def test_raw_and_hashed_are_different(self):
        raw, hashed = generate_refresh_token()
        assert raw != hashed

    def test_deterministic_hash(self):
        raw, _ = generate_refresh_token()
        h1 = hash_refresh_token(raw)
        h2 = hash_refresh_token(raw)
        assert h1 == h2

    def test_unique_tokens(self):
        raw1, _ = generate_refresh_token()
        raw2, _ = generate_refresh_token()
        assert raw1 != raw2
