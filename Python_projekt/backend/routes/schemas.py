# sprawdzanie i formatowanie danych
from datetime import datetime

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class NoteResponse(BaseModel):
    note_id: int
    user_id: int
    note_text: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class MoodEntryResponse(BaseModel):
    mood_id: int
    user_id: int
    mood: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

