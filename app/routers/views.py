from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from psycopg2.extras import RealDictCursor
from typing import Optional
import math
import string
import random

from app.database import get_db_connection, sprawdz_dostepnosc_miejsc
from app.security import get_current_user

router = APIRouter(tags=["Widoki Publiczne"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def strona_glowna(request: Request, kierunek: Optional[str] = None, data: Optional[str] = None, numer_lotu: Optional[str] = None):
    user = get_current_user(request)
    conn = get_db_connection()
    loty_do_wyswietlenia = []
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:

            # albo wywietla tylko te co maja planowo odlot w ciagu 2h, albo wszystkie z opcja filtrowania

            # query = "SELECT * FROM Loty WHERE planowo >= NOW() - INTERVAL '2 hours'"
            query = "SELECT * FROM Loty WHERE 1=1"



            params = []
            if kierunek:
                query += " AND kierunek ILIKE %s"
                params.append(f"%{kierunek}%")
            if data:
                query += " AND DATE(planowo) = %s"
                params.append(data)
            if numer_lotu:
                query += " AND numer_lotu ILIKE %s"
                params.append(f"%{numer_lotu}%")
                
            query += " ORDER BY planowo ASC LIMIT 10"
            cur.execute(query, tuple(params))
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                if obecny_status.lower() == 'opóźniony': status_css = "delayed"
                elif obecny_status.lower() == 'boarding': status_css = "boarding"
                elif obecny_status.lower() == 'odwołany': status_css = "delayed"
                
                planowo_str = lot['planowo'].strftime('%H:%M') if lot.get('planowo') else '00:00'
                loty_do_wyswietlenia.append({
                    "numer_lotu": lot.get('numer_lotu', 'Brak'), "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": planowo_str, "bramka": lot.get('bramka', '-'), "status": obecny_status, "status_css": status_css
                })
        except Exception as e:
            print(f"Błąd: {e}")
        finally:
            cur.close()
            conn.close()

    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "user": user, "loty": loty_do_wyswietlenia})


@router.get("/loty", response_class=HTMLResponse)
async def strona_loty(request: Request, page: int = 1, kierunek: Optional[str] = None, data: Optional[str] = None, numer_lotu: Optional[str] = None):
    user = get_current_user(request)
    conn = get_db_connection()
    loty_do_wyswietlenia = []
    total_pages = 1
    items_per_page = 20
    page_range = []
    search_query = f"&kierunek={kierunek or ''}&data={data or ''}&numer_lotu={numer_lotu or ''}"
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query_conditions = "WHERE 1=1"
            params = []
            if kierunek:
                query_conditions += " AND kierunek ILIKE %s"
                params.append(f"%{kierunek}%")
            if data:
                query_conditions += " AND DATE(planowo) = %s"
                params.append(data)
            if numer_lotu:
                query_conditions += " AND numer_lotu ILIKE %s"
                params.append(f"%{numer_lotu}%")

            cur.execute(f"SELECT COUNT(*) as total FROM Loty {query_conditions}", tuple(params))
            total_items = cur.fetchone()['total']
            
            total_pages = math.ceil(total_items / items_per_page)
            if page < 1: page = 1
            if page > total_pages and total_pages > 0: page = total_pages
            
            offset = (page - 1) * items_per_page
            data_query = f"SELECT * FROM Loty {query_conditions} ORDER BY planowo ASC LIMIT %s OFFSET %s"
            
            final_params = tuple(params) + (items_per_page, offset)
            cur.execute(data_query, final_params)
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                if obecny_status.lower() == 'opóźniony': status_css = "delayed"
                elif obecny_status.lower() == 'boarding': status_css = "boarding"
                elif obecny_status.lower() == 'odwołany': status_css = "delayed"
                
                planowo_str = lot['planowo'].strftime('%H:%M') if lot.get('planowo') else '00:00'
                loty_do_wyswietlenia.append({
                    "numer_lotu": lot.get('numer_lotu', 'Brak'), "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": planowo_str, "bramka": lot.get('bramka', '-'), "status": obecny_status, "status_css": status_css,
                    "id_lotu": lot['id_lotu'],  
                })
        finally:
            cur.close()
            conn.close()

    start_page = max(1, page - 1)
    end_page = min(total_pages, page + 1)
    if page == 1: end_page = min(total_pages, 3)
    elif page == total_pages and total_pages >= 3: start_page = total_pages - 2
    page_range = range(start_page, end_page + 1)

    return templates.TemplateResponse(request=request, name="loty.html", context={"request": request, "user": user, "loty": loty_do_wyswietlenia, "current_page": page, "total_pages": total_pages, "page_range": page_range, "search_query": search_query})


@router.get("/parking", response_class=HTMLResponse)
async def strona_parking(request: Request): 
    return templates.TemplateResponse(request=request, name="parking.html", context={"request": request, "user": get_current_user(request)})


@router.post("/sprawdz-parking", response_class=HTMLResponse)
async def sprawdz_parking_endpoint(
    request: Request,
    data_przyjazdu: str = Form(...),
    data_wyjazdu: str = Form(...),
    rodzaj_parkingu: str = Form(...)
):
    user = get_current_user(request)
    wynik = sprawdz_dostepnosc_miejsc(rodzaj_parkingu, data_przyjazdu, data_wyjazdu)
    
    if "error" in wynik:
        wiadomosc = wynik["error"]
        czy_sukces = False
    elif wynik["dostepny"]:
        wiadomosc = f"Świetnie! Mamy wolne miejsca ({wynik['wolne_miejsca']} z {wynik['pojemnosc_calkowita']}). Możesz przejść do rezerwacji!"
        czy_sukces = True
    else:
        wiadomosc = "Przepraszamy, ten parking jest w pełni zarezerwowany w tym terminie."
        czy_sukces = False

    return templates.TemplateResponse(
        request=request, 
        name="parking.html", 
        context={
            "request": request, 
            "user": user, 
            "wiadomosc": wiadomosc,
            "czy_sukces": czy_sukces
        }
    )
@router.get("/rezerwacja-parkingu", response_class=HTMLResponse)
async def strona_rezerwacji_parkingu(request: Request, rodzaj: Optional[str] = None):
    user = get_current_user(request)
    
    
    if not user:
        return RedirectResponse(url="/logowanie", status_code=303)
    
    return templates.TemplateResponse(
        request=request, 
        name="rezerwacja_parkingu.html", 
        context={
            "request": request, 
            "user": user, 
            "wybrany_rodzaj": rodzaj
        }
    )
@router.get("/mapy", response_class=HTMLResponse)
async def strona_mapy(request: Request): return templates.TemplateResponse(request=request, name="mapy.html", context={"request": request, "user": get_current_user(request)})

@router.get("/bezpieczenstwo", response_class=HTMLResponse)
async def strona_bezpieczenstwo(request: Request): return templates.TemplateResponse(request=request, name="bezpieczenstwo.html", context={"request": request, "user": get_current_user(request)})

@router.get("/pomoc", response_class=HTMLResponse)
async def strona_pomoc(request: Request): return templates.TemplateResponse(request=request, name="pomoc.html", context={"request": request, "user": get_current_user(request)})

@router.get("/logowanie", response_class=HTMLResponse)
async def strona_logowania(request: Request): return templates.TemplateResponse(request=request, name="logowanie.html", context={"request": request, "user": get_current_user(request)})

@router.post("/potwierdz-rezerwacje")
async def potwierdz_rezerwacje_endpoint(
    request: Request,
    data_przyjazdu: str = Form(...),
    data_wyjazdu: str = Form(...),
    rodzaj_parkingu: str = Form(...),
    nr_rejestracyjny: str = Form(...),
    rodzaj_pojazdu: str = Form(...)
):

    user = get_current_user(request)
    
    if not user:
        return RedirectResponse(url="/logowanie", status_code=303)
        
    id_konta_klienta = user.get('id') 

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO rezerwacje_parkingu 
                (id_konta, rodzaj_parkingu, rodzaj_pojazdu, data_przyjazdu, data_wyjazdu, nr_rejestracyjny, status) 
                VALUES (%s, %s, %s, %s, %s, %s, 'oczekujaca')
            """, (
                id_konta_klienta, 
                rodzaj_parkingu, 
                rodzaj_pojazdu, 
                data_przyjazdu, 
                data_wyjazdu, 
                nr_rejestracyjny
            ))
            
            conn.commit() 
            cur.close()
        except Exception as e:
            print(f"Błąd podczas zapisu rezerwacji: {e}")
            if conn:
                conn.rollback()
            return HTMLResponse("<h1>Wystąpił błąd podczas zapisu do bazy danych. Spróbuj ponownie.</h1>")
        finally:
            if conn:
                conn.close()

    return HTMLResponse(f"""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1 style="color: #28a745;">Sukces! Rezerwacja została potwierdzona.</h1>
            <p>Dziękujemy, {user.get('imie')}! Miejsce zostało zarezerwowane i zapisane w systemie.</p>
            <div style="background-color: #f8f9fa; display: inline-block; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left;">
                <p><strong>Parking:</strong> {rodzaj_parkingu}</p>
                <p><strong>Pojazd:</strong> {rodzaj_pojazdu} (Nr: {nr_rejestracyjny})</p>
                <p><strong>Przyjazd:</strong> {data_przyjazdu.replace('T', ' ')}</p>
                <p><strong>Wyjazd:</strong> {data_wyjazdu.replace('T', ' ')}</p>
            </div>
            <br><br>
            <a href='/parking' style="padding: 10px 20px; background-color: #f1c40f; color: black; text-decoration: none; border-radius: 5px; font-weight: bold;">Wróć do strony głównej</a>
        </div>
    """)
@router.post("/rezerwuj-lot/{id_lotu}", response_class=HTMLResponse)
async def rezerwuj_lot_endpoint(request: Request, id_lotu: int):
    user = get_current_user(request)
    
    if not user:
        return RedirectResponse(url="/logowanie", status_code=status.HTTP_302_FOUND)

    conn = get_db_connection()
    if not conn:
        return HTMLResponse("Błąd połączenia z bazą danych.")

    pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT numer_lotu, kierunek FROM Loty WHERE id_lotu = %s", (id_lotu,))
        lot = cur.fetchone()

        cur.execute("""
            INSERT INTO rezerwacje_lotow (id_konta, id_lotu, pnr, status) 
            VALUES (%s, %s, %s, 'Aktywna')
        """, (user['id'], id_lotu, pnr))
        conn.commit()
        
        return HTMLResponse(f"""
            <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h1 style="color: #28a745;">Sukces! Zarezerwowano bilet lotniczy.</h1>
                <p>Twój unikalny kod rezerwacji (PNR) to: <strong>{pnr}</strong></p>
                <div style="background-color: #f8f9fa; display: inline-block; padding: 20px; border-radius: 10px; margin-top: 20px;">
                    <p><strong>Lot:</strong> {lot['numer_lotu']}</p>
                    <p><strong>Kierunek:</strong> {lot['kierunek']}</p>
                    <p><strong>Pasażer:</strong> {user.get('imie')}</p>
                </div>
                <br><br>
                <a href='/loty' style="padding: 10px 20px; background-color: #f1c40f; color: black; text-decoration: none; border-radius: 5px; font-weight: bold;">Wróć do tablicy lotów</a>
            </div>
        """)
    except Exception as e:
        conn.rollback()
        print(f"Błąd rezerwacji lotu: {e}")
        return HTMLResponse("<h1>Wystąpił błąd. Możliwe, że ten lot nie istnieje. Spróbuj ponownie.</h1>")
    finally:
        cur.close()
        conn.close()