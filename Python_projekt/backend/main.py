from fastapi import FastAPI

from database import Base, engine
from routes import auth, jokes

#Inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)

#Stworzenie aplikacji FastAPI
app = FastAPI(title="Mood Tracker API")

#podlacza autoryzacje
app.include_router(auth.router)
app.include_router(jokes.router)

#test
@app.get("/")
def root():
    return {"message": "MoodJokes API"}





