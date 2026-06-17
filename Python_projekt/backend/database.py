from sqlalchemy import create_engine #tworzy obiekt polaczenia SQLAlchemy z baza danych
from sqlalchemy.orm import declarative_base #zwraca klase 'Base' dla klas, ktore SQLAlchemy będzie używać jako modelu bazy danych
from sqlalchemy.orm import sessionmaker #polaczenia do zapytan

# Ustawienia polaczenia
SERVER = "localhost"
DATABASE = "MoodTracker"

#polaczenie SQLAlchemy z SQL Server przez pyodbc
connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

#zarzadza polaczeniami do bazy
engine = create_engine(
    connection_string,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#opis tabel za posrednictwem modeli ORM
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()