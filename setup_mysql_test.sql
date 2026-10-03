-- Create the test database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Give the user all privileges on the test database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Give the user SELECT privilege on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

FLUSH PRIVILEGES;
