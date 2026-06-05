"""
Integration tests for authentication endpoints.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient


MFI_PAYLOAD = {
    "institution_name": "Equity MFI Kenya",
    "institution_email": "admin@equitymfi.co.ke",
    "institution_phone": "+254712345678",
    "institution_location": "Nairobi, Kenya",
    "admin_full_name": "Jane Wanjiku",
    "admin_phone": "+254798765432",
    "admin_password": "SecurePass1",
}


@pytest.mark.asyncio
async def test_register_mfi_returns_201(client: AsyncClient, conn):
    response = await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["institution_name"] == MFI_PAYLOAD["institution_name"]
    assert data["data"]["role"] == "mfi_admin"


@pytest.mark.asyncio
async def test_register_mfi_duplicate_email_returns_409(client: AsyncClient, conn):
    await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)
    response = await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_with_valid_credentials(client: AsyncClient, conn):
    # First register
    await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)

    # Then login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": MFI_PAYLOAD["admin_phone"],
            "password": MFI_PAYLOAD["admin_password"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_wrong_password_returns_401(client: AsyncClient, conn):
    await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)

    response = await client.post(
        "/api/v1/auth/login",
        json={"phone_number": MFI_PAYLOAD["admin_phone"], "password": "WrongPass1"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_phone_returns_401(client: AsyncClient, conn):
    response = await client.post(
        "/api/v1/auth/login",
        json={"phone_number": "+254700000000", "password": "SomePass1"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_token_refresh_flow(client: AsyncClient, conn):
    await client.post("/api/v1/auth/register-mfi", json=MFI_PAYLOAD)

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": MFI_PAYLOAD["admin_phone"],
            "password": MFI_PAYLOAD["admin_password"],
        },
    )
    refresh_token = login.json()["data"]["refresh_token"]

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh.status_code == 200
    assert "access_token" in refresh.json()["data"]


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
