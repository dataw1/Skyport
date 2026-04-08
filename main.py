from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="SkyPort")

# Ustawienie katalogu dla plikow HTML i CSS
app.mount("/static", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def strona_glowna(request: Request):

    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "user": None})
# Dzialanie przyciskow na stronie
@app.get("/loty", response_class=HTMLResponse)
async def strona_loty(request: Request):
    return templates.TemplateResponse(request=request, name="loty.html", context={"request": request, "user": None})

@app.get("/parking", response_class=HTMLResponse)
async def strona_parking(request: Request):
    return templates.TemplateResponse(request=request, name="parking.html", context={"request": request, "user": None})

@app.get("/mapy", response_class=HTMLResponse)
async def strona_mapy(request: Request):
    return templates.TemplateResponse(request=request, name="mapy.html", context={"request": request, "user": None})

@app.get("/bezpieczenstwo", response_class=HTMLResponse)
async def strona_bezpieczenstwo(request: Request):
    return templates.TemplateResponse(request=request, name="bezpieczenstwo.html", context={"request": request, "user": None})

@app.get("/pomoc", response_class=HTMLResponse)
async def strona_pomoc(request: Request):
    return templates.TemplateResponse(request=request, name="pomoc.html", context={"request": request, "user": None})

@app.get("/logowanie", response_class=HTMLResponse)
async def strona_logowania(request: Request):
    return templates.TemplateResponse(request=request, name="logowanie.html", context={"request": request, "user": None})