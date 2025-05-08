-- -- Create databases
-- CREATE DATABASE files;
CREATE DATABASE analysis;

-- Create users with privileges
-- CREATE USER storing_user WITH PASSWORD 'storing_pass';
-- GRANT ALL PRIVILEGES ON DATABASE files TO storing_user;

CREATE USER analysis_user WITH PASSWORD 'analysis_pass';
GRANT ALL PRIVILEGES ON DATABASE analysis TO analysis_user;