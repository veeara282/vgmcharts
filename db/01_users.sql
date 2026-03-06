-- Creates the second database user and grants access.
-- Credentials are read from the container environment (set in docker-compose via .env).

\getenv pguser2 POSTGRES_USER2
\getenv pgpassword2 POSTGRES_PASSWORD2
\getenv pgdb POSTGRES_DB

SELECT format('CREATE USER %I WITH PASSWORD %L', :'pguser2', :'pgpassword2') \gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'pgdb', :'pguser2') \gexec
SELECT format('GRANT USAGE ON SCHEMA public TO %I', :'pguser2') \gexec
SELECT format('GRANT SELECT ON ALL TABLES IN SCHEMA public TO %I', :'pguser2') \gexec
SELECT format(
  'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO %I',
  :'pguser2'
) \gexec
