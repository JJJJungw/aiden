from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_supabase_admin
from app.core.security import create_expired_access_token
from app.models.user import User
from app.schemas.auth import AuthSessionResponse, GoogleLoginRequest
from app.schemas.user import MeResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def set_auth_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )


def set_expired_auth_cookie(response: Response) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=create_expired_access_token(),
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
        max_age=0,
        expires=0,
        path="/",
    )


@router.post("/google", response_model=AuthSessionResponse, status_code=status.HTTP_200_OK)
async def login_with_google(
    payload: GoogleLoginRequest,
    response: Response,
    client: Annotated[httpx.AsyncClient, Depends(get_supabase_admin)],
) -> AuthSessionResponse:
    user, access_token = await AuthService(client).login_with_google(payload)
    set_auth_cookie(response, access_token)
    return AuthSessionResponse(
        authenticated=True,
        user=MeResponse(
            id=user.id,
            email=user.email,
            nickname=user.name,
            grade=user.grade,
        ),
    )


@router.get("/me", response_model=MeResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        nickname=current_user.name,
        grade=current_user.grade,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.status_code = status.HTTP_204_NO_CONTENT
    set_expired_auth_cookie(response)
