--
-- PostgreSQL database dump
--

\restrict Vb42GAohRkBnEKZIabfLgwRlVhT0GYA0uNFIoLZhET5CVSdcEeAMwdqO0VRPfhb

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-04-29 17:32:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16430)
-- Name: konta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.konta (
    id_konta integer NOT NULL,
    email character varying(255) NOT NULL,
    haslo character varying(255) NOT NULL,
    rola character varying(50) DEFAULT 'pasazer'::character varying NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 16429)
-- Name: konta_id_konta_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.konta_id_konta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 217
-- Name: konta_id_konta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.konta_id_konta_seq OWNED BY public.konta.id_konta;


--
-- TOC entry 224 (class 1259 OID 16470)
-- Name: loty; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.loty (
    id_lotu integer NOT NULL,
    numer_lotu character varying(10) NOT NULL,
    kierunek character varying(100) NOT NULL,
    planowo timestamp without time zone NOT NULL,
    bramka character varying(10),
    status character varying(50) DEFAULT 'O czasie'::character varying
);


--
-- TOC entry 223 (class 1259 OID 16469)
-- Name: loty_id_lotu_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.loty_id_lotu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 223
-- Name: loty_id_lotu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.loty_id_lotu_seq OWNED BY public.loty.id_lotu;


--
-- TOC entry 230 (class 1259 OID 24662)
-- Name: parkingi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parkingi (
    id_parkingu integer NOT NULL,
    nazwa character varying(50) NOT NULL,
    pojemnosc_total integer NOT NULL,
    cena_bazowa numeric(10,2)
);


--
-- TOC entry 229 (class 1259 OID 24661)
-- Name: parkingi_id_parkingu_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.parkingi_id_parkingu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 229
-- Name: parkingi_id_parkingu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.parkingi_id_parkingu_seq OWNED BY public.parkingi.id_parkingu;


--
-- TOC entry 220 (class 1259 OID 16442)
-- Name: pasazerowie; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pasazerowie (
    id_pasazera integer NOT NULL,
    id_konta integer NOT NULL,
    imie character varying(100) NOT NULL,
    nazwisko character varying(100) NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 16441)
-- Name: pasazerowie_id_pasazera_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pasazerowie_id_pasazera_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 219
-- Name: pasazerowie_id_pasazera_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pasazerowie_id_pasazera_seq OWNED BY public.pasazerowie.id_pasazera;


--
-- TOC entry 222 (class 1259 OID 16456)
-- Name: pracownicy; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pracownicy (
    id_pracownika integer NOT NULL,
    id_konta integer NOT NULL,
    imie character varying(100) NOT NULL,
    nazwisko character varying(100) NOT NULL,
    stanowisko character varying(100) NOT NULL
);


--
-- TOC entry 221 (class 1259 OID 16455)
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pracownicy_id_pracownika_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 221
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pracownicy_id_pracownika_seq OWNED BY public.pracownicy.id_pracownika;


--
-- TOC entry 226 (class 1259 OID 16478)
-- Name: rezerwacje_lotow; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rezerwacje_lotow (
    id_rezerwacji integer NOT NULL,
    id_konta integer,
    id_lotu integer,
    pnr character varying(6) NOT NULL,
    status character varying(50) DEFAULT 'Aktywna'::character varying,
    data_rezerwacji timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 225 (class 1259 OID 16477)
-- Name: rezerwacje_lotow_id_rezerwacji_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rezerwacje_lotow_id_rezerwacji_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 225
-- Name: rezerwacje_lotow_id_rezerwacji_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rezerwacje_lotow_id_rezerwacji_seq OWNED BY public.rezerwacje_lotow.id_rezerwacji;


--
-- TOC entry 228 (class 1259 OID 16499)
-- Name: rezerwacje_parkingu; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rezerwacje_parkingu (
    id_rezerwacji_parkingu integer NOT NULL,
    id_konta integer,
    rodzaj_parkingu character varying(50) NOT NULL,
    rodzaj_pojazdu character varying(50),
    data_przyjazdu timestamp without time zone NOT NULL,
    data_wyjazdu timestamp without time zone NOT NULL,
    status character varying(50) DEFAULT 'oczekujaca'::character varying,
    cena_calkowita numeric(10,2),
    nr_rejestracyjny character varying(20)
);


--
-- TOC entry 227 (class 1259 OID 16498)
-- Name: rezerwacje_parkingu_id_rezerwacji_parkingu_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 227
-- Name: rezerwacje_parkingu_id_rezerwacji_parkingu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq OWNED BY public.rezerwacje_parkingu.id_rezerwacji_parkingu;


--
-- TOC entry 4772 (class 2604 OID 16433)
-- Name: konta id_konta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta ALTER COLUMN id_konta SET DEFAULT nextval('public.konta_id_konta_seq'::regclass);


--
-- TOC entry 4776 (class 2604 OID 16473)
-- Name: loty id_lotu; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.loty ALTER COLUMN id_lotu SET DEFAULT nextval('public.loty_id_lotu_seq'::regclass);


--
-- TOC entry 4783 (class 2604 OID 24665)
-- Name: parkingi id_parkingu; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parkingi ALTER COLUMN id_parkingu SET DEFAULT nextval('public.parkingi_id_parkingu_seq'::regclass);


--
-- TOC entry 4774 (class 2604 OID 16445)
-- Name: pasazerowie id_pasazera; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie ALTER COLUMN id_pasazera SET DEFAULT nextval('public.pasazerowie_id_pasazera_seq'::regclass);


--
-- TOC entry 4775 (class 2604 OID 16459)
-- Name: pracownicy id_pracownika; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy ALTER COLUMN id_pracownika SET DEFAULT nextval('public.pracownicy_id_pracownika_seq'::regclass);


--
-- TOC entry 4778 (class 2604 OID 16481)
-- Name: rezerwacje_lotow id_rezerwacji; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow ALTER COLUMN id_rezerwacji SET DEFAULT nextval('public.rezerwacje_lotow_id_rezerwacji_seq'::regclass);


--
-- TOC entry 4781 (class 2604 OID 16502)
-- Name: rezerwacje_parkingu id_rezerwacji_parkingu; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu ALTER COLUMN id_rezerwacji_parkingu SET DEFAULT nextval('public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq'::regclass);


--
-- TOC entry 4959 (class 0 OID 16430)
-- Dependencies: 218
-- Data for Name: konta; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.konta VALUES (1, 'admin@skyport.pl', '$2b$12$DUDhbIBuf9iMymg659RV1.r9DDFI8jdgw42BrWdXy4v.xXGuzrbiW', 'admin');
INSERT INTO public.konta VALUES (2, 'test@test.com', '$2b$12$soZ4ZA1J.wNa7Kw9PE5Adu891rp25WgjxaZFrZ0ixmId8xDVnEv5y', 'pasazer');
INSERT INTO public.konta VALUES (3, 'Jan@skyport.pl', '$2b$12$5mq65o5rgrX2mLAR4YhxeOc0v7mEMUa31Sy.mBkEZf2E0cFae3fPO', 'pasazer');
INSERT INTO public.konta VALUES (4, 'pracownik1@skyport.pl', '$2b$12$saqNeU7kdRXsVZbKGxqct.4U2f6Tb5S.B/u6hXaLgd1T7XlrkFQLC', 'pracownik');
INSERT INTO public.konta VALUES (5, 'janek@skyport.pl', '$2b$12$G0tXVy2gw1lwQGZ0lLGPZOUhJL/cuu.akHJjJMAWrliaWhg6/BXHe', 'pasazer');
INSERT INTO public.konta VALUES (9, 'Dominik@skyport.pl', '$2b$12$yuPllojD8RivRrUgcJAo5uZsIgGe6TaIp0gQl/AR/s.XcizvyQ/uu', 'pasazer');
INSERT INTO public.konta VALUES (11, 'Dominikadmin@skyport.pl', '$2b$12$gep8FmQ4.2HvSzB1StoFH.HMilAZQhsYyfvgIQCbF0eDl6CG/h3py', 'admin');
INSERT INTO public.konta VALUES (12, 'Dominik2@skyport.pl', '$2b$12$.Z46f602ETxJKd8/7bL7S.FqUdHua5CNS.S5r34pyRN1o97geRz9e', 'pasazer');


--
-- TOC entry 4965 (class 0 OID 16470)
-- Dependencies: 224
-- Data for Name: loty; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.loty VALUES (1, 'BA123', 'Londyn Heathrow', '2026-04-15 14:30:00', 'A12', 'Boarding');
INSERT INTO public.loty VALUES (2, 'LH456', 'Frankfurt', '2026-04-15 14:45:00', 'B04', 'O czasie');
INSERT INTO public.loty VALUES (3, 'AF789', 'Paryż CDG', '2026-04-15 15:00:00', 'A08', 'O czasie');
INSERT INTO public.loty VALUES (4, 'KL321', 'Amsterdam', '2026-04-15 15:15:00', 'B11', 'Opóźniony');
INSERT INTO public.loty VALUES (5, 'EI654', 'Dublin', '2026-04-15 15:30:00', 'A15', 'O czasie');
INSERT INTO public.loty VALUES (6, 'LO392', 'Warszawa (WAW)', '2026-04-15 16:45:00', 'A02', 'O czasie');
INSERT INTO public.loty VALUES (7, 'RY847', 'Rzym (FCO)', '2026-04-15 17:10:00', 'B05', 'Boarding');
INSERT INTO public.loty VALUES (8, 'WZ102', 'Barcelona (BCN)', '2026-04-15 17:30:00', 'C12', 'O czasie');
INSERT INTO public.loty VALUES (9, 'AF444', 'Paryż (CDG)', '2026-04-15 18:00:00', 'A09', 'Opóźniony');
INSERT INTO public.loty VALUES (10, 'BA901', 'Londyn (LHR)', '2026-04-15 18:15:00', 'A14', 'O czasie');
INSERT INTO public.loty VALUES (11, 'SK722', 'Sztokholm (ARN)', '2026-04-15 18:45:00', 'B02', 'O czasie');
INSERT INTO public.loty VALUES (12, 'IB331', 'Madryt (MAD)', '2026-04-15 19:00:00', 'C08', 'O czasie');
INSERT INTO public.loty VALUES (13, 'EK202', 'Dubaj (DXB)', '2026-04-15 19:30:00', 'C03', 'Odprawa');
INSERT INTO public.loty VALUES (14, 'QR411', 'Doha (DOH)', '2026-04-15 20:00:00', 'A05', 'Odprawa');
INSERT INTO public.loty VALUES (15, 'TK199', 'Stambuł (IST)', '2026-04-15 20:20:00', 'C01', 'O czasie');
INSERT INTO public.loty VALUES (16, 'LO441', 'Wiedeń (VIE)', '2026-04-15 20:45:00', 'A04', 'Opóźniony');
INSERT INTO public.loty VALUES (17, 'EN291', 'Monachium (MUC)', '2026-04-15 21:10:00', 'B07', 'O czasie');
INSERT INTO public.loty VALUES (18, 'UA101', 'Nowy Jork (JFK)', '2026-04-16 06:30:00', 'C01', 'O czasie');
INSERT INTO public.loty VALUES (19, 'DL404', 'Atlanta (ATL)', '2026-04-16 07:00:00', 'A02', 'O czasie');
INSERT INTO public.loty VALUES (20, 'AC882', 'Toronto (YYZ)', '2026-04-16 07:45:00', 'B04', 'O czasie');
INSERT INTO public.loty VALUES (22, 'WZ334', 'Oslo (OSL)', '2026-04-16 08:50:00', 'C03', 'O czasie');
INSERT INTO public.loty VALUES (23, 'LO505', 'Praga (PRG)', '2026-04-16 09:10:00', 'A01', 'O czasie');
INSERT INTO public.loty VALUES (24, 'LX887', 'Zurych (ZRH)', '2026-04-16 09:40:00', 'B06', 'O czasie');
INSERT INTO public.loty VALUES (21, 'RY992', 'Mediolan (BGY)', '2026-04-16 08:15:00', 'B09', 'Opóźniony');
INSERT INTO public.loty VALUES (26, 'GR569', 'Kraków Kraków', '2026-04-21 09:00:00', 'C6', 'O czasie');
INSERT INTO public.loty VALUES (25, 'AY105', 'Helsinki (HEL)', '2026-04-16 10:15:00', 'C07', 'O czasie');


--
-- TOC entry 4971 (class 0 OID 24662)
-- Dependencies: 230
-- Data for Name: parkingi; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.parkingi VALUES (1, 'Krótkoterminowy', 100, 15.00);
INSERT INTO public.parkingi VALUES (2, 'Długoterminowy', 300, 45.00);
INSERT INTO public.parkingi VALUES (3, 'Premium', 50, 65.00);


--
-- TOC entry 4961 (class 0 OID 16442)
-- Dependencies: 220
-- Data for Name: pasazerowie; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.pasazerowie VALUES (1, 2, 'Grzegorz', 'Twaróg');
INSERT INTO public.pasazerowie VALUES (2, 3, 'Jan', 'Kowalski');
INSERT INTO public.pasazerowie VALUES (3, 4, 'Maciek', 'Wtylnowy');
INSERT INTO public.pasazerowie VALUES (4, 5, 'janek', 'wójcik');
INSERT INTO public.pasazerowie VALUES (5, 9, 'Dominik', 'Migacz');
INSERT INTO public.pasazerowie VALUES (6, 12, 'Dominik', 'migacz');


--
-- TOC entry 4963 (class 0 OID 16456)
-- Dependencies: 222
-- Data for Name: pracownicy; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.pracownicy VALUES (1, 11, 'dominikadmin', 'Migacz', 'Administrator');


--
-- TOC entry 4967 (class 0 OID 16478)
-- Dependencies: 226
-- Data for Name: rezerwacje_lotow; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 4969 (class 0 OID 16499)
-- Dependencies: 228
-- Data for Name: rezerwacje_parkingu; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rezerwacje_parkingu VALUES (1, 12, 'Długoterminowy', 'Standardowy Samochód Osobowy', '2026-11-10 10:00:00', '2026-11-11 12:00:00', 'oczekujaca', NULL, 'KNS 1656');


--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 217
-- Name: konta_id_konta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.konta_id_konta_seq', 12, true);


--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 223
-- Name: loty_id_lotu_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.loty_id_lotu_seq', 26, true);


--
-- TOC entry 4986 (class 0 OID 0)
-- Dependencies: 229
-- Name: parkingi_id_parkingu_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.parkingi_id_parkingu_seq', 3, true);


--
-- TOC entry 4987 (class 0 OID 0)
-- Dependencies: 219
-- Name: pasazerowie_id_pasazera_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pasazerowie_id_pasazera_seq', 6, true);


--
-- TOC entry 4988 (class 0 OID 0)
-- Dependencies: 221
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pracownicy_id_pracownika_seq', 1, true);


--
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 225
-- Name: rezerwacje_lotow_id_rezerwacji_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rezerwacje_lotow_id_rezerwacji_seq', 1, false);


--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 227
-- Name: rezerwacje_parkingu_id_rezerwacji_parkingu_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq', 1, true);


--
-- TOC entry 4785 (class 2606 OID 16440)
-- Name: konta konta_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta
    ADD CONSTRAINT konta_email_key UNIQUE (email);


--
-- TOC entry 4787 (class 2606 OID 16438)
-- Name: konta konta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta
    ADD CONSTRAINT konta_pkey PRIMARY KEY (id_konta);


--
-- TOC entry 4797 (class 2606 OID 16476)
-- Name: loty loty_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.loty
    ADD CONSTRAINT loty_pkey PRIMARY KEY (id_lotu);


--
-- TOC entry 4805 (class 2606 OID 24669)
-- Name: parkingi parkingi_nazwa_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parkingi
    ADD CONSTRAINT parkingi_nazwa_key UNIQUE (nazwa);


--
-- TOC entry 4807 (class 2606 OID 24667)
-- Name: parkingi parkingi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parkingi
    ADD CONSTRAINT parkingi_pkey PRIMARY KEY (id_parkingu);


--
-- TOC entry 4789 (class 2606 OID 16449)
-- Name: pasazerowie pasazerowie_id_konta_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_id_konta_key UNIQUE (id_konta);


--
-- TOC entry 4791 (class 2606 OID 16447)
-- Name: pasazerowie pasazerowie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_pkey PRIMARY KEY (id_pasazera);


--
-- TOC entry 4793 (class 2606 OID 16463)
-- Name: pracownicy pracownicy_id_konta_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_id_konta_key UNIQUE (id_konta);


--
-- TOC entry 4795 (class 2606 OID 16461)
-- Name: pracownicy pracownicy_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_pkey PRIMARY KEY (id_pracownika);


--
-- TOC entry 4799 (class 2606 OID 16485)
-- Name: rezerwacje_lotow rezerwacje_lotow_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_pkey PRIMARY KEY (id_rezerwacji);


--
-- TOC entry 4801 (class 2606 OID 16487)
-- Name: rezerwacje_lotow rezerwacje_lotow_pnr_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_pnr_key UNIQUE (pnr);


--
-- TOC entry 4803 (class 2606 OID 16505)
-- Name: rezerwacje_parkingu rezerwacje_parkingu_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu
    ADD CONSTRAINT rezerwacje_parkingu_pkey PRIMARY KEY (id_rezerwacji_parkingu);


--
-- TOC entry 4808 (class 2606 OID 16450)
-- Name: pasazerowie pasazerowie_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4809 (class 2606 OID 16464)
-- Name: pracownicy pracownicy_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4810 (class 2606 OID 16488)
-- Name: rezerwacje_lotow rezerwacje_lotow_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4811 (class 2606 OID 16493)
-- Name: rezerwacje_lotow rezerwacje_lotow_id_lotu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_id_lotu_fkey FOREIGN KEY (id_lotu) REFERENCES public.loty(id_lotu) ON DELETE CASCADE;


--
-- TOC entry 4812 (class 2606 OID 16506)
-- Name: rezerwacje_parkingu rezerwacje_parkingu_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu
    ADD CONSTRAINT rezerwacje_parkingu_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


-- Completed on 2026-04-29 17:32:20

--
-- PostgreSQL database dump complete
--

\unrestrict Vb42GAohRkBnEKZIabfLgwRlVhT0GYA0uNFIoLZhET5CVSdcEeAMwdqO0VRPfhb

