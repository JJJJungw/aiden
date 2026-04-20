from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import jwt
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()


class TokenDecodeError(Exception):
    pass


class GoogleTokenError(Exception):
    pass


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: UUID, email: str, role: str) -> str:
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_expired_access_token() -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": "logged-out",
        "email": "logged-out@example.com",
        "role": "guest",
        "type": "access",
        "iat": now - timedelta(minutes=10),
        "exp": now - timedelta(minutes=5),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except ExpiredSignatureError as exc:
        raise TokenDecodeError("Token has expired") from exc
    except InvalidTokenError as exc:
        raise TokenDecodeError("Invalid token") from exc

    if payload.get("type") != "access":
        raise TokenDecodeError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise TokenDecodeError("Token subject is missing")

    return payload


def verify_google_id_token(token: str) -> dict[str, Any]:
    try:
        payload = id_token.verify_oauth2_token(
            token,
            Request(),
            settings.google_client_id,
        )
    except Exception as exc:
        raise GoogleTokenError("Invalid Google token") from exc

    if payload.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
        raise GoogleTokenError("Invalid Google issuer")

    if not payload.get("sub") or not payload.get("email"):
        raise GoogleTokenError("Google account information is missing")

    if payload.get("email_verified") is not True:
        raise GoogleTokenError("Google email is not verified")

    return payload
