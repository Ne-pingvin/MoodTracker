from fastapi import FastAPI
from routes import auth, jokes, notes

from database import Base, engine

#Inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)

#Stworzenie aplikacji FastAPI
app = FastAPI(title="Mood Tracker API")

#podlacza autoryzacje
app.include_router(auth.router)
app.include_router(jokes.router)
app.include_router(notes.router)

#test
@app.get("/")
def root():
    return {"message": "MoodJokes API"}





