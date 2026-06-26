from sqlalchemy import Column, DateTime, Integer, String, func

from database import Base


class User(Base):
    __tablename__ = "Users" # python class User == SQL tablica z nazwa Users

    UserID = Column(Integer, primary_key=True, index=True)  # to samo co w SQL UserID INT PRIMARY KEY
    Username = Column(String(50), unique=True, nullable=False, index=True)
    Email = Column(String(100), unique=True, nullable=False, index=True)
    PasswordHash = Column(String(255), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())# SQL Server automatycznie zapisuje bieżący czas
