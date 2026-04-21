from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from psycopg2.extras import RealDictCursor
import math

from app.database import get_db_connection
from app.security import get_current_user

router = APIRouter(prefix="/admin", tags=["Administrator"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def panel_admina(request: Request, page: int = 1):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        
    conn = get_db_connection()
    loty_do_wyswietlenia = []
    total_pages = 1
    items_per_page = 10
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
            cur.execute("SELECT * FROM Loty ORDER BY id_lotu DESC LIMIT %s OFFSET %s", (items_per_page, offset))
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                if obecny_status.lower() == 'opóźniony': status_css = "delayed"
                elif obecny_status.lower() == 'boarding': status_css = "boarding"
                elif obecny_status.lower() == 'odwołany': status_css = "delayed"
                
                planowo_str = lot['planowo'].strftime('%Y-%m-%d %H:%M') if lot.get('planowo') else 'Brak'
                loty_do_wyswietlenia.append({
                    "id": lot.get('id_lotu', 1), "numer_lotu": lot.get('numer_lotu', 'Brak'), "kierunek": lot.get('kierunek', 'Brak'),
                    "planowo": planowo_str, "bramka": lot.get('bramka', '-'), "status": obecny_status, "status_css": status_css
                })
        finally:
            cur.close()
            conn.close()

    start_page = max(1, page - 1)
    end_page = min(total_pages, page + 1)
    if page == 1: end_page = min(total_pages, 3)
    elif page == total_pages and total_pages >= 3: start_page = total_pages - 2
    page_range = range(start_page, end_page + 1)

    return templates.TemplateResponse(request=request, name="admin_panel.html", context={"request": request, "user": user, "loty": loty_do_wyswietlenia, "current_page": page, "total_pages": total_pages, "page_range": page_range, "active_tab": "dashboard"})

@router.get("/uzytkownicy", response_class=HTMLResponse)
async def admin_uzytkownicy(request: Request):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    conn = get_db_connection()
    uzytkownicy = []
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Pobieramy dane z tabeli Konta i łączymy z tabelą Pasazerowie (aby mieć imię i nazwisko)
            cur.execute("""
                SELECT k.id_konta, k.email, k.rola, p.imie, p.nazwisko 
                FROM Konta k 
                LEFT JOIN Pasazerowie p ON k.id_konta = p.id_konta 
                ORDER BY k.id_konta DESC LIMIT 50
            """)
            uzytkownicy = cur.fetchall()
        except Exception as e: print(f"Błąd bazy: {e}")
        finally: cur.close(); conn.close()

    return templates.TemplateResponse(request=request, name="admin_uzytkownicy.html", context={"request": request, "user": user, "uzytkownicy": uzytkownicy, "active_tab": "uzytkownicy"})


@router.get("/rezerwacje", response_class=HTMLResponse)
async def admin_rezerwacje(request: Request):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    conn = get_db_connection()
    rezerwacje = []
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT r.id_rezerwacji, r.pnr, r.status, r.data_rezerwacji, k.email, l.numer_lotu 
                FROM Rezerwacje_Lotow r
                LEFT JOIN Konta k ON r.id_konta = k.id_konta
                LEFT JOIN Loty l ON r.id_lotu = l.id_lotu
                ORDER BY r.data_rezerwacji DESC LIMIT 50
            """)
            rezerwacje = cur.fetchall()
        except Exception as e: print(f"Błąd bazy: {e}")
        finally: cur.close(); conn.close()

    return templates.TemplateResponse(request=request, name="admin_rezerwacje.html", context={"request": request, "user": user, "rezerwacje": rezerwacje, "active_tab": "rezerwacje"})


@router.post("/zmien_status/{id_lotu}")
async def admin_zmien_status(request: Request, id_lotu: int, nowy_status: str = Form(...)):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Loty SET status = %s WHERE id_lotu = %s", (nowy_status, id_lotu))
        conn.commit()
    except Exception: conn.rollback()
    finally: cur.close(); conn.close()
    referer = request.headers.get("referer", "/admin")
    return RedirectResponse(url=referer, status_code=status.HTTP_302_FOUND)

@router.get("/dodaj_lot", response_class=HTMLResponse)
async def dodaj_lot_get(request: Request):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="admin_form_lot.html", context={"request": request, "user": user, "akcja": "dodaj"})

@router.post("/dodaj_lot")
async def dodaj_lot_post(request: Request, numer_lotu: str=Form(...), kierunek: str=Form(...), planowo: str=Form(...), bramka: str=Form(...), status_lotu: str=Form(...)):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Loty (numer_lotu, kierunek, planowo, bramka, status) VALUES (%s, %s, %s, %s, %s)", (numer_lotu, kierunek, planowo, bramka, status_lotu))
        conn.commit()
    finally: cur.close(); conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

@router.get("/edytuj/{id_lotu}", response_class=HTMLResponse)
async def edytuj_lot_get(request: Request, id_lotu: int):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    lot = None
    try:
        cur.execute("SELECT * FROM Loty WHERE id_lotu = %s", (id_lotu,))
        lot = cur.fetchone()
    finally: cur.close(); conn.close()
    if not lot: return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    if lot.get('planowo'): lot['planowo_format'] = lot['planowo'].strftime('%Y-%m-%dT%H:%M')
    return templates.TemplateResponse(request=request, name="admin_form_lot.html", context={"request": request, "user": user, "akcja": "edytuj", "lot": lot})

@router.post("/edytuj/{id_lotu}")
async def edytuj_lot_post(request: Request, id_lotu: int, numer_lotu: str=Form(...), kierunek: str=Form(...), planowo: str=Form(...), bramka: str=Form(...), status_lotu: str=Form(...)):
    user = get_current_user(request)
    if not user or user.get("rola") != "admin": return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Loty SET numer_lotu=%s, kierunek=%s, planowo=%s, bramka=%s, status=%s WHERE id_lotu=%s", (numer_lotu, kierunek, planowo, bramka, status_lotu, id_lotu))
        conn.commit()
    finally: cur.close(); conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)