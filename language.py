from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ..db import get_conn
from ..utils import t
import time

conn = get_conn()
cur = conn.cursor()

async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton('Bahasa Indonesia 🇮🇩', callback_data='lang_id')],
        [InlineKeyboardButton('English 🇺🇸', callback_data='lang_en')]
    ])
    await update.message.reply_text(t(user.id, 'start'), reply_markup=kb)

async def language_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    code = q.data.split('_')[1]
    # create users table row if missing
    cur.execute('SELECT 1 FROM users WHERE user_id=?', (uid,))
    if not cur.fetchone():
        cur.execute('INSERT INTO users(user_id, joined_at, last_reset, language) VALUES(?,?,?,?)', (uid, int(time.time()), int(time.time()), code))
    else:
        try:
            cur.execute('UPDATE users SET language=? WHERE user_id=?', (code, uid))
        except Exception:
            pass
    conn.commit()
    await q.edit_message_text('Bahasa disimpan.' if code=='id' else 'Language saved.')
