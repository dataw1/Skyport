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
        print(f"Błąd połączenia z bazą")
        return None

def wgraj_dane_testowe():
    conn = get_db_connection()
    if not conn:
        print("Nie udało się połączyć z bazą")
        return

    zapytania = [
        """
        INSERT INTO konta (id_konta, email, haslo, rola) VALUES 
        (1, 'admin@skyport.pl', '$2b$12$DUDhbIBuf9iMymg659RV1.r9DDFI8jdgw42BrWdXy4v.xXGuzrbiW', 'admin'),
        (2, 'test@test.com', '$2b$12$soZ4ZA1J.wNa7Kw9PE5Adu891rp25WgjxaZFrZ0ixmId8xDVnEv5y', 'pasazer'),
        (3, 'Jan@skyport.pl', '$2b$12$5mq65o5rgrX2mLAR4YhxeOc0v7mEMUa31Sy.mBkEZf2E0cFae3fPO', 'pasazer'),
        (4, 'pracownik1@skyport.pl', '$2b$12$saqNeU7kdRXsVZbKGxqct.4U2f6Tb5S.B/u6hXaLgd1T7XlrkFQLC', 'pracownik'),
        (5, 'janek@skyport.pl', '$2b$12$G0tXVy2gw1lwQGZ0lLGPZOUhJL/cuu.akHJjJMAWrliaWhg6/BXHe', 'pasazer'),
        (9, 'Dominik@skyport.pl', '$2b$12$yuPllojD8RivRrUgcJAo5uZsIgGe6TaIp0gQl/AR/s.XcizvyQ/uu', 'pasazer'),
        (11, 'Dominikadmin@skyport.pl', '$2b$12$gep8FmQ4.2HvSzB1StoFH.HMilAZQhsYyfvgIQCbF0eDl6CG/h3py', 'admin'),
        (12, 'Dominik2@skyport.pl', '$2b$12$.Z46f602ETxJKd8/7bL7S.FqUdHua5CNS.S5r34pyRN1o97geRz9e', 'pasazer')
        ON CONFLICT (email) DO NOTHING;
        """,
        "SELECT setval('konta_id_konta_seq', (SELECT COALESCE(MAX(id_konta), 1) FROM konta));",

        """
        INSERT INTO loty (id_lotu, numer_lotu, kierunek, planowo, bramka, status, cena_bazowa) VALUES 
        (1, 'BA123', 'Londyn Heathrow', '2026-04-15 14:30:00', 'A12', 'Boarding', 300.00),
        (2, 'LH456', 'Frankfurt', '2026-04-15 14:45:00', 'B04', 'O czasie', 300.00),
        (3, 'AF789', 'Paryż CDG', '2026-04-15 15:00:00', 'A08', 'O czasie', 300.00),
        (4, 'KL321', 'Amsterdam', '2026-04-15 15:15:00', 'B11', 'Opóźniony', 300.00),
        (26, 'GR569', 'Kraków Kraków', '2026-04-21 09:00:00', 'C6', 'O czasie', 300.00),
        (27, 'AY105', 'Zurych (ZRH)', '2026-05-07 18:40:00', 'A1', 'O czasie', 300.00)
        ON CONFLICT (id_lotu) DO NOTHING;
        """,
        "SELECT setval('loty_id_lotu_seq', (SELECT COALESCE(MAX(id_lotu), 1) FROM loty));",

        """
        INSERT INTO pasazerowie (id_pasazera, id_konta, imie, nazwisko) VALUES 
        (1, 2, 'Grzegorz', 'Twaróg'),
        (2, 3, 'Jan', 'Kowalski'),
        (3, 4, 'Maciek', 'Wtylnowy'),
        (4, 5, 'janek', 'wójcik'),
        (5, 9, 'Dominik', 'Migacz')
        ON CONFLICT (id_konta) DO NOTHING;
        """,
        "SELECT setval('pasazerowie_id_pasazera_seq', (SELECT COALESCE(MAX(id_pasazera), 1) FROM pasazerowie));",

        """
        INSERT INTO pracownicy (id_pracownika, id_konta, imie, nazwisko, stanowisko) VALUES 
        (1, 11, 'dominikadmin', 'Migacz', 'Administrator')
        ON CONFLICT (id_konta) DO NOTHING;
        """,
        "SELECT setval('pracownicy_id_pracownika_seq', (SELECT COALESCE(MAX(id_pracownika), 1) FROM pracownicy));",

        """
        INSERT INTO rezerwacje_lotow (id_rezerwacji, id_konta, id_lotu, pnr, status, data_rezerwacji, bagaz, koszt_calkowity) VALUES 
        (1, 2, 1, '37UEA1', 'Aktywna', '2026-04-29 18:22:57', 'Brak (Tylko podręczny)', 300.00),
        (2, 2, 27, '71Q6LD', 'Aktywna', '2026-04-29 18:41:30', 'Rejestrowany 20kg (+150 PLN)', 300.00),
        (3, 2, 27, 'VP14MP', 'Aktywna', '2026-04-29 18:41:40', 'Rejestrowany 20kg (+150 PLN)', 300.00),
        (4, 2, 27, '5HKNDR', 'Aktywna', '2026-04-29 18:41:48', 'Rejestrowany 20kg (+150 PLN)', 300.00)
        ON CONFLICT (pnr) DO NOTHING;
        """,
        "SELECT setval('rezerwacje_lotow_id_rezerwacji_seq', (SELECT COALESCE(MAX(id_rezerwacji), 1) FROM rezerwacje_lotow));",

        """
        INSERT INTO rezerwacje_parkingu (id_rezerwacji_parkingu, id_konta, rodzaj_parkingu, rodzaj_pojazdu, data_przyjazdu, data_wyjazdu, status, cena_calkowita, nr_rejestracyjny) VALUES 
        (1, 12, 'Długoterminowy', 'Standardowy Samochód Osobowy', '2026-11-10 10:00:00', '2026-11-11 12:00:00', 'oczekujaca', NULL, 'KNS 1656'),
        (2, 2, 'Krótkoterminowy', 'Standardowy Samochód Osobowy', '2026-05-14 18:06:00', '2026-05-29 18:06:00', 'oczekujaca', NULL, 'KLI 12345')
        ON CONFLICT (id_rezerwacji_parkingu) DO NOTHING;
        """,
        "SELECT setval('rezerwacje_parkingu_id_rezerwacji_parkingu_seq', (SELECT COALESCE(MAX(id_rezerwacji_parkingu), 1) FROM rezerwacje_parkingu));"
    ]

    try:
        cursor = conn.cursor()
        print(f"Wgrywanie danych ...")
        
        for sql in zapytania:
            cursor.execute(sql)
            
        conn.commit()
        print("Dane testowe zostały wgrane do bazy danych")
    except Exception as e:
        conn.rollback()
        print(f"Błąd wgrywania danych: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    wgraj_dane_testowe()