from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ..db import get_conn
from ..config import ADMIN_IDS
import time

conn = get_conn()
cur = conn.cursor()

async def panel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        await update.message.reply_text('❌ Anda bukan admin.')
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton('📊 Statistik', callback_data='admin_stats')],
        [InlineKeyboardButton('💳 Monetisasi', callback_data='admin_pay')],
        [InlineKeyboardButton('🧰 Tools', callback_data='admin_tools')]
    ])
    await update.message.reply_text('Admin Panel', reply_markup=kb)

async def admin_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == 'admin_stats':
        cur.execute('SELECT COUNT(*) FROM users')
        users = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM files')
        files = cur.fetchone()[0]
        await q.edit_message_text(f'Users: {users} | Files: {files}')
    else:
        await q.edit_message_text('Action not implemented yet.')
