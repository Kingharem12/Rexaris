import time, os, json
from .config import DATA_DIR, TOKEN_BUCKET_CAP, TOKEN_BUCKET_REFILL
from .db import get_conn

_conn = get_conn()
_cur = _conn.cursor()

LANG = {
    'id': {
        'start': 'Selamat datang di Superbot! Pilih bahasa Anda:',
        'menu_main': 'Menu Utama',
        'help': 'Ketik /help untuk bantuan',
        'vip_active': 'Status VIP Anda: Aktif',
        'vip_inactive': 'Status VIP Anda: Tidak aktif',
        'need_join': 'Anda harus bergabung dengan semua channel yang diwajibkan:'
    },
    'en': {
        'start': 'Welcome to Superbot! Choose your language:',
        'menu_main': 'Main Menu',
        'help': 'Type /help for assistance',
        'vip_active': 'Your VIP Status: Active',
        'vip_inactive': 'Your VIP Status: Inactive',
        'need_join': 'You must join all required channels:'
    }
}

def t(user_id: int, key: str):
    try:
        _cur.execute('SELECT language FROM users WHERE user_id=?', (user_id,))
        r = _cur.fetchone()
        lang = r[0] if r and r[0] else 'id'
    except Exception:
        lang = 'id'
    return LANG.get(lang, LANG['id']).get(key, key)

def bucket_get_state(uid: int):
    _cur.execute('SELECT tokens, last_ts FROM bucket_state WHERE user_id=?', (uid,))
    r = _cur.fetchone()
    if r:
        return float(r[0]), float(r[1])
    return TOKEN_BUCKET_CAP, time.time()

def bucket_put_state(uid: int, tokens: float, last_ts: float):
    _cur.execute('INSERT INTO bucket_state(user_id,tokens,last_ts) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET tokens=excluded.tokens,last_ts=excluded.last_ts',
                 (uid, tokens, last_ts))
    _conn.commit()

def bucket_consume(uid: int, cost: float = 1.0):
    tokens, last_ts = bucket_get_state(uid)
    now = time.time()
    refill = (now - last_ts) * TOKEN_BUCKET_REFILL
    tokens = min(TOKEN_BUCKET_CAP, tokens + refill)
    if tokens >= cost:
        tokens -= cost
        bucket_put_state(uid, tokens, now)
        return True
    bucket_put_state(uid, tokens, now)
    return False
