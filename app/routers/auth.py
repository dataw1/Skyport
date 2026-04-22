from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from psycopg2.extras import RealDictCursor
import jwt
from datetime import datetime, timedelta
import re

from app.database import get_db_connection
from app.security import pwd_context, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Autoryzacja"])

@router.post("/auth/register")
async def rejestracja_post(imie: str = Form(...), nazwisko: str = Form(...), email: str = Form(...), haslo: str = Form(...)):
    wzorzec_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(wzorzec_email, email):
        return RedirectResponse(url="/logowanie?error=invalid_email", status_code=status.HTTP_302_FOUND)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id_konta FROM Konta WHERE email = %s", (email,))
        if cur.fetchone():
            return RedirectResponse(url="/logowanie?error=email_exists", status_code=status.HTTP_302_FOUND)

        haslo_hash = pwd_context.hash(haslo)
        cur.execute("INSERT INTO Konta (email, haslo, rola) VALUES (%s, %s, %s) RETURNING id_konta", (email, haslo_hash, 'pasazer'))
        nowe_id_konta = cur.fetchone()[0]

        cur.execute("INSERT INTO Pasazerowie (id_konta, imie, nazwisko) VALUES (%s, %s, %s)", (nowe_id_konta, imie, nazwisko))
        conn.commit()

        token = jwt.encode({
            "email": email, "rola": "pasazer", "id": nowe_id_konta, "imie": imie, "exp": datetime.utcnow() + timedelta(hours=8)
        }, SECRET_KEY, algorithm=ALGORITHM)

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_token", value=token, httponly=True)
        return response
    except Exception:
        conn.rollback()
        return RedirectResponse(url="/logowanie?error=register_failed", status_code=status.HTTP_302_FOUND)
    finally:
        cur.close()
        conn.close()

@router.post("/auth/login")
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
            "email": user_db['email'], "rola": user_db['rola'], "id": user_db['id_konta'], "imie": imie_uzytkownika, "exp": datetime.utcnow() + timedelta(hours=8)
        }, SECRET_KEY, algorithm=ALGORITHM)

        cur.close()
        conn.close()

        if user_db['rola'] == 'admin':
            cel = "/admin"
        elif user_db['rola'] == 'pracownik':
            cel = "/pracownik"
        else:
            cel = "/"

        response = RedirectResponse(url=cel, status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_token", value=token, httponly=True)
        return response
    
    cur.close()
    conn.close()
    return RedirectResponse(url="/logowanie?error=invalid", status_code=status.HTTP_302_FOUND)

@router.get("/wyloguj")
async def wylogowanie():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response