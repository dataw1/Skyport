# Skyport

W pliku trzeba wpisać tą komendę
pip install fastapi uvicorn psycopg2-binary passlib bcrypt pyjwt jinja2 python-multipart


# Instalacja FastAPI i serwera
py -m pip install fastapi uvicorn[standard]

# Instalacja silnika szablonów i bazy danych
py -m pip install jinja2 psycopg2

# Instalacja zabezpieczeń (Kluczowe: konkretna wersja bcrypt!)
py -m pip install passlib python-multipart PyJWT
py -m pip install bcrypt==3.2.2

py -m uvicorn app.main:app --reload
