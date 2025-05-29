
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_habit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_response = await ac.post("/users/", json={"name": "Test User", "email": "testuser@example.com"})
        user_id = user_response.json()["id"]
        habit_data = {"name": "Drink water", "description": "Drink 8 glasses", "user_id": user_id}
        response = await ac.post("/habits/", json=habit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Drink water"
    assert data["description"] == "Drink 8 glasses"
    assert data["user_id"] == user_id

@pytest.mark.asyncio
async def test_get_habit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_response = await ac.post("/users/", json={"name": "Another User", "email": "another@example.com"})
        user_id = user_response.json()["id"]
        habit_response = await ac.post("/habits/", json={
            "name": "Read book",
            "description": "Read 20 pages",
            "user_id": user_id
        })
        habit_id = habit_response.json()["id"]
        response = await ac.get(f"/habits/{habit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Read book"
    assert data["description"] == "Read 20 pages"
    assert data["user_id"] == user_id
