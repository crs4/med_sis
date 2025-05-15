CREATE USER backoffice_user WITH PASSWORD 'backoffice_pwd';
CREATE DATABASE backoffice WITH OWNER backoffice_user;
\c backoffice
CREATE EXTENSION postgis;
GRANT ALL PRIVILEGES ON DATABASE backoffice TO backoffice_user; 
