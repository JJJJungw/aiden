import httpx
import logging
from fastapi import HTTPException, status

from app.core.security import GoogleTokenError, create_access_token, verify_google_id_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import GoogleLoginRequest

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.user_repository = UserRepository(client)

    async def login_with_google(self, payload: GoogleLoginRequest) -> tuple[User, str]:
        try:
            google_payload = verify_google_id_token(payload.id_token)
        except GoogleTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        google_sub = str(google_payload["sub"])
        email = str(google_payload["email"]).lower()
        name = str(google_payload.get("name") or email.split("@")[0])

        try:
            user = await self.user_repository.get_by_google_sub(google_sub)
            if user is None:
                user = await self.user_repository.get_by_email(email)
                if user is None:
                    user = await self.user_repository.create(
                        email=email,
                        name=name,
                        google_sub=google_sub,
                    )
                else:
                    user = await self.user_repository.update_google_account(
                        user,
                        google_sub=google_sub,
                        name=name,
                    )
        except httpx.HTTPStatusError as exc:
            response_text = exc.response.text
            logger.exception(
                "Supabase user sync failed: status=%s body=%s",
                exc.response.status_code,
                response_text,
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "message": "Supabase user sync failed",
                    "supabase_status": exc.response.status_code,
                    "supabase_body": response_text,
                },
            ) from exc
        except httpx.HTTPError as exc:
            logger.exception("Supabase connection failed")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "message": "Supabase connection failed",
                    "error": str(exc),
                },
            ) from exc

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )
        return user, access_token
