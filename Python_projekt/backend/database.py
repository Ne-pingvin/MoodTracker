import os

from sqlalchemy import create_engine #tworzy obiekt polaczenia SQLAlchemy z baza danych
from sqlalchemy.orm import declarative_base #zwraca klase 'Base' dla klas, ktore SQLAlchemy będzie używać jako modelu bazy danych
from sqlalchemy.orm import sessionmaker #polaczenia do zapytan

# # Ustawienia polaczenia
SERVER = "localhost"
DATABASE = "MoodTracker"

#polaczenie SQLAlchemy z SQL Server przez pyodbc
connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)



# połączenie z bazą danych na Azure SQL Server

# Postawiłem na szybko bazę na Azure aby nie trzeba było instalować SQL Servera lokalnie i aby można było przerzucać historię miedzy urządzeniami.
# Nie chcę wyłączać firewalla dla całej bazy, wiec trzeba będzie dodać każdorazowo adressy ip, albo zmienić na inną metodę autoryzacji. Będzie można to zmienić w przyszłości na ten moment zostawiam kod zakomentowany.

# SERVER = os.getenv("DB_SERVER", "localhost")
# DATABASE = os.getenv("DB_NAME", "MoodTracker")
# USERNAME = os.getenv("DB_USER")
# PASSWORD = os.getenv("DB_PASSWORD")

# if USERNAME and PASSWORD:
#     connection_string = (
#         f"mssql+pyodbc://{(USERNAME)}:{(PASSWORD)}@{SERVER}/{DATABASE}"
#         "?driver=ODBC+Driver+17+for+SQL+Server"
#         "&Encrypt=yes"
#         "&TrustServerCertificate=no"
#     )
# else:
#     raise RuntimeError(
#         "Missing database credentials. Set DB_USER and DB_PASSWORD environment variables."
#     )



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