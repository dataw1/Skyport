from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import utworz_admina_przy_starcie
from app.routers import auth, views, admin, pracownik

from app.routers import auth, views, admin

app = FastAPI(title="SkyPort")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(views.router)
app.include_router(admin.router)
app.include_router(pracownik.router)

@app.on_event("startup")
def startup_event():
    utworz_admina_przy_starcie()