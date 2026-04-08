from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form, status
from fastapi.responses import RedirectResponse
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor

# Polaczenie z baza danych
from database import get_db_connection
app = FastAPI(title="SkyPort")

# Ustawienie katalogu dla plikow HTML i CSS
app.mount("/static", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")
# Ustawienia dla JWT i hashowania hasel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "klucz_szyfru"
ALGORITHM = "HS256"

def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        return None
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None


@app.on_event("startup")
def utworz_admina_przy_starcie():
    conn = get_db_connection()
    if not conn:
        print("Błąd: Nie można połączyć się z bazą danych przy starcie.")
        return
        
    cur = conn.cursor()
    
    cur.execute("SELECT id_konta FROM Konta WHERE email = 'admin@skyport.pl'")
    admin_istnieje = cur.fetchone()
    
    if not admin_istnieje:
        print("Brak konta admina. Tworzę nowe konto...")
        haslo_hash = pwd_context.hash("admin123") 
        
        try:
            cur.execute(
                "INSERT INTO Konta (email, haslo, rola) VALUES (%s, %s, %s)", 
                ('admin@skyport.pl', haslo_hash, 'admin')
            )
            conn.commit()
            print("Sukces! Konto admina (admin@skyport.pl / admin123) zostało utworzone.")
        except Exception as e:
            conn.rollback()
            print(f"Błąd podczas tworzenia admina: {e}")
    else:
        print("Konto admina już istnieje w bazie.")
    
    cur.close()
    conn.close()


@app.get("/", response_class=HTMLResponse)
async def strona_glowna(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "user": None})

@app.get("/loty", response_class=HTMLResponse)
async def strona_loty(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="loty.html", context={"request": request, "user": None})

@app.get("/parking", response_class=HTMLResponse)
async def strona_parking(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="parking.html", context={"request": request, "user": None})

@app.get("/mapy", response_class=HTMLResponse)
async def strona_mapy(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="mapy.html", context={"request": request, "user": None})

@app.get("/bezpieczenstwo", response_class=HTMLResponse)
async def strona_bezpieczenstwo(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="bezpieczenstwo.html", context={"request": request, "user": None})

@app.get("/pomoc", response_class=HTMLResponse)
async def strona_pomoc(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="pomoc.html", context={"request": request, "user": None})

@app.get("/logowanie", response_class=HTMLResponse)
async def strona_logowania(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="logowanie.html", context={"request": request, "user": None})



@app.post("/auth/login")
async def logowanie_post(email: str = Form(...), haslo: str = Form(...)):
    # Pobranie danych uzyt
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Konta WHERE email = %s", (email,))
    user_db = cur.fetchone()
    cur.close()
    conn.close()

    # Sprawdzanie hasla
    if user_db and pwd_context.verify(haslo, user_db['haslo']):

        token = jwt.encode({
            "email": user_db['email'],
            "rola": user_db['rola'],
            "id": user_db['id_konta'],
            "exp": datetime.utcnow() + timedelta(hours=8)
        }, SECRET_KEY, algorithm=ALGORITHM)

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_token", value=token, httponly=True)
        return response
    
    return RedirectResponse(url="/logowanie?error=invalid", status_code=status.HTTP_302_FOUND)

@app.get("/wyloguj")
async def wylogowanie():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response