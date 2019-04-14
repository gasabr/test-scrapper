CREATE USER gasabr WITH PASSWORD 'password';
update pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'app_vacancy';
-- CREATE DATABASE scrapping WITH OWNER gasabr;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gasabr;
