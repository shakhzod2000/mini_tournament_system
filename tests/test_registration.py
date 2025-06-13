from httpx import AsyncClient
from app.main import app

import pytest

@pytest.mark.asyncio
async def test_create_and_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tournaments", json={
            "name": "Weekend Cup",
            "max_players": 1,
            "start_at": "2025-06-01T15:00:00Z"
        })
        assert response.status_code == 200
        tid = response.json()["id"]

        response = await ac.post(f"/tournaments/{tid}/register", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        assert response.status_code == 200

        # Test duplicate
        response = await ac.post(f"/tournaments/{tid}/register", json={
            "name": "John Duplicate",
            "email": "john@example.com"
        })
        assert response.status_code == 400
