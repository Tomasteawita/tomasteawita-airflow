CREATE DATABASE tecnica_db;
CREATE USER tecnica WITH ENCRYPTED PASSWORD 'tecnica_password';
GRANT ALL PRIVILEGES ON DATABASE tecnica_db TO tecnica;

create schema dev;

CREATE TABLE IF NOT EXISTS tecnica_ml (
    id varchar(100),
    site_id varchar(100),
    title varchar(100),
    price decimal(10,2),
    thumbnail varchar(100),
    create_date date,
    primary key(id, create_date)
);