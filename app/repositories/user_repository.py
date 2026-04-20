from uuid import UUID

import httpx

from app.models.base import parse_datetime
from app.models.user import User


class UserRepository:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    @staticmethod
    def _serialize_user(payload: dict) -> User:
        return User(
            id=UUID(payload["id"]),
            email=payload["email"],
            name=payload["name"],
            grade=payload.get("grade", "free"),
            role=payload.get("role", "user"),
            is_active=payload.get("is_active", True),
            google_sub=payload.get("google_sub"),
            created_at=parse_datetime(payload["created_at"]),
            updated_at=parse_datetime(payload["updated_at"]),
        )

    async def _fetch_one(self, params: dict[str, str]) -> User | None:
        response = await self.client.get(
            "/rest/v1/users",
            params={**params, "select": "*", "limit": "1"},
        )
        response.raise_for_status()
        rows = response.json()
        if not rows:
            return None
        return self._serialize_user(rows[0])

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._fetch_one({"id": f"eq.{user_id}"})

    async def get_by_email(self, email: str) -> User | None:
        return await self._fetch_one({"email": f"eq.{email}"})

    async def get_by_google_sub(self, google_sub: str) -> User | None:
        return await self._fetch_one({"google_sub": f"eq.{google_sub}"})

    async def create(
        self,
        *,
        email: str,
        name: str,
        google_sub: str | None = None,
        grade: str = "free",
        role: str = "user",
    ) -> User:
        response = await self.client.post(
            "/rest/v1/users",
            headers={"Prefer": "return=representation"},
            json={
                "email": email,
                "name": name,
                "google_sub": google_sub,
                "grade": grade,
                "role": role,
                "is_active": True,
            },
        )
        response.raise_for_status()
        rows = response.json()
        return self._serialize_user(rows[0])

    async def update_google_account(
        self,
        user: User,
        *,
        google_sub: str,
        name: str,
    ) -> User:
        response = await self.client.patch(
            "/rest/v1/users",
            params={"id": f"eq.{user.id}", "select": "*"},
            headers={"Prefer": "return=representation"},
            json={
                "google_sub": google_sub,
                "name": name,
            },
        )
        response.raise_for_status()
        rows = response.json()
        return self._serialize_user(rows[0])
