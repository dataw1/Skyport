from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from psycopg2.extras import RealDictCursor
from typing import Optional
import math

from app.database import get_db_connection
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
            query = "SELECT * FROM Loty WHERE planowo >= NOW() - INTERVAL '2 hours'"
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

    return templates.TemplateResponse(request=request, name="loty.html", context={"request": request, "user": user, "loty": loty_do_wyswietlenia, "current_page": page, "total_pages": total_pages, "page_range": page_range, "search_query": search_query})

@router.get("/parking", response_class=HTMLResponse)
async def strona_parking(request: Request): return templates.TemplateResponse(request=request, name="parking.html", context={"request": request, "user": get_current_user(request)})

@router.get("/mapy", response_class=HTMLResponse)
async def strona_mapy(request: Request): return templates.TemplateResponse(request=request, name="mapy.html", context={"request": request, "user": get_current_user(request)})

@router.get("/bezpieczenstwo", response_class=HTMLResponse)
async def strona_bezpieczenstwo(request: Request): return templates.TemplateResponse(request=request, name="bezpieczenstwo.html", context={"request": request, "user": get_current_user(request)})

@router.get("/pomoc", response_class=HTMLResponse)
async def strona_pomoc(request: Request): return templates.TemplateResponse(request=request, name="pomoc.html", context={"request": request, "user": get_current_user(request)})

@router.get("/logowanie", response_class=HTMLResponse)
async def strona_logowania(request: Request): return templates.TemplateResponse(request=request, name="logowanie.html", context={"request": request, "user": get_current_user(request)})