--
-- PostgreSQL database dump
--

\restrict ZsC5kxgkqBO082M0aDbmWEjk6R4qRzX6w4wYzjnZbp7rEG2tQrvoOrB1gf9t12Z

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-04-15 12:18:00

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
-- TOC entry 4965 (class 0 OID 0)
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
-- TOC entry 4966 (class 0 OID 0)
-- Dependencies: 223
-- Name: loty_id_lotu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.loty_id_lotu_seq OWNED BY public.loty.id_lotu;


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
-- TOC entry 4967 (class 0 OID 0)
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
-- TOC entry 4968 (class 0 OID 0)
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
-- TOC entry 4969 (class 0 OID 0)
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
    status character varying(50) DEFAULT 'Zarezerwowany'::character varying
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
-- TOC entry 4970 (class 0 OID 0)
-- Dependencies: 227
-- Name: rezerwacje_parkingu_id_rezerwacji_parkingu_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq OWNED BY public.rezerwacje_parkingu.id_rezerwacji_parkingu;


--
-- TOC entry 4767 (class 2604 OID 16433)
-- Name: konta id_konta; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta ALTER COLUMN id_konta SET DEFAULT nextval('public.konta_id_konta_seq'::regclass);


--
-- TOC entry 4771 (class 2604 OID 16473)
-- Name: loty id_lotu; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.loty ALTER COLUMN id_lotu SET DEFAULT nextval('public.loty_id_lotu_seq'::regclass);


--
-- TOC entry 4769 (class 2604 OID 16445)
-- Name: pasazerowie id_pasazera; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie ALTER COLUMN id_pasazera SET DEFAULT nextval('public.pasazerowie_id_pasazera_seq'::regclass);


--
-- TOC entry 4770 (class 2604 OID 16459)
-- Name: pracownicy id_pracownika; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy ALTER COLUMN id_pracownika SET DEFAULT nextval('public.pracownicy_id_pracownika_seq'::regclass);


--
-- TOC entry 4773 (class 2604 OID 16481)
-- Name: rezerwacje_lotow id_rezerwacji; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow ALTER COLUMN id_rezerwacji SET DEFAULT nextval('public.rezerwacje_lotow_id_rezerwacji_seq'::regclass);


--
-- TOC entry 4776 (class 2604 OID 16502)
-- Name: rezerwacje_parkingu id_rezerwacji_parkingu; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu ALTER COLUMN id_rezerwacji_parkingu SET DEFAULT nextval('public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq'::regclass);


--
-- TOC entry 4949 (class 0 OID 16430)
-- Dependencies: 218
-- Data for Name: konta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.konta (id_konta, email, haslo, rola) FROM stdin;
1	admin@skyport.pl	$2b$12$DUDhbIBuf9iMymg659RV1.r9DDFI8jdgw42BrWdXy4v.xXGuzrbiW	admin
2	test@test.com	$2b$12$soZ4ZA1J.wNa7Kw9PE5Adu891rp25WgjxaZFrZ0ixmId8xDVnEv5y	pasazer
\.


--
-- TOC entry 4955 (class 0 OID 16470)
-- Dependencies: 224
-- Data for Name: loty; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.loty (id_lotu, numer_lotu, kierunek, planowo, bramka, status) FROM stdin;
1	BA123	Londyn Heathrow	2026-04-15 14:30:00	A12	Boarding
2	LH456	Frankfurt	2026-04-15 14:45:00	B04	O czasie
3	AF789	Paryż CDG	2026-04-15 15:00:00	A08	O czasie
4	KL321	Amsterdam	2026-04-15 15:15:00	B11	Opóźniony
5	EI654	Dublin	2026-04-15 15:30:00	A15	O czasie
\.


--
-- TOC entry 4951 (class 0 OID 16442)
-- Dependencies: 220
-- Data for Name: pasazerowie; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pasazerowie (id_pasazera, id_konta, imie, nazwisko) FROM stdin;
1	2	Grzegorz	Twaróg
\.


--
-- TOC entry 4953 (class 0 OID 16456)
-- Dependencies: 222
-- Data for Name: pracownicy; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pracownicy (id_pracownika, id_konta, imie, nazwisko, stanowisko) FROM stdin;
\.


--
-- TOC entry 4957 (class 0 OID 16478)
-- Dependencies: 226
-- Data for Name: rezerwacje_lotow; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rezerwacje_lotow (id_rezerwacji, id_konta, id_lotu, pnr, status, data_rezerwacji) FROM stdin;
\.


--
-- TOC entry 4959 (class 0 OID 16499)
-- Dependencies: 228
-- Data for Name: rezerwacje_parkingu; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.rezerwacje_parkingu (id_rezerwacji_parkingu, id_konta, rodzaj_parkingu, rodzaj_pojazdu, data_przyjazdu, data_wyjazdu, status) FROM stdin;
\.


--
-- TOC entry 4971 (class 0 OID 0)
-- Dependencies: 217
-- Name: konta_id_konta_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.konta_id_konta_seq', 2, true);


--
-- TOC entry 4972 (class 0 OID 0)
-- Dependencies: 223
-- Name: loty_id_lotu_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.loty_id_lotu_seq', 5, true);


--
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 219
-- Name: pasazerowie_id_pasazera_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pasazerowie_id_pasazera_seq', 1, true);


--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 221
-- Name: pracownicy_id_pracownika_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pracownicy_id_pracownika_seq', 1, false);


--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 225
-- Name: rezerwacje_lotow_id_rezerwacji_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rezerwacje_lotow_id_rezerwacji_seq', 1, false);


--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 227
-- Name: rezerwacje_parkingu_id_rezerwacji_parkingu_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rezerwacje_parkingu_id_rezerwacji_parkingu_seq', 1, false);


--
-- TOC entry 4779 (class 2606 OID 16440)
-- Name: konta konta_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta
    ADD CONSTRAINT konta_email_key UNIQUE (email);


--
-- TOC entry 4781 (class 2606 OID 16438)
-- Name: konta konta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.konta
    ADD CONSTRAINT konta_pkey PRIMARY KEY (id_konta);


--
-- TOC entry 4791 (class 2606 OID 16476)
-- Name: loty loty_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.loty
    ADD CONSTRAINT loty_pkey PRIMARY KEY (id_lotu);


--
-- TOC entry 4783 (class 2606 OID 16449)
-- Name: pasazerowie pasazerowie_id_konta_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_id_konta_key UNIQUE (id_konta);


--
-- TOC entry 4785 (class 2606 OID 16447)
-- Name: pasazerowie pasazerowie_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_pkey PRIMARY KEY (id_pasazera);


--
-- TOC entry 4787 (class 2606 OID 16463)
-- Name: pracownicy pracownicy_id_konta_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_id_konta_key UNIQUE (id_konta);


--
-- TOC entry 4789 (class 2606 OID 16461)
-- Name: pracownicy pracownicy_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_pkey PRIMARY KEY (id_pracownika);


--
-- TOC entry 4793 (class 2606 OID 16485)
-- Name: rezerwacje_lotow rezerwacje_lotow_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_pkey PRIMARY KEY (id_rezerwacji);


--
-- TOC entry 4795 (class 2606 OID 16487)
-- Name: rezerwacje_lotow rezerwacje_lotow_pnr_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_pnr_key UNIQUE (pnr);


--
-- TOC entry 4797 (class 2606 OID 16505)
-- Name: rezerwacje_parkingu rezerwacje_parkingu_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu
    ADD CONSTRAINT rezerwacje_parkingu_pkey PRIMARY KEY (id_rezerwacji_parkingu);


--
-- TOC entry 4798 (class 2606 OID 16450)
-- Name: pasazerowie pasazerowie_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pasazerowie
    ADD CONSTRAINT pasazerowie_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4799 (class 2606 OID 16464)
-- Name: pracownicy pracownicy_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pracownicy
    ADD CONSTRAINT pracownicy_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4800 (class 2606 OID 16488)
-- Name: rezerwacje_lotow rezerwacje_lotow_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


--
-- TOC entry 4801 (class 2606 OID 16493)
-- Name: rezerwacje_lotow rezerwacje_lotow_id_lotu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_lotow
    ADD CONSTRAINT rezerwacje_lotow_id_lotu_fkey FOREIGN KEY (id_lotu) REFERENCES public.loty(id_lotu) ON DELETE CASCADE;


--
-- TOC entry 4802 (class 2606 OID 16506)
-- Name: rezerwacje_parkingu rezerwacje_parkingu_id_konta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rezerwacje_parkingu
    ADD CONSTRAINT rezerwacje_parkingu_id_konta_fkey FOREIGN KEY (id_konta) REFERENCES public.konta(id_konta) ON DELETE CASCADE;


-- Completed on 2026-04-15 12:18:00

--
-- PostgreSQL database dump complete
--

\unrestrict ZsC5kxgkqBO082M0aDbmWEjk6R4qRzX6w4wYzjnZbp7rEG2tQrvoOrB1gf9t12Z

