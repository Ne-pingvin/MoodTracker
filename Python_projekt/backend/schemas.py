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


class JokeRequest(BaseModel):
	mood: str = Field(default="neutral", min_length=2, max_length=20)


class JokeResponse(BaseModel):
	joke: str
	mood: str
	category: str | None = None


class JokeRatingCreate(BaseModel):
	user_id: int
	joke_text: str = Field(min_length=1)
	rating: bool
	mood_at_moment: str | None = Field(default=None, max_length=20)


class JokeRatingResponse(BaseModel):
	rating_id: int
	user_id: int
	joke_text: str
	rating: bool
	mood_at_moment: str | None = None
	created_at: datetime | None = None

class NoteCreate(BaseModel):
    note_text: str = Field(min_length=1)

class NoteUpdate(BaseModel):
    note_text: str = Field(min_length=1)

class NoteResponse(BaseModel):
    note_id: int
    user_id: int
    note_text: str
    created_at: datetime | None = None

class MoodEntryCreate(BaseModel):
    mood: str = Field(min_length=2, max_length=20)

class MoodEntryResponse(BaseModel):
    mood_id: int
    user_id: int
    mood: str
    created_at: datetime | None = None