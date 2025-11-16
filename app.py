import asyncio, time
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .config import BOT_TOKENS, ADMIN_IDS, CHANNELS_WAJIB, DAILY_LIMIT, PAYMENT_PROVIDER_TOKEN, PAYMENT_CURRENCY, VIP_PRICE, DATA_DIR
from .handlers.start import start_cmd, help_cmd
from .handlers.language import language_cmd, language_cb
from .handlers.admin import panel_cmd, admin_cb
from .handlers.file_handler import upload_handler
from .db import init_db, get_conn
from .utils import bucket_consume
import os

init_db()

async def start_single(token: str):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start_cmd))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('language', language_cmd))
    app.add_handler(CallbackQueryHandler(language_cb, pattern='^lang_'))
    app.add_handler(CommandHandler('panel', panel_cmd))
    app.add_handler(CallbackQueryHandler(admin_cb, pattern='^admin_'))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, upload_handler))
    print(f"[INFO] Starting bot for token prefix: {token[:10]}")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # keep running
    while True:
        await asyncio.sleep(3600)

async def start_all():
    tokens = [t for t in BOT_TOKENS if t]
    if not tokens:
        raise RuntimeError('No BOT_TOKENS configured')
    tasks = [asyncio.create_task(start_single(t)) for t in tokens]
    await asyncio.gather(*tasks)
