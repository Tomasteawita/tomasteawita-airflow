CREATE DATABASE tecnica_db;
CREATE USER tecnica WITH ENCRYPTED PASSWORD 'tecnica_password';
GRANT ALL PRIVILEGES ON DATABASE tecnica_db TO tecnica;

create schema dev;
