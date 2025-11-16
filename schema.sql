CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    joined_at INTEGER,
    downloads_today INTEGER DEFAULT 0,
    last_reset INTEGER DEFAULT 0,
    vip INTEGER DEFAULT 0,
    backoff_level INTEGER DEFAULT 0,
    banned_until INTEGER DEFAULT 0,
    referred_by INTEGER DEFAULT NULL,
    total_referrals INTEGER DEFAULT 0,
    language TEXT DEFAULT 'id'
);

CREATE TABLE IF NOT EXISTS files (
    file_unique TEXT PRIMARY KEY,
    file_id TEXT,
    caption TEXT,
    uploader INTEGER,
    created_at INTEGER,
    downloads INTEGER DEFAULT 0,
    category TEXT
);

CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item TEXT,
    amount INTEGER,
    currency TEXT,
    status TEXT,
    created_at INTEGER
);

CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);

CREATE TABLE IF NOT EXISTS bucket_state (
    user_id INTEGER PRIMARY KEY,
    tokens REAL,
    last_ts REAL
);

CREATE TABLE IF NOT EXISTS autorespond (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger TEXT,
    response TEXT
);
