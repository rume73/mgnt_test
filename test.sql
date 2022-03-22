CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY,
 second_name TEXT NOT NULL,
 first_name TEXT NOT NULL,
 patronymic TEXT NOT NULL,
 region_id INTEGER,
 city_id INTEGER,
 phone INTEGER,
 email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regions (
 id INTEGER PRIMARY KEY,
 region_name TEXT NOT NULL
);

INSERT OR IGNORE INTO regions (id, region_name)
VALUES (0, 'Краснодарский край');

INSERT OR IGNORE INTO regions (id, region_name)
VALUES (1, 'Ростовская область');

INSERT OR IGNORE INTO regions (id, region_name)
VALUES (2, 'Ставропольский край');

CREATE TABLE IF NOT EXISTS cities (
 id INTEGER PRIMARY KEY,
 region_id INTEGER,
 city_name TEXT NOT NULL
);

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (0, 0, 'Краснодар');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (1, 0, 'Кропоткин');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (2, 0, 'Славянск');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (3, 1, 'Ростов');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (4, 1, 'Шахты');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (5, 1, 'Батайск');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (6, 2, 'Ставрополь');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (7, 2, 'Пятигорск');

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES (8, 2, 'Кисловодск');