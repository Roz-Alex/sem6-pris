--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13 (Homebrew)

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

--
-- Name: mobile_dev; Type: DATABASE; Schema: -; Owner: entityfrm
--

CREATE DATABASE mobile_dev WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';


ALTER DATABASE mobile_dev OWNER TO entityfrm;

\connect mobile_dev

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
-- Name: affirmation; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.affirmation (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    category_id character varying NOT NULL,
    text character varying NOT NULL,
    image_url character varying,
    audio_url character varying,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.affirmation OWNER TO entityfrm;

--
-- Name: affirmationtag; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.affirmationtag (
    affirmation_id character varying NOT NULL,
    tag_id character varying NOT NULL
);


ALTER TABLE public.affirmationtag OWNER TO entityfrm;

--
-- Name: category; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.category (
    id character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.category OWNER TO entityfrm;

--
-- Name: educationalcontent; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.educationalcontent (
    id character varying NOT NULL,
    title character varying NOT NULL,
    content_type character varying NOT NULL,
    url character varying NOT NULL,
    description character varying
);


ALTER TABLE public.educationalcontent OWNER TO entityfrm;

--
-- Name: favorite; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.favorite (
    user_id character varying NOT NULL,
    affirmation_id character varying NOT NULL
);


ALTER TABLE public.favorite OWNER TO entityfrm;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.tag (
    id character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.tag OWNER TO entityfrm;

--
-- Name: user; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public."user" (
    id character varying NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public."user" OWNER TO entityfrm;

--
-- Name: userprogress; Type: TABLE; Schema: public; Owner: entityfrm
--

CREATE TABLE public.userprogress (
    id character varying NOT NULL,
    user_id character varying NOT NULL,
    affirmation_id character varying NOT NULL,
    date_used date NOT NULL,
    mood_note character varying,
    times_played integer NOT NULL
);


ALTER TABLE public.userprogress OWNER TO entityfrm;

--
-- Data for Name: affirmation; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: affirmationtag; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: educationalcontent; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: favorite; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: entityfrm
--

INSERT INTO public."user" (id, name, email, password_hash, created_at, updated_at) VALUES ('b02da5b5-74f2-4ae3-8568-7bcd2a7e7b6b', 'Иван Иванов', 'ivan1@example.com', '$2b$12$8gHN9zx8XBJQR8IF3WSL8.GJCbwPJ/Ywm99Qx2LgeQg7g1oHwRcDe', '2025-05-25 15:17:35.436242', '2025-05-25 15:17:35.436261');
INSERT INTO public."user" (id, name, email, password_hash, created_at, updated_at) VALUES ('9154116e-65af-4deb-a466-ad7c8503f2cd', 'John Doe', 'test@testing.com', '$2b$12$BhINRPqkhI2wt41I1w8WBOUPANfXOJjDYndVoRCcTQoOZ1baLzrLG', '2025-05-27 17:33:32.378436', '2025-05-27 17:33:32.37845');
INSERT INTO public."user" (id, name, email, password_hash, created_at, updated_at) VALUES ('00301f92-9071-4857-8701-ee7a0c89afdb', 'Ivan Ivanov', 'Ivan@test.com', '$2b$12$ieXQNFUrZC4s1pmMwbLVheuYhAScBvdi3MYrJ2aemFuxPUZEbhRDK', '2025-05-27 17:58:20.385015', '2025-05-27 17:58:20.385051');
INSERT INTO public."user" (id, name, email, password_hash, created_at, updated_at) VALUES ('03e23ad2-c0e9-4b1a-bd73-b1c335ab35a1', 'Alex R', 'Testing@trest.test', '$2b$12$sEoKU1h7JaHJGL922X5UI.fZtq2UuLxtSZPkiy/2DYFhQInzbCVU6', '2025-05-29 16:36:42.420809', '2025-05-29 16:36:42.420826');


--
-- Data for Name: userprogress; Type: TABLE DATA; Schema: public; Owner: entityfrm
--



--
-- Name: affirmation affirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmation
    ADD CONSTRAINT affirmation_pkey PRIMARY KEY (id);


--
-- Name: affirmationtag affirmationtag_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmationtag
    ADD CONSTRAINT affirmationtag_pkey PRIMARY KEY (affirmation_id, tag_id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: educationalcontent educationalcontent_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.educationalcontent
    ADD CONSTRAINT educationalcontent_pkey PRIMARY KEY (id);


--
-- Name: favorite favorite_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.favorite
    ADD CONSTRAINT favorite_pkey PRIMARY KEY (user_id, affirmation_id);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: userprogress userprogress_pkey; Type: CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.userprogress
    ADD CONSTRAINT userprogress_pkey PRIMARY KEY (id);


--
-- Name: affirmation affirmation_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmation
    ADD CONSTRAINT affirmation_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: affirmation affirmation_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmation
    ADD CONSTRAINT affirmation_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: affirmationtag affirmationtag_affirmation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmationtag
    ADD CONSTRAINT affirmationtag_affirmation_id_fkey FOREIGN KEY (affirmation_id) REFERENCES public.affirmation(id);


--
-- Name: affirmationtag affirmationtag_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.affirmationtag
    ADD CONSTRAINT affirmationtag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: favorite favorite_affirmation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.favorite
    ADD CONSTRAINT favorite_affirmation_id_fkey FOREIGN KEY (affirmation_id) REFERENCES public.affirmation(id);


--
-- Name: favorite favorite_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.favorite
    ADD CONSTRAINT favorite_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: userprogress userprogress_affirmation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.userprogress
    ADD CONSTRAINT userprogress_affirmation_id_fkey FOREIGN KEY (affirmation_id) REFERENCES public.affirmation(id);


--
-- Name: userprogress userprogress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: entityfrm
--

ALTER TABLE ONLY public.userprogress
    ADD CONSTRAINT userprogress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

