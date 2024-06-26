--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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
-- Name: marmut; Type: SCHEMA; Schema: -; Owner: basdat
--

CREATE SCHEMA marmut;


ALTER SCHEMA marmut OWNER TO basdat;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: akun; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.akun (
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    nama character varying(100) NOT NULL,
    gender integer NOT NULL,
    tempat_lahir character varying(50) NOT NULL,
    tanggal_lahir date NOT NULL,
    is_verified boolean NOT NULL,
    kota_asal character varying(50) NOT NULL,
    CONSTRAINT akun_gender_check CHECK ((gender = ANY (ARRAY[0, 1])))
);


ALTER TABLE marmut.akun OWNER TO basdat;

--
-- Name: akun_play_song; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.akun_play_song (
    email_pemain character varying(50) NOT NULL,
    id_song uuid NOT NULL,
    waktu timestamp without time zone NOT NULL
);


ALTER TABLE marmut.akun_play_song OWNER TO basdat;

--
-- Name: akun_play_user_playlist; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.akun_play_user_playlist (
    email_pemain character varying(50) NOT NULL,
    id_user_playlist uuid NOT NULL,
    email_pembuat character varying(50) NOT NULL,
    waktu timestamp without time zone NOT NULL
);


ALTER TABLE marmut.akun_play_user_playlist OWNER TO basdat;

--
-- Name: album; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.album (
    id uuid NOT NULL,
    judul character varying(100) NOT NULL,
    jumlah_lagu integer DEFAULT 0 NOT NULL,
    id_label uuid,
    total_durasi integer DEFAULT 0 NOT NULL
);


ALTER TABLE marmut.album OWNER TO basdat;

--
-- Name: artist; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.artist (
    id uuid NOT NULL,
    email_akun character varying(50),
    id_pemilik_hak_cipta uuid
);


ALTER TABLE marmut.artist OWNER TO basdat;

--
-- Name: chart; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.chart (
    tipe character varying(50) NOT NULL,
    id_playlist uuid
);


ALTER TABLE marmut.chart OWNER TO basdat;

--
-- Name: downloaded_song; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.downloaded_song (
    id_song uuid NOT NULL,
    email_downloader character varying(50) NOT NULL
);


ALTER TABLE marmut.downloaded_song OWNER TO basdat;

--
-- Name: episode; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.episode (
    id_episode uuid NOT NULL,
    id_konten_podcast uuid,
    judul character varying(100) NOT NULL,
    deskripsi character varying(500) NOT NULL,
    durasi integer NOT NULL,
    tanggal_rilis date NOT NULL
);


ALTER TABLE marmut.episode OWNER TO basdat;

--
-- Name: genre; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.genre (
    id_konten uuid NOT NULL,
    genre character varying(50) NOT NULL
);


ALTER TABLE marmut.genre OWNER TO basdat;

--
-- Name: konten; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.konten (
    id uuid NOT NULL,
    judul character varying(100) NOT NULL,
    tanggal_rilis date NOT NULL,
    tahun integer NOT NULL,
    durasi integer NOT NULL
);


ALTER TABLE marmut.konten OWNER TO basdat;

--
-- Name: label; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.label (
    id uuid NOT NULL,
    nama character varying(100) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    kontak character varying(50) NOT NULL,
    id_pemilik_hak_cipta uuid
);


ALTER TABLE marmut.label OWNER TO basdat;

--
-- Name: nonpremium; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.nonpremium (
    email character varying(50) NOT NULL
);


ALTER TABLE marmut.nonpremium OWNER TO basdat;

--
-- Name: paket; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.paket (
    jenis character varying(50) NOT NULL,
    harga integer NOT NULL
);


ALTER TABLE marmut.paket OWNER TO basdat;

--
-- Name: pemilik_hak_cipta; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.pemilik_hak_cipta (
    id uuid NOT NULL,
    rate_royalti integer NOT NULL
);


ALTER TABLE marmut.pemilik_hak_cipta OWNER TO basdat;

--
-- Name: playlist; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.playlist (
    id uuid NOT NULL
);


ALTER TABLE marmut.playlist OWNER TO basdat;

--
-- Name: playlist_song; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.playlist_song (
    id_playlist uuid NOT NULL,
    id_song uuid NOT NULL
);


ALTER TABLE marmut.playlist_song OWNER TO basdat;

--
-- Name: podcast; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.podcast (
    id_konten uuid NOT NULL,
    email_podcaster character varying(50)
);


ALTER TABLE marmut.podcast OWNER TO basdat;

--
-- Name: podcaster; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.podcaster (
    email character varying(50) NOT NULL
);


ALTER TABLE marmut.podcaster OWNER TO basdat;

--
-- Name: premium; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.premium (
    email character varying(50) NOT NULL
);


ALTER TABLE marmut.premium OWNER TO basdat;

--
-- Name: royalti; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.royalti (
    id_pemilik_hak_cipta uuid NOT NULL,
    id_song uuid NOT NULL,
    jumlah integer NOT NULL
);


ALTER TABLE marmut.royalti OWNER TO basdat;

--
-- Name: song; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.song (
    id_konten uuid NOT NULL,
    id_artist uuid,
    id_album uuid,
    total_play integer DEFAULT 0 NOT NULL,
    total_download integer DEFAULT 0 NOT NULL
);


ALTER TABLE marmut.song OWNER TO basdat;

--
-- Name: songwriter; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.songwriter (
    id uuid NOT NULL,
    email_akun character varying(50),
    id_pemilik_hak_cipta uuid
);


ALTER TABLE marmut.songwriter OWNER TO basdat;

--
-- Name: songwriter_write_song; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.songwriter_write_song (
    id_songwriter uuid NOT NULL,
    id_song uuid NOT NULL
);


ALTER TABLE marmut.songwriter_write_song OWNER TO basdat;

--
-- Name: transaction; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.transaction (
    id uuid NOT NULL,
    jenis_paket character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    timestamp_dimulai timestamp without time zone NOT NULL,
    timestamp_berakhir timestamp without time zone NOT NULL,
    metode_bayar character varying(50) NOT NULL,
    nominal integer NOT NULL
);


ALTER TABLE marmut.transaction OWNER TO basdat;

--
-- Name: user_playlist; Type: TABLE; Schema: marmut; Owner: basdat
--

CREATE TABLE marmut.user_playlist (
    email_pembuat character varying(50) NOT NULL,
    id_user_playlist uuid NOT NULL,
    judul character varying(100) NOT NULL,
    deskripsi character varying(500) NOT NULL,
    jumlah_lagu integer NOT NULL,
    tanggal_dibuat date NOT NULL,
    id_playlist uuid,
    total_durasi integer DEFAULT 0 NOT NULL
);


ALTER TABLE marmut.user_playlist OWNER TO basdat;

--
-- Data for Name: akun; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) FROM stdin;
abc@abc.com	abc	abc	1	abc	2024-04-29	f	None
\.


--
-- Data for Name: akun_play_song; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.akun_play_song (email_pemain, id_song, waktu) FROM stdin;
\.


--
-- Data for Name: akun_play_user_playlist; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu) FROM stdin;
\.


--
-- Data for Name: album; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.album (id, judul, jumlah_lagu, id_label, total_durasi) FROM stdin;
\.


--
-- Data for Name: artist; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.artist (id, email_akun, id_pemilik_hak_cipta) FROM stdin;
\.


--
-- Data for Name: chart; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.chart (tipe, id_playlist) FROM stdin;
\.


--
-- Data for Name: downloaded_song; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.downloaded_song (id_song, email_downloader) FROM stdin;
\.


--
-- Data for Name: episode; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) FROM stdin;
\.


--
-- Data for Name: genre; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.genre (id_konten, genre) FROM stdin;
\.


--
-- Data for Name: konten; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.konten (id, judul, tanggal_rilis, tahun, durasi) FROM stdin;
\.


--
-- Data for Name: label; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.label (id, nama, email, password, kontak, id_pemilik_hak_cipta) FROM stdin;
\.


--
-- Data for Name: nonpremium; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.nonpremium (email) FROM stdin;
\.


--
-- Data for Name: paket; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.paket (jenis, harga) FROM stdin;
\.


--
-- Data for Name: pemilik_hak_cipta; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.pemilik_hak_cipta (id, rate_royalti) FROM stdin;
\.


--
-- Data for Name: playlist; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.playlist (id) FROM stdin;
\.


--
-- Data for Name: playlist_song; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.playlist_song (id_playlist, id_song) FROM stdin;
\.


--
-- Data for Name: podcast; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.podcast (id_konten, email_podcaster) FROM stdin;
\.


--
-- Data for Name: podcaster; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.podcaster (email) FROM stdin;
\.


--
-- Data for Name: premium; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.premium (email) FROM stdin;
\.


--
-- Data for Name: royalti; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.royalti (id_pemilik_hak_cipta, id_song, jumlah) FROM stdin;
\.


--
-- Data for Name: song; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.song (id_konten, id_artist, id_album, total_play, total_download) FROM stdin;
\.


--
-- Data for Name: songwriter; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.songwriter (id, email_akun, id_pemilik_hak_cipta) FROM stdin;
\.


--
-- Data for Name: songwriter_write_song; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.songwriter_write_song (id_songwriter, id_song) FROM stdin;
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.transaction (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) FROM stdin;
\.


--
-- Data for Name: user_playlist; Type: TABLE DATA; Schema: marmut; Owner: basdat
--

COPY marmut.user_playlist (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) FROM stdin;
\.


--
-- Name: akun akun_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun
    ADD CONSTRAINT akun_pkey PRIMARY KEY (email);


--
-- Name: akun_play_song akun_play_song_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_song
    ADD CONSTRAINT akun_play_song_pkey PRIMARY KEY (email_pemain, id_song, waktu);


--
-- Name: akun_play_user_playlist akun_play_user_playlist_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_user_playlist
    ADD CONSTRAINT akun_play_user_playlist_pkey PRIMARY KEY (email_pemain, id_user_playlist, email_pembuat, waktu);


--
-- Name: album album_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.album
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: chart chart_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.chart
    ADD CONSTRAINT chart_pkey PRIMARY KEY (tipe);


--
-- Name: downloaded_song downloaded_song_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.downloaded_song
    ADD CONSTRAINT downloaded_song_pkey PRIMARY KEY (id_song, email_downloader);


--
-- Name: episode episode_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.episode
    ADD CONSTRAINT episode_pkey PRIMARY KEY (id_episode);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id_konten, genre);


--
-- Name: konten konten_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.konten
    ADD CONSTRAINT konten_pkey PRIMARY KEY (id);


--
-- Name: label label_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.label
    ADD CONSTRAINT label_pkey PRIMARY KEY (id);


--
-- Name: nonpremium nonpremium_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.nonpremium
    ADD CONSTRAINT nonpremium_pkey PRIMARY KEY (email);


--
-- Name: paket paket_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.paket
    ADD CONSTRAINT paket_pkey PRIMARY KEY (jenis);


--
-- Name: pemilik_hak_cipta pemilik_hak_cipta_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.pemilik_hak_cipta
    ADD CONSTRAINT pemilik_hak_cipta_pkey PRIMARY KEY (id);


--
-- Name: playlist playlist_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.playlist
    ADD CONSTRAINT playlist_pkey PRIMARY KEY (id);


--
-- Name: playlist_song playlist_song_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.playlist_song
    ADD CONSTRAINT playlist_song_pkey PRIMARY KEY (id_playlist, id_song);


--
-- Name: podcast podcast_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.podcast
    ADD CONSTRAINT podcast_pkey PRIMARY KEY (id_konten);


--
-- Name: podcaster podcaster_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.podcaster
    ADD CONSTRAINT podcaster_pkey PRIMARY KEY (email);


--
-- Name: premium premium_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.premium
    ADD CONSTRAINT premium_pkey PRIMARY KEY (email);


--
-- Name: royalti royalti_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.royalti
    ADD CONSTRAINT royalti_pkey PRIMARY KEY (id_pemilik_hak_cipta, id_song);


--
-- Name: song song_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.song
    ADD CONSTRAINT song_pkey PRIMARY KEY (id_konten);


--
-- Name: songwriter songwriter_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter
    ADD CONSTRAINT songwriter_pkey PRIMARY KEY (id);


--
-- Name: songwriter_write_song songwriter_write_song_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter_write_song
    ADD CONSTRAINT songwriter_write_song_pkey PRIMARY KEY (id_songwriter, id_song);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id, jenis_paket, email);


--
-- Name: user_playlist user_playlist_pkey; Type: CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.user_playlist
    ADD CONSTRAINT user_playlist_pkey PRIMARY KEY (email_pembuat, id_user_playlist);


--
-- Name: akun_play_song akun_play_song_email_pemain_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_song
    ADD CONSTRAINT akun_play_song_email_pemain_fkey FOREIGN KEY (email_pemain) REFERENCES marmut.akun(email);


--
-- Name: akun_play_song akun_play_song_id_song_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_song
    ADD CONSTRAINT akun_play_song_id_song_fkey FOREIGN KEY (id_song) REFERENCES marmut.song(id_konten);


--
-- Name: akun_play_user_playlist akun_play_user_playlist_email_pemain_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_user_playlist
    ADD CONSTRAINT akun_play_user_playlist_email_pemain_fkey FOREIGN KEY (email_pemain) REFERENCES marmut.akun(email);


--
-- Name: akun_play_user_playlist akun_play_user_playlist_id_user_playlist_email_pembuat_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.akun_play_user_playlist
    ADD CONSTRAINT akun_play_user_playlist_id_user_playlist_email_pembuat_fkey FOREIGN KEY (id_user_playlist, email_pembuat) REFERENCES marmut.user_playlist(id_user_playlist, email_pembuat);


--
-- Name: album album_id_label_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.album
    ADD CONSTRAINT album_id_label_fkey FOREIGN KEY (id_label) REFERENCES marmut.label(id);


--
-- Name: artist artist_email_akun_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.artist
    ADD CONSTRAINT artist_email_akun_fkey FOREIGN KEY (email_akun) REFERENCES marmut.akun(email);


--
-- Name: artist artist_id_pemilik_hak_cipta_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.artist
    ADD CONSTRAINT artist_id_pemilik_hak_cipta_fkey FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES marmut.pemilik_hak_cipta(id);


--
-- Name: chart chart_id_playlist_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.chart
    ADD CONSTRAINT chart_id_playlist_fkey FOREIGN KEY (id_playlist) REFERENCES marmut.playlist(id);


--
-- Name: downloaded_song downloaded_song_email_downloader_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.downloaded_song
    ADD CONSTRAINT downloaded_song_email_downloader_fkey FOREIGN KEY (email_downloader) REFERENCES marmut.premium(email);


--
-- Name: downloaded_song downloaded_song_id_song_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.downloaded_song
    ADD CONSTRAINT downloaded_song_id_song_fkey FOREIGN KEY (id_song) REFERENCES marmut.song(id_konten);


--
-- Name: episode episode_id_konten_podcast_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.episode
    ADD CONSTRAINT episode_id_konten_podcast_fkey FOREIGN KEY (id_konten_podcast) REFERENCES marmut.podcast(id_konten);


--
-- Name: genre genre_id_konten_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.genre
    ADD CONSTRAINT genre_id_konten_fkey FOREIGN KEY (id_konten) REFERENCES marmut.konten(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: label label_id_pemilik_hak_cipta_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.label
    ADD CONSTRAINT label_id_pemilik_hak_cipta_fkey FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES marmut.pemilik_hak_cipta(id);


--
-- Name: nonpremium nonpremium_email_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.nonpremium
    ADD CONSTRAINT nonpremium_email_fkey FOREIGN KEY (email) REFERENCES marmut.akun(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: playlist_song playlist_song_id_playlist_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.playlist_song
    ADD CONSTRAINT playlist_song_id_playlist_fkey FOREIGN KEY (id_playlist) REFERENCES marmut.playlist(id);


--
-- Name: playlist_song playlist_song_id_song_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.playlist_song
    ADD CONSTRAINT playlist_song_id_song_fkey FOREIGN KEY (id_song) REFERENCES marmut.song(id_konten);


--
-- Name: podcast podcast_email_podcaster_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.podcast
    ADD CONSTRAINT podcast_email_podcaster_fkey FOREIGN KEY (email_podcaster) REFERENCES marmut.podcaster(email);


--
-- Name: podcast podcast_id_konten_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.podcast
    ADD CONSTRAINT podcast_id_konten_fkey FOREIGN KEY (id_konten) REFERENCES marmut.konten(id);


--
-- Name: podcaster podcaster_email_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.podcaster
    ADD CONSTRAINT podcaster_email_fkey FOREIGN KEY (email) REFERENCES marmut.akun(email);


--
-- Name: premium premium_email_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.premium
    ADD CONSTRAINT premium_email_fkey FOREIGN KEY (email) REFERENCES marmut.akun(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: royalti royalti_id_pemilik_hak_cipta_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.royalti
    ADD CONSTRAINT royalti_id_pemilik_hak_cipta_fkey FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES marmut.pemilik_hak_cipta(id);


--
-- Name: royalti royalti_id_song_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.royalti
    ADD CONSTRAINT royalti_id_song_fkey FOREIGN KEY (id_song) REFERENCES marmut.song(id_konten);


--
-- Name: song song_id_album_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.song
    ADD CONSTRAINT song_id_album_fkey FOREIGN KEY (id_album) REFERENCES marmut.album(id);


--
-- Name: song song_id_artist_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.song
    ADD CONSTRAINT song_id_artist_fkey FOREIGN KEY (id_artist) REFERENCES marmut.artist(id);


--
-- Name: song song_id_konten_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.song
    ADD CONSTRAINT song_id_konten_fkey FOREIGN KEY (id_konten) REFERENCES marmut.konten(id);


--
-- Name: songwriter songwriter_email_akun_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter
    ADD CONSTRAINT songwriter_email_akun_fkey FOREIGN KEY (email_akun) REFERENCES marmut.akun(email);


--
-- Name: songwriter songwriter_id_pemilik_hak_cipta_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter
    ADD CONSTRAINT songwriter_id_pemilik_hak_cipta_fkey FOREIGN KEY (id_pemilik_hak_cipta) REFERENCES marmut.pemilik_hak_cipta(id);


--
-- Name: songwriter_write_song songwriter_write_song_id_song_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter_write_song
    ADD CONSTRAINT songwriter_write_song_id_song_fkey FOREIGN KEY (id_song) REFERENCES marmut.song(id_konten);


--
-- Name: songwriter_write_song songwriter_write_song_id_songwriter_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.songwriter_write_song
    ADD CONSTRAINT songwriter_write_song_id_songwriter_fkey FOREIGN KEY (id_songwriter) REFERENCES marmut.songwriter(id);


--
-- Name: transaction transaction_email_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.transaction
    ADD CONSTRAINT transaction_email_fkey FOREIGN KEY (email) REFERENCES marmut.akun(email) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction transaction_jenis_paket_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.transaction
    ADD CONSTRAINT transaction_jenis_paket_fkey FOREIGN KEY (jenis_paket) REFERENCES marmut.paket(jenis) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_playlist user_playlist_email_pembuat_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.user_playlist
    ADD CONSTRAINT user_playlist_email_pembuat_fkey FOREIGN KEY (email_pembuat) REFERENCES marmut.akun(email);


--
-- Name: user_playlist user_playlist_id_playlist_fkey; Type: FK CONSTRAINT; Schema: marmut; Owner: basdat
--

ALTER TABLE ONLY marmut.user_playlist
    ADD CONSTRAINT user_playlist_id_playlist_fkey FOREIGN KEY (id_playlist) REFERENCES marmut.playlist(id);


--
-- PostgreSQL database dump complete
--

