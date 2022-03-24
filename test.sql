CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY,
 second_name varchar(20) NOT NULL,
 first_name varchar(20) NOT NULL,
 patronymic varchar(20) NOT NULL,
 region_id INTEGER NOT NULL,
 city_id INTEGER NOT NULL,
 phone VARCHAR(20) NOT NULL UNIQUE,
 email VARCHAR(320) NOT NULL UNIQUE,
 FOREIGN KEY(region_id) REFERENCES cities(region_id),
 FOREIGN KEY(city_id) REFERENCES cities(id)
);

CREATE TABLE IF NOT EXISTS regions (
 id INTEGER PRIMARY KEY,
 region_name varchar(50) NOT NULL UNIQUE
);

INSERT OR IGNORE INTO regions (id, region_name)
VALUES 
 (0, 'Краснодарский край'),
 (1, 'Ростовская область'),
 (2, 'Ставропольский край');

CREATE TABLE IF NOT EXISTS cities (
 id INTEGER PRIMARY KEY,
 region_id INTEGER NOT NULL,
 city_name varchar(30) NOT NULL UNIQUE,
 FOREIGN KEY(region_id) REFERENCES regions(id)
);

INSERT OR IGNORE INTO cities (id, region_id, city_name)
VALUES 
 (0, 0, 'Краснодар'),
 (1, 0, 'Кропоткин'),
 (2, 0, 'Славянск'),
 (3, 1, 'Ростов'),
 (4, 1, 'Шахты'),
 (5, 1, 'Батайск'),
 (6, 2, 'Ставрополь'),
 (7, 2, 'Пятигорск'),
 (8, 2, 'Кисловодск');