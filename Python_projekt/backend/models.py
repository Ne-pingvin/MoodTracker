from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func

from database import Base


class User(Base):
    __tablename__ = "Users" # python class User == SQL tablica z nazwa Users

    UserID = Column(Integer, primary_key=True, index=True)  # to samo co w SQL UserID INT PRIMARY KEY
    Username = Column(String(50), unique=True, nullable=False, index=True)
    Email = Column(String(100), unique=True, nullable=False, index=True)
    PasswordHash = Column(String(255), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())# SQL Server automatycznie zapisuje bieżący czas

class JokeRating(Base):
    __tablename__ = "JokeRatings"

    RatingID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("Users.UserID", ondelete="CASCADE"), nullable=False, index=True)
    JokeText = Column(String, nullable=False)
    Rating = Column(Boolean, nullable=False)
    MoodAtMoment = Column(String(20), nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())

class MoodEntry(Base):
    __tablename__ = "MoodEntries"

    MoodID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("Users.UserID", ondelete="CASCADE"), nullable=False, index=True)
    Mood = Column(String(20), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())

class Note(Base):
    __tablename__ = "Notes"

    NoteID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("Users.UserID", ondelete="CASCADE"), nullable=False, index=True)
    NoteText = Column(String, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())