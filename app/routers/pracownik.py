from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from psycopg2.extras import RealDictCursor

from app.database import get_db_connection
from app.security import get_current_user

router = APIRouter(prefix="/pracownik", tags=["Pracownik"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def panel_pracownika(request: Request):
    user = get_current_user(request)
    if not user or user.get("rola") not in ["admin", "pracownik"]:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        
    conn = get_db_connection()
    loty = []
    
    if conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM Loty ORDER BY planowo ASC LIMIT 20")
            loty_db = cur.fetchall()
            
            for lot in loty_db:
                status_css = "on-time"
                obecny_status = str(lot.get('status', 'O czasie'))
                if obecny_status.lower() == 'opóźniony': status_css = "delayed"
                elif obecny_status.lower() == 'boarding': status_css = "boarding"
                
                loty.append({
                    "numer_lotu": lot['numer_lotu'],
                    "kierunek": lot['kierunek'],
                    "planowo": lot['planowo'].strftime('%H:%M'),
                    "bramka": lot['bramka'],
                    "status": obecny_status,
                    "status_css": status_css
                })
        finally:
            cur.close()
            conn.close()

    return templates.TemplateResponse(
        request=request, 
        name="pracownik_panel.html", 
        context={"request": request, "user": user, "loty": loty}
    )