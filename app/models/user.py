from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    name: str
    grade: str
    role: str
    is_active: bool
    google_sub: str | None
    created_at: datetime
    updated_at: datetime

#ㅁㄴㅇㅁㄴㅇㅁㄴㅇ