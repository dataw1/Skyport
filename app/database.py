import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Błąd bazy danych: {e}")
        return None

def utworz_admina_przy_starcie():
    from app.security import pwd_context 
    
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
            print("Sukces! Konto admina utworzone.")
        except Exception as e:
            conn.rollback()
            print(f"Błąd podczas tworzenia admina: {e}")
    else:
        print("Konto admina już istnieje w bazie.")
    
    cur.close()
    conn.close()

def sprawdz_dostepnosc_miejsc(rodzaj_parkingu: str, data_przyjazdu: str, data_wyjazdu: str):
    conn = get_db_connection()
    if not conn:
        return {"error": "Błąd połączenia z bazą danych."}

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT pojemnosc_total FROM parkingi WHERE nazwa = %s;", (rodzaj_parkingu,))
        parking = cursor.fetchone()
        
        if not parking:
            return {"error": "Nie znaleziono takiego parkingu w bazie (upewnij się, że wykonałeś skrypt SQL)."}
        
        pojemnosc_total = parking[0]

        query = """
            SELECT COUNT(*) FROM rezerwacje_parkingu 
            WHERE rodzaj_parkingu = %s 
            AND status != 'anulowana'
            AND data_przyjazdu < %s 
            AND data_wyjazdu > %s;
        """
        cursor.execute(query, (rodzaj_parkingu, data_wyjazdu, data_przyjazdu))
        zajete_miejsca = cursor.fetchone()[0]

        wolne_miejsca = pojemnosc_total - zajete_miejsca

        return {
            "dostepny": wolne_miejsca > 0,
            "wolne_miejsca": wolne_miejsca,
            "zajete": zajete_miejsca,
            "pojemnosc_calkowita": pojemnosc_total
        }

    except Exception as e:
        print(f"Błąd podczas sprawdzania dostępności: {e}")
        return {"error": "Wystąpił błąd serwera podczas odpytywania bazy danych."}
    finally:
        if conn:
            cursor.close()
            conn.close()