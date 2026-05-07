# ✈️ SkyPort

Aplikacja webowa do zarządzania lotami, parkingami i rezerwacjami. Projekt posiada wbudowany panel dla pasażerów, pracowników oraz administratorów.

---

## 🐳 Szybki start (Zalecane - Docker)

Dzięki konteneryzacji, uruchomienie projektu i bazy danych wymaga tylko kilku prostych kroków. Nie musisz ręcznie instalować Pythona ani bazy PostgreSQL na swoim komputerze.

### Wymagania
* Zainstalowany **Docker** oraz **Docker Compose** (np. Docker Desktop).

### Instrukcja uruchomienia

1. **Zmienne środowiskowe:** Skopiuj plik `.env.example`, zmień jego nazwę na `.env`. Dla domyślnego środowiska Dockerowego, upewnij się, że ustawienia bazy wyglądają tak:
   ```env
   DB_NAME=mazwa_bazy
   DB_USER=uzytkownik_bazy
   DB_PASSWORD=haslo_do_bazy
   DB_HOST=db
   DB_PORT=5432
   ```

2. **Baza danych:**
   Upewnij się, że w głównym folderze projektu znajduje się plik ze strukturą bazy danych o nazwie `init.sql`. Docker automatycznie załaduje go przy pierwszym uruchomieniu i stworzy wszystkie tabele.

3. **Uruchomienie kontenerów:**
   Otwórz terminal w folderze projektu i wpisz:
   ```bash
   docker-compose up --build
   ```

4. **Gotowe!**
   Aplikacja będzie dostępna w przeglądarce pod adresem: **http://localhost:8000**

### 🔑 Domyślne konto administratora
Jeśli baza danych została poprawnie zainicjalizowana, możesz zalogować się do panelu administratora:
* **E-mail:** `admin@skyport.pl`
* **Hasło:** `********`

Przy próbie resetu ustawień dockera używamy : 
docker-compose down -v
a potem 
docker-compose up
---

## 💻 Uruchomienie lokalne (Bez Dockera)

Jeśli wolisz uruchomić projekt bezpośrednio w swoim systemie, postępuj zgodnie z poniższymi krokami. Wymaga to posiadania własnego serwera PostgreSQL.

**1. Instalacja FastAPI i serwera:**
```bash
py -m pip install fastapi uvicorn[standard]
```

**2. Instalacja silnika szablonów i obsługi bazy danych:**
```bash
py -m pip install jinja2 psycopg2-binary
```

**3. Instalacja zabezpieczeń i autoryzacji:**
*(Kluczowe: wymagana jest konkretna wersja biblioteki bcrypt!)*
```bash
py -m pip install passlib python-multipart PyJWT
py -m pip install bcrypt==3.2.2
```

**4. Instalacja obsługi zmiennych środowiskowych i maili:**
```bash
py -m pip install python-dotenv fastapi-mail email-validator
```

**5. Konfiguracja:**
Skopiuj plik `.env.example`, zmień jego nazwę na `.env` i uzupełnij w nim swoje własne, lokalne dane logowania do bazy PostgreSQL (wtedy `DB_HOST` zazwyczaj ustawia się na `localhost`).

**6. Uruchomienie serwera:**
```bash
py -m uvicorn app.main:app --reload
```