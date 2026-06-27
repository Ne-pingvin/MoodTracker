from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import JokeRating
from schemas import JokeRatingCreate, JokeRatingResponse, JokeResponse
from services.joke_api import JokeAPIError, fetch_joke


router = APIRouter(prefix="/jokes", tags=["jokes"])


def rating_to_response(rating: JokeRating) -> JokeRatingResponse:
	return JokeRatingResponse(
		rating_id=rating.RatingID,
		user_id=rating.UserID,
		joke_text=rating.JokeText,
		rating=rating.Rating,
		mood_at_moment=rating.MoodAtMoment,
		created_at=rating.CreatedAt,
	)


@router.get("", response_model=JokeResponse)
def get_joke(mood: str = "neutral"):
	try:
		joke_data = fetch_joke(mood)
	except JokeAPIError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

	return JokeResponse(**joke_data)


@router.post("/rate", response_model=JokeRatingResponse, status_code=status.HTTP_201_CREATED)
def rate_joke(rating_data: JokeRatingCreate, db: Session = Depends(get_db)):
	rating = JokeRating(
		UserID=rating_data.user_id,
		JokeText=rating_data.joke_text,
		Rating=rating_data.rating,
		MoodAtMoment=rating_data.mood_at_moment,
	)

	db.add(rating)
	db.commit()
	db.refresh(rating)
	return rating_to_response(rating)
