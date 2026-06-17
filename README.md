# MoodTracker
Mood tracker - web aplikacja służąca do poprawy nastroju, gdzie użytkownik rejestruje się,  wybiera nastrój, otrzymuje żart, ocenia go, pisze notatki, przegląda historię nastrojów i notatek

Użytkownik może wybrać swój nastrój, a aplikacja pobiera odpowiedni żart z zewnętrznego API (https://v2.jokeapi.dev/?ref=freepublicapis.com) i wyświetla go na stronie. Każdy żart może zostać oceniony jako zabawny lub niezabawny.
Dodatkowo aplikacja umożliwia tworzenie i przechowywanie notatek oraz śledzenie historii nastrojów. Wszystkie dane użytkownika są zapisywane w bazie danych.

Funkcjonalności:
Rejestracja i logowanie użytkowników
Wybór aktualnego nastroju
Pobieranie żartów z zewnętrznego API
Ocenianie żartów
Tworzenie notatek
Historia nastrojów użytkownika

Technologie:
FastAPI
SQL Server Management Studio (19)
SQLAlchemy
HTML, CSS, JavaScript
JokeAPI
