# Skyport

# Instalacja FastAPI i serwera
py -m pip install fastapi uvicorn[standard]

# Instalacja silnika szablonów i bazy danych
py -m pip install jinja2 psycopg2

# Instalacja zabezpieczeń (Kluczowe: konkretna wersja bcrypt!)
py -m pip install passlib python-multipart PyJWT
py -m pip install bcrypt==3.2.2

# Instalacja obsługi zmiennych środowiskowych (.env)
py -m pip install python-dotenv

# SKOPIUJ plik .env.example, zmień jego nazwę na .env i uzupełnij w nim swoje dane logowania do bazy!

pip install fastapi-mail

py -m uvicorn app.main:app --reload
