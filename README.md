# Calorie Balance & Diet Planner

Aplikacja do zarządzania bilansem kalorycznym i planowania diety (Etap 1 – implementacja).

## Stack
- Backend: Python 3.11+, FastAPI, SQLAlchemy, SQLite
- Frontend: HTML5 + CSS3 + Vanilla JS (serwowany przez FastAPI)

## Uruchomienie

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Następnie w przeglądarce otwórz: http://127.0.0.1:8000/

- UI: `/`
- Dokumentacja API (Swagger): `/docs`

Baza SQLite `calorie_app.db` tworzona jest automatycznie przy pierwszym uruchomieniu i zasilana przykładowymi produktami.

## Struktura
```
app/
  main.py              # FastAPI bootstrap, DI, static files
  database.py          # Engine/Session SQLAlchemy
  models/              # ORM
  schemas/             # Pydantic DTO
  repositories/        # Dostęp do danych (Repository pattern)
  services/            # Logika biznesowa (w tym Strategy dla celów)
  routers/             # Endpointy HTTP
  seed.py              # Dane startowe
static/                # Frontend
```

Etap 2 (testy) i Etap 3 (dokumentacja/test case'y) – osobne iteracje.
