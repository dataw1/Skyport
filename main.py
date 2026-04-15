from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form, status
from fastapi.responses import RedirectResponse
import jwt
import math
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
    
    # Pobieranie lotów z bazy danych dla strony głównej
    conn = get_db_connection()
    loty_do_wyswietlenia = []
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Pobieramy np. 10 najbliższych lotów
            cur.execute("SELECT * FROM Loty ORDER BY planowo ASC LIMIT 10")
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                
                if obecny_status.lower() == 'opóźniony':
                    status_css = "delayed"
                elif obecny_status.lower() == 'boarding':
                    status_css = "boarding"
                
                # Formatowanie czasu do postaci HH:MM, jeśli 'planowo' to obiekt datetime
                planowo_str = lot['planowo'].strftime('%H:%M') if lot.get('planowo') else '00:00'
                
                loty_do_wyswietlenia.append({
                    "numer_lotu": lot.get('numer_lotu', 'Brak'),
                    "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": planowo_str,
                    "bramka": lot.get('bramka', '-'),
                    "status": obecny_status,
                    "status_css": status_css
                })
        except Exception as e:
            print(f"Błąd pobierania lotów na stronę główną: {e}")
        finally:
            cur.close()
            conn.close()

    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "request": request, 
            "user": user,
            "loty": loty_do_wyswietlenia # Przekazujemy loty do HTML-a
        }
    )

@app.get("/loty", response_class=HTMLResponse)
async def strona_loty(request: Request, page: int = 1):
    user = get_current_user(request)
    conn = get_db_connection()
    loty_do_wyswietlenia = []
    
    total_pages = 1
    items_per_page = 20
    page_range = []
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:

            cur.execute("SELECT COUNT(*) as total FROM Loty")
            total_items = cur.fetchone()['total']

            total_pages = math.ceil(total_items / items_per_page)

            if page < 1: page = 1
            if page > total_pages and total_pages > 0: page = total_pages

            offset = (page - 1) * items_per_page
            cur.execute("SELECT * FROM Loty ORDER BY planowo ASC LIMIT %s OFFSET %s", (items_per_page, offset))
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                
                if obecny_status.lower() == 'opóźniony':
                    status_css = "delayed"
                elif obecny_status.lower() == 'boarding':
                    status_css = "boarding"
                elif obecny_status.lower() == 'odwołany':
                    status_css = "delayed" 
                
                planowo_str = lot['planowo'].strftime('%H:%M') if lot.get('planowo') else '00:00'
                
                loty_do_wyswietlenia.append({
                    "numer_lotu": lot.get('numer_lotu', 'Brak'),
                    "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": planowo_str,
                    "bramka": lot.get('bramka', '-'),
                    "status": obecny_status,
                    "status_css": status_css
                })
        except Exception as e:
            print(f"Błąd pobierania lotów: {e}")
        finally:
            cur.close()
            conn.close()

    start_page = max(1, page - 1)
    end_page = min(total_pages, page + 1)
    
    if page == 1:
        end_page = min(total_pages, 3)
    elif page == total_pages and total_pages >= 3:
        start_page = total_pages - 2
        
    page_range = range(start_page, end_page + 1)

    return templates.TemplateResponse(
        request=request, 
        name="loty.html", 
        context={
            "request": request, 
            "user": user,
            "loty": loty_do_wyswietlenia,
            "current_page": page,
            "total_pages": total_pages,
            "page_range": page_range
        }
    )

@app.get("/parking", response_class=HTMLResponse)
async def strona_parking(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="parking.html", context={"request": request, "user": user})

@app.get("/mapy", response_class=HTMLResponse)
async def strona_mapy(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="mapy.html", context={"request": request, "user": user})

@app.get("/bezpieczenstwo", response_class=HTMLResponse)
async def strona_bezpieczenstwo(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="bezpieczenstwo.html", context={"request": request, "user": user})

@app.get("/pomoc", response_class=HTMLResponse)
async def strona_pomoc(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="pomoc.html", context={"request": request, "user": user})

@app.get("/logowanie", response_class=HTMLResponse)
async def strona_logowania(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse(request=request, name="logowanie.html", context={"request": request, "user": user})



@app.post("/auth/register")
async def rejestracja_post(imie: str = Form(...), nazwisko: str = Form(...), email: str = Form(...), haslo: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        haslo_hash = pwd_context.hash(haslo)
        

        cur.execute(
            "INSERT INTO Konta (email, haslo, rola) VALUES (%s, %s, %s) RETURNING id_konta",
            (email, haslo_hash, 'pasazer')
        )
        nowe_id_konta = cur.fetchone()[0]


        cur.execute(
            "INSERT INTO Pasazerowie (id_konta, imie, nazwisko) VALUES (%s, %s, %s)",
            (nowe_id_konta, imie, nazwisko)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Błąd rejestracji: {e}")
        return RedirectResponse(url="/logowanie?error=register_failed", status_code=status.HTTP_302_FOUND)
    finally:
        cur.close()
        conn.close()


    return RedirectResponse(url="/logowanie?success=registered", status_code=status.HTTP_302_FOUND)

@app.post("/auth/login")
async def logowanie_post(email: str = Form(...), haslo: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Konta WHERE email = %s", (email,))
    user_db = cur.fetchone()

    if user_db and pwd_context.verify(haslo, user_db['haslo']):

        imie_uzytkownika = "Admin" 
        
        if user_db['rola'] == 'pasazer':
            cur.execute("SELECT imie FROM Pasazerowie WHERE id_konta = %s", (user_db['id_konta'],))
            pasazer = cur.fetchone()
            if pasazer:
                imie_uzytkownika = pasazer['imie']


        token = jwt.encode({
            "email": user_db['email'],
            "rola": user_db['rola'],
            "id": user_db['id_konta'],
            "imie": imie_uzytkownika, 
            "exp": datetime.utcnow() + timedelta(hours=8)
        }, SECRET_KEY, algorithm=ALGORITHM)

        cur.close()
        conn.close()

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_token", value=token, httponly=True)
        return response
    
    cur.close()
    conn.close()
    return RedirectResponse(url="/logowanie?error=invalid", status_code=status.HTTP_302_FOUND)

@app.get("/wyloguj")
async def wylogowanie():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response

@app.get("/admin", response_class=HTMLResponse)
async def panel_admina(request: Request):
    user = get_current_user(request)
    

    if not user or user.get("rola") != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    conn = get_db_connection()
    loty_do_wyswietlenia = []
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM Loty ORDER BY id_lotu DESC LIMIT 20")
            loty_db = cur.fetchall()
            

            for lot in loty_db:
                status_css = "on-time" 
                obecny_status = str(lot.get('status', 'O czasie'))
                
                if obecny_status.lower() == 'opóźniony':
                    status_css = "delayed"
                elif obecny_status.lower() == 'boarding':
                    status_css = "boarding"
                
                loty_do_wyswietlenia.append({
                    "id": lot.get('id_lotu', 1),
                    "numer_lotu": lot.get('numer_lotu', 'Brak'),
                    "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": lot.get('planowo', '00:00'),
                    "bramka": lot.get('bramka', '-'),
                    "status": obecny_status,
                    "status_css": status_css
                })
        except Exception as e:
            print(f"Błąd pobierania lotów do panelu admina: {e}")
        finally:
            cur.close()
            conn.close()


    return templates.TemplateResponse(
        request=request, 
        name="admin_panel.html", 
        context={
            "request": request, 
            "user": user, 
            "loty": loty_do_wyswietlenia
        }
    )