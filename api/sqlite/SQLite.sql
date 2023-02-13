-- SQLite
CREATE TABLE IF NOT EXISTS USERS (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL,
	EMAIL TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PEPPER (
    USERNAME TEXT PRIMARY KEY,
    PEPPER TEXT NOT NULL
);