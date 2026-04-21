from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import utworz_admina_przy_starcie

# Importujemy nasze moduły (Routery)
from app.routers import auth, views, admin

app = FastAPI(title="SkyPort")

# Uwaga: Upewnij się, że przeniosłeś pliki .css do osobnego folderu "static" obok folderu "app"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Podpinamy wszystkie ścieżki
app.include_router(auth.router)
app.include_router(views.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_event():
    utworz_admina_przy_starcie()