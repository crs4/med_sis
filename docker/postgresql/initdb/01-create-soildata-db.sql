CREATE USER backoffice_user WITH PASSWORD 'backoffice_pwd';
CREATE DATABASE backoffice_db WITH OWNER backoffice_user;
\c soildata_db
CREATE EXTENSION postgis;
GRANT ALL PRIVILEGES ON DATABASE backoffice_db TO backoffice_user; 
