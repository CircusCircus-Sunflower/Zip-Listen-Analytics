--
-- PostgreSQL database dump
--

\restrict 0MnaB7QchIjurwOfCCa9gW6AYy0TVgxKkFjtoF0ul9UV3NPke6DJXaqjqPrm0cN

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: auth_events; Type: TABLE; Schema: public; Owner: zipuser
--

CREATE TABLE public.auth_events (
    id integer NOT NULL,
    success boolean,
    "userId" character varying,
    state character varying,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.auth_events OWNER TO zipuser;

--
-- Name: auth_events_id_seq; Type: SEQUENCE; Schema: public; Owner: zipuser
--

CREATE SEQUENCE public.auth_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_events_id_seq OWNER TO zipuser;

--
-- Name: auth_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zipuser
--

ALTER SEQUENCE public.auth_events_id_seq OWNED BY public.auth_events.id;


--
-- Name: listen_events; Type: TABLE; Schema: public; Owner: zipuser
--

CREATE TABLE public.listen_events (
    id integer NOT NULL,
    artist character varying,
    song character varying,
    duration double precision,
    "userId" character varying,
    state character varying,
    level character varying,
    genre character varying,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.listen_events OWNER TO zipuser;

--
-- Name: listen_events_id_seq; Type: SEQUENCE; Schema: public; Owner: zipuser
--

CREATE SEQUENCE public.listen_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.listen_events_id_seq OWNER TO zipuser;

--
-- Name: listen_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zipuser
--

ALTER SEQUENCE public.listen_events_id_seq OWNED BY public.listen_events.id;


--
-- Name: status_change_events; Type: TABLE; Schema: public; Owner: zipuser
--

CREATE TABLE public.status_change_events (
    id integer NOT NULL,
    level character varying,
    "userId" character varying,
    state character varying,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.status_change_events OWNER TO zipuser;

--
-- Name: status_change_events_id_seq; Type: SEQUENCE; Schema: public; Owner: zipuser
--

CREATE SEQUENCE public.status_change_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_change_events_id_seq OWNER TO zipuser;

--
-- Name: status_change_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zipuser
--

ALTER SEQUENCE public.status_change_events_id_seq OWNED BY public.status_change_events.id;


--
-- Name: auth_events id; Type: DEFAULT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.auth_events ALTER COLUMN id SET DEFAULT nextval('public.auth_events_id_seq'::regclass);


--
-- Name: listen_events id; Type: DEFAULT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.listen_events ALTER COLUMN id SET DEFAULT nextval('public.listen_events_id_seq'::regclass);


--
-- Name: status_change_events id; Type: DEFAULT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.status_change_events ALTER COLUMN id SET DEFAULT nextval('public.status_change_events_id_seq'::regclass);


--
-- Data for Name: auth_events; Type: TABLE DATA; Schema: public; Owner: zipuser
--

COPY public.auth_events (id, success, "userId", state, "timestamp") FROM stdin;
\.


--
-- Data for Name: listen_events; Type: TABLE DATA; Schema: public; Owner: zipuser
--

COPY public.listen_events (id, artist, song, duration, "userId", state, level, genre, "timestamp") FROM stdin;
\.


--
-- Data for Name: status_change_events; Type: TABLE DATA; Schema: public; Owner: zipuser
--

COPY public.status_change_events (id, level, "userId", state, "timestamp") FROM stdin;
\.


--
-- Name: auth_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zipuser
--

SELECT pg_catalog.setval('public.auth_events_id_seq', 1, false);


--
-- Name: listen_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zipuser
--

SELECT pg_catalog.setval('public.listen_events_id_seq', 1, false);


--
-- Name: status_change_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zipuser
--

SELECT pg_catalog.setval('public.status_change_events_id_seq', 1, false);


--
-- Name: auth_events auth_events_pkey; Type: CONSTRAINT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.auth_events
    ADD CONSTRAINT auth_events_pkey PRIMARY KEY (id);


--
-- Name: listen_events listen_events_pkey; Type: CONSTRAINT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.listen_events
    ADD CONSTRAINT listen_events_pkey PRIMARY KEY (id);


--
-- Name: status_change_events status_change_events_pkey; Type: CONSTRAINT; Schema: public; Owner: zipuser
--

ALTER TABLE ONLY public.status_change_events
    ADD CONSTRAINT status_change_events_pkey PRIMARY KEY (id);


--
-- Name: ix_auth_events_id; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_auth_events_id ON public.auth_events USING btree (id);


--
-- Name: ix_auth_events_state; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_auth_events_state ON public.auth_events USING btree (state);


--
-- Name: ix_auth_events_userId; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX "ix_auth_events_userId" ON public.auth_events USING btree ("userId");


--
-- Name: ix_listen_events_artist; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_listen_events_artist ON public.listen_events USING btree (artist);


--
-- Name: ix_listen_events_genre; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_listen_events_genre ON public.listen_events USING btree (genre);


--
-- Name: ix_listen_events_id; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_listen_events_id ON public.listen_events USING btree (id);


--
-- Name: ix_listen_events_level; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_listen_events_level ON public.listen_events USING btree (level);


--
-- Name: ix_listen_events_state; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_listen_events_state ON public.listen_events USING btree (state);


--
-- Name: ix_listen_events_userId; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX "ix_listen_events_userId" ON public.listen_events USING btree ("userId");


--
-- Name: ix_status_change_events_id; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_status_change_events_id ON public.status_change_events USING btree (id);


--
-- Name: ix_status_change_events_level; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_status_change_events_level ON public.status_change_events USING btree (level);


--
-- Name: ix_status_change_events_state; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX ix_status_change_events_state ON public.status_change_events USING btree (state);


--
-- Name: ix_status_change_events_userId; Type: INDEX; Schema: public; Owner: zipuser
--

CREATE INDEX "ix_status_change_events_userId" ON public.status_change_events USING btree ("userId");


--
-- PostgreSQL database dump complete
--

\unrestrict 0MnaB7QchIjurwOfCCa9gW6AYy0TVgxKkFjtoF0ul9UV3NPke6DJXaqjqPrm0cN

