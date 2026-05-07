# Wybieramy oficjalny, lekki obraz z Pythonem
FROM python:3.11-slim

# Instalujemy zależności systemowe potrzebne dla psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Ustawiamy folder roboczy wewnątrz "pudełka"
WORKDIR /code

# Kopiujemy plik z wymaganymi bibliotekami
COPY requirements.txt /code/

# Instalujemy biblioteki Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą resztę naszego kodu do pudełka
COPY . /code/

# Mówimy, że aplikacja będzie działać na porcie 8000
EXPOSE 8000

# Komenda, która uruchamia Twój serwer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]