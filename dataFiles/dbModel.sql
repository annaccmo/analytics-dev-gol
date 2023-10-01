-- database

CREATE DATABASE analystic_gol;
USE analystic_gol;

-- user
CREATE TABLE user 
    (id INT NOT NULL AUTO_INCREMENT primary key, 
    username VARCHAR(255), name VARCHAR(255),
    last_login DATETIME, create_user DATETIME,
    password VARCHAR(255));

-- analytic_data
CREATE TABLE analytic_data 
    (id INT NOT NULL AUTO_INCREMENT primary key, 
    date_year YEAR, date_month INT,
    market VARCHAR(255), rpk INT);
	
-- log_query
CREATE TABLE log_query 
    (id INT NOT NULL AUTO_INCREMENT primary key, 
    user_id INT NOT NULL,
    log_timestamp TIMESTAMP,
    market VARCHAR(255),
    year_begin YEAR, month_begin INT,	
	year_end YEAR, month_end INT);

ALTER TABLE log_query add foreign key(user_id) references user(id);
	
-- log_analytic 
CREATE TABLE log_analytic
	(log_id INT NOT NULL,
	analytic_id INT NOT NULL);

ALTER TABLE log_analytic add foreign key(log_id) references log_query(id);
ALTER TABLE log_analytic add foreign key(analytic_id) references analytic_data(id);


