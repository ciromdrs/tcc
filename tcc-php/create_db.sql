CREATE DATABASE tcc_db;

CREATE TABLE tcc_db.post(
  id INT NOT NULL AUTO_INCREMENT,
  author VARCHAR(255),
  content VARCHAR(255),
  img BLOB,
  
  PRIMARY KEY(id)
);
