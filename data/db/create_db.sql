CREATE TABLE news
(
  id				  INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  date                TIMESTAMP NOT NULL DEFAULT NOW(),
  title               TEXT NOT NULL,
  href                TEXT NULL,
  source              TEXT NULL,
  KEY(date),
  KEY(source(500)),
  UNIQUE KEY(title(500))
);

