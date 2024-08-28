CREATE DATABASE IF NOT EXISTS moviedatabase;

USE moviedatabase;

CREATE TABLE IF NOT EXISTS movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS theater (
    theater_id INT PRIMARY KEY,
    name VARCHAR(50),
    wide_area VARCHAR(10),
    basic_area VARCHAR(10)  
);

CREATE TABLE IF NOT EXISTS info (
    info_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT ,
    theater_id INT,
    time TIME,
    date DATE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (theater_id) REFERENCES theater(theater_id)
);

CREATE USER 'exporter'@'%' IDENTIFIED BY 'qlalfqjsgh486' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
flush privileges;