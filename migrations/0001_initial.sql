CREATE TABLE konta (
    id_konta SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    haslo VARCHAR(255) NOT NULL,
    rola VARCHAR(50) DEFAULT 'pasazer' NOT NULL
);

CREATE TABLE loty (
    id_lotu SERIAL PRIMARY KEY,
    numer_lotu VARCHAR(10) NOT NULL,
    kierunek VARCHAR(100) NOT NULL,
    planowo TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    bramka VARCHAR(10),
    status VARCHAR(50) DEFAULT 'O czasie',
    cena_bazowa NUMERIC(10,2) DEFAULT 300.00
);

CREATE TABLE parkingi (
    id_parkingu SERIAL PRIMARY KEY,
    nazwa VARCHAR(50) UNIQUE NOT NULL,
    pojemnosc_total INTEGER NOT NULL,
    cena_bazowa NUMERIC(10,2)
);

CREATE TABLE pasazerowie (
    id_pasazera SERIAL PRIMARY KEY,
    id_konta INTEGER UNIQUE NOT NULL REFERENCES konta(id_konta) ON DELETE CASCADE,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL
);

CREATE TABLE pracownicy (
    id_pracownika SERIAL PRIMARY KEY,
    id_konta INTEGER UNIQUE NOT NULL REFERENCES konta(id_konta) ON DELETE CASCADE,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL,
    stanowisko VARCHAR(100) NOT NULL
);

CREATE TABLE rezerwacje_lotow (
    id_rezerwacji SERIAL PRIMARY KEY,
    id_konta INTEGER REFERENCES konta(id_konta) ON DELETE CASCADE,
    id_lotu INTEGER REFERENCES loty(id_lotu) ON DELETE CASCADE,
    pnr VARCHAR(6) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'Aktywna',
    data_rezerwacji TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    bagaz VARCHAR(100) DEFAULT 'Brak (Tylko podręczny)',
    koszt_calkowity NUMERIC(10,2) DEFAULT 300.00
);

CREATE TABLE rezerwacje_parkingu (
    id_rezerwacji_parkingu SERIAL PRIMARY KEY,
    id_konta INTEGER REFERENCES konta(id_konta) ON DELETE CASCADE,
    rodzaj_parkingu VARCHAR(50) NOT NULL,
    rodzaj_pojazdu VARCHAR(50),
    data_przyjazdu TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    data_wyjazdu TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'oczekujaca',
    cena_calkowita NUMERIC(10,2),
    nr_rejestracyjny VARCHAR(20)
);
