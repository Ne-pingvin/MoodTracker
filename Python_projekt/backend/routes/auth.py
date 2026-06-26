from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserLogin, UserRegister, UserResponse

# tworzenie routera, wszystkie sciezki wewnątrz pliku będą zaczynały się od /auth
router = APIRouter(prefix="/auth", tags=["auth"])

# funkcja przeksztalca obiekt SQLAlchemy User w odpowiedz UserResponse, nie zwracajac hasla
def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.UserID,
        username=user.Username,
        email=user.Email,
        created_at=user.CreatedAt,
    )

# wyszukiwanie uzytkownika wedlug username
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.Username == username).first()

# wyszukiwanie uzytkownika poprzez e-mail
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.Email == email).first()

# endpoint rejestracji
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username is already taken")
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    # tworzenie obiektu User
    user = User(
        Username=user_data.username,
        Email=user_data.email,
        PasswordHash=user_data.password,
    )

    # zapisywanie do bazy danych
    db.add(user)
    # INSERT INTO Users
    db.commit()
    db.refresh(user)
    return user_to_response(user)


@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, credentials.username)
    if user is None or user.PasswordHash != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return user_to_response(user)
