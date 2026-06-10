import os
import psycopg2
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
        print(f"Błąd połączenia z bazą: {e}")
        return None

def wgraj_loty_testowe():
    conn = get_db_connection()
    if not conn:
        print("Nie udało się połączyć z bazą")
        return

    zapytania = [
        """
        INSERT INTO loty (id_lotu, numer_lotu, kierunek, planowo, bramka, status, cena_bazowa) VALUES 
        (1, 'LO3901', 'Kraków (KRK)', '2026-06-11 08:00:00', 'A1', 'O czasie', 150.00),
        (2, 'LH1615', 'Monachium (MUC)', '2026-06-11 08:30:00', 'B2', 'O czasie', 400.00),
        (3, 'AF1247', 'Paryż (CDG)', '2026-06-11 09:10:00', 'A3', 'Boarding', 500.00),
        (4, 'BA0873', 'Londyn (LHR)', '2026-06-11 09:45:00', 'B1', 'Opóźniony', 350.00),
        (5, 'KL1992', 'Amsterdam (AMS)', '2026-06-11 10:20:00', 'B1', 'O czasie', 450.00),
        (6, 'SK1432', 'Kopenhaga (CPH)', '2026-06-11 11:00:00', 'A2', 'O czasie', 300.00),
        (7, 'AY0045', 'Helsinki (HEL)', '2026-06-11 11:30:00', 'A3', 'O czasie', 320.00),
        (8, 'LX1332', 'Zurych (ZRH)', '2026-06-11 12:15:00', 'B1', 'O czasie', 600.00),
        (9, 'OS0602', 'Wiedeń (VIE)', '2026-06-11 13:00:00', 'A3', 'O czasie', 250.00),
        (10, 'LO0320', 'Warszawa (WAW)', '2026-06-11 13:45:00', 'B1', 'Odprawa', 200.00),
        (11, 'FR1023', 'Dublin (DUB)', '2026-06-11 14:20:00', 'B1', 'O czasie', 180.00),
        (12, 'W63021', 'Rzym (FCO)', '2026-06-11 15:00:00', 'A2', 'Opóźniony', 220.00),
        (13, 'U24510', 'Berlin (BER)', '2026-06-11 15:30:00', 'B1', 'O czasie', 150.00),
        (14, 'IB3140', 'Madryt (MAD)', '2026-06-11 16:15:00', 'B2', 'O czasie', 480.00),
        (15, 'TP1201', 'Lizbona (LIS)', '2026-06-11 17:00:00', 'A2', 'O czasie', 550.00),
        (16, 'EI0234', 'Cork (ORK)', '2026-06-11 17:45:00', 'A3', 'O czasie', 310.00),
        (17, 'SN2830', 'Bruksela (BRU)', '2026-06-11 18:30:00', 'B2', 'O czasie', 350.00),
        (18, 'A30412', 'Ateny (ATH)', '2026-06-11 19:15:00', 'A3', 'O czasie', 420.00),
        (19, 'TK1040', 'Stambuł (IST)', '2026-06-11 20:00:00', 'A1', 'O czasie', 700.00),
        (20, 'EK0115', 'Dubaj (DXB)', '2026-06-11 20:45:00', 'B2', 'Opóźniony', 1200.00),
        (21, 'QR0204', 'Doha (DOH)', '2026-06-11 21:30:00', 'B1', 'O czasie', 1500.00),
        (22, 'EY0080', 'Abu Zabi (AUH)', '2026-06-11 22:15:00', 'A3', 'O czasie', 1400.00),
        (23, 'LO3903', 'Kraków (KRK)', '2026-06-12 08:00:00', 'A1', 'O czasie', 150.00),
        (24, 'LH1617', 'Monachium (MUC)', '2026-06-12 08:30:00', 'B2', 'O czasie', 400.00),
        (25, 'AF1249', 'Paryż (CDG)', '2026-06-12 09:10:00', 'A3', 'O czasie', 500.00),
        (26, 'BA0875', 'Londyn (LHR)', '2026-06-12 09:45:00', 'B1', 'O czasie', 350.00),
        (27, 'KL1994', 'Amsterdam (AMS)', '2026-06-12 10:20:00', 'B2', 'O czasie', 450.00),
        (28, 'SK1434', 'Kopenhaga (CPH)', '2026-06-12 11:00:00', 'A2', 'O czasie', 300.00),
        (29, 'AY0047', 'Helsinki (HEL)', '2026-06-12 11:30:00', 'A3', 'O czasie', 320.00),
        (30, 'LX1334', 'Zurych (ZRH)', '2026-06-12 12:15:00', 'B1', 'O czasie', 600.00)
        ON CONFLICT (id_lotu) DO NOTHING;
        """,
        "SELECT setval('loty_id_lotu_seq', (SELECT COALESCE(MAX(id_lotu), 1) FROM loty));"
    ]

    try:
        cursor = conn.cursor()
        print("Wgrywanie testowej bazy 30 lotów...")
        
        for sql in zapytania:
            cursor.execute(sql)
            
        conn.commit()
        print("Gotowe! 30 lotów zostało wgranych do bazy danych.")
    except Exception as e:
        conn.rollback()
        print(f"Błąd wgrywania danych: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    wgraj_loty_testowe()