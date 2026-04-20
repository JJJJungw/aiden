from uuid import UUID

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

UserGrade = Literal["free", "pro"]


class MeResponse(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str
    grade: UserGrade

    model_config = ConfigDict(from_attributes=True)
