from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import MeResponse


class GoogleLoginRequest(BaseModel):
    id_token: str = Field(min_length=1)

    model_config = ConfigDict(str_strip_whitespace=True)


class AuthSessionResponse(BaseModel):
    authenticated: bool = True
    user: MeResponse

    model_config = ConfigDict(from_attributes=True)
