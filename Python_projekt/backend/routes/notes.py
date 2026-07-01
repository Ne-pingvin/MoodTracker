from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Note, MoodEntry, User
from schemas import NoteCreate, NoteUpdate, NoteResponse, MoodEntryCreate, MoodEntryResponse

router = APIRouter(prefix="/history", tags=["notes and moods"])

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#  SQLAlchemy do Pydantic
def note_to_response(note: Note) -> NoteResponse:
    return NoteResponse(
        note_id=note.NoteID,
        user_id=note.UserID,
        note_text=note.NoteText,
        created_at=note.CreatedAt
    )

def mood_to_response(mood_entry: MoodEntry) -> MoodEntryResponse:
    return MoodEntryResponse(
        mood_id=mood_entry.MoodID,
        user_id=mood_entry.UserID,
        mood=mood_entry.Mood,
        created_at=mood_entry.CreatedAt
    )

# ---------------- NOTES ----------------

@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note_data: NoteCreate, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    new_note = Note(
        UserID=user.UserID,
        NoteText=note_data.note_text
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return note_to_response(new_note)


@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteUpdate, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    note = db.query(Note).filter(
        Note.NoteID == note_id,
        Note.UserID == user.UserID
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.NoteText = note_data.note_text
    db.commit()
    db.refresh(note)

    return note_to_response(note)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    note = db.query(Note).filter(
        Note.NoteID == note_id,
        Note.UserID == user.UserID
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()


@router.get("/notes", response_model=List[NoteResponse])
def get_notes(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    notes = db.query(Note).filter(Note.UserID == user.UserID).order_by(Note.CreatedAt.desc()).all()
    
    return [note_to_response(note) for note in notes]


# ---------------- MOODS ----------------

@router.post("/moods", response_model=MoodEntryResponse, status_code=status.HTTP_201_CREATED)
def create_mood(mood_data: MoodEntryCreate, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    mood_entry = MoodEntry(
        UserID=user.UserID,
        Mood=mood_data.mood
    )

    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)

    return mood_to_response(mood_entry)


@router.get("/moods", response_model=List[MoodEntryResponse])
def get_moods(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    moods = db.query(MoodEntry).filter(MoodEntry.UserID == user.UserID).order_by(MoodEntry.CreatedAt.desc()).all()
    
    return [mood_to_response(mood) for mood in moods]