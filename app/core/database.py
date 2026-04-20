from collections.abc import AsyncGenerator

import httpx

from app.core.config import settings


class SupabaseAdminClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.supabase_url,
            timeout=10.0,
            headers={
                "apikey": settings.supabase_service_key,
                "Authorization": f"Bearer {settings.supabase_service_key}",
                "Content-Type": "application/json",
            },
        )

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def aclose(self) -> None:
        await self._client.aclose()


supabase_admin = SupabaseAdminClient()


async def get_supabase_admin() -> AsyncGenerator[httpx.AsyncClient, None]:
    yield supabase_admin.client
