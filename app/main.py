from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from yoyo import read_migrations, get_backend
from app.database import (
    utworz_admina_przy_starcie, 
    DB_USER, 
    DB_PASSWORD, 
    DB_HOST, 
    DB_PORT, 
    DB_NAME
)
from app.routers import auth, views, admin, pracownik

app = FastAPI(title="SkyPort")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(views.router)
app.include_router(admin.router)
app.include_router(pracownik.router)

def uruchom_migracje():
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    backend = get_backend(db_url)
    migrations = read_migrations('migrations')
    
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    print("Udało się : Migracje bazy danych zostały wykonane.")


@app.on_event("startup")
def startup_event():
    uruchom_migracje()
    utworz_admina_przy_starcie()