from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils import t
from ..db import get_conn
import time

conn = get_conn()
cur = conn.cursor()

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # show language selection if not set
    cur.execute('SELECT language FROM users WHERE user_id=?', (user.id,))
    r = cur.fetchone()
    if not r or not r[0]:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton('Bahasa Indonesia 🇮🇩', callback_data='lang_id')],
            [InlineKeyboardButton('English 🇺🇸', callback_data='lang_en')]
        ])
        await update.message.reply_text('Selamat datang! Pilih bahasa Anda / Welcome! Choose your language:', reply_markup=kb)
        return
    await update.message.reply_text(t(user.id, 'menu_main'))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(t(user.id, 'help'))
