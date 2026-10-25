-- Shoe Tracker Database Schema

CREATE TABLE IF NOT EXISTS shoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    color TEXT,
    current_km REAL DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    retired INTEGER DEFAULT 0,
    garmin_uuid TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS run_shoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shoe_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    distance_km REAL NOT NULL,
    source TEXT DEFAULT 'strava',
    strava_activity_id TEXT,
    garmin_activity_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shoe_id) REFERENCES shoes(id)
);

-- Index for quick lookups
CREATE INDEX IF NOT EXISTS idx_run_shoes_date ON run_shoes(date);
CREATE INDEX IF NOT EXISTS idx_run_shoes_shoe ON run_shoes(shoe_id);
CREATE INDEX IF NOT EXISTS idx_shoes_active ON shoes(retired);
