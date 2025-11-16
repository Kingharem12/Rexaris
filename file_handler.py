from telegram import Update
from telegram.ext import ContextTypes
from ..db import get_conn
from ..config import DATA_DIR
import os, json, time

conn = get_conn()
cur = conn.cursor()

async def upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = update.effective_user
    file_obj = msg.document or msg.video or msg.audio or (msg.photo and msg.photo[-1])
    if not file_obj:
        return
    f_id = file_obj.file_id
    f_unique = getattr(file_obj, 'file_unique_id', f_id)
    caption = msg.caption or ''
    cur.execute('INSERT OR REPLACE INTO files(file_unique,file_id,caption,uploader,created_at) VALUES(?,?,?,?,?)',
                (f_unique, f_id, caption, user.id, int(time.time())))
    conn.commit()
    meta = {'file_unique': f_unique, 'file_id': f_id, 'caption': caption, 'uploader': user.id, 'created_at': int(time.time())}
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, f"{f_unique}.json"), 'w') as fh:
        json.dump(meta, fh, ensure_ascii=False)
    link = f"https://t.me/{(await context.bot.get_me()).username}?start={f_unique}"
    await msg.reply_text('✅ File disimpan!\n' + link)
