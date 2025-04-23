CREATE USER soildata_user WITH PASSWORD 'soildata_pwd';
CREATE DATABASE soildata_db WITH OWNER soildata_user;
\c soildata_db
CREATE EXTENSION postgis;
GRANT ALL PRIVILEGES ON DATABASE soildata_db TO soildata_user;
