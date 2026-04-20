from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_anon_key: str = Field(alias="SUPABASE_ANON_KEY")
    supabase_service_key: str = Field(alias="SUPABASE_SERVICE_KEY")
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        default=60,
    )
    google_client_id: str = Field(alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(alias="GOOGLE_CLIENT_SECRET")
    auth_cookie_name: str = Field(alias="AUTH_COOKIE_NAME", default="access_token")
    cookie_secure: bool = Field(alias="COOKIE_SECURE", default=False)
    cookie_samesite: str = Field(alias="COOKIE_SAMESITE", default="lax")
    cookie_domain: str | None = Field(alias="COOKIE_DOMAIN", default=None)
    frontend_origin: str = Field(alias="FRONTEND_ORIGIN", default="http://127.0.0.1:8000")
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
