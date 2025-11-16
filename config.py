import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKENS = [t.strip() for t in os.getenv('BOT_TOKENS','').split(',') if t.strip()] or ([os.getenv('TG_BOT_TOKEN')] if os.getenv('TG_BOT_TOKEN') else [])
CHANNELS_WAJIB = [c.strip() for c in os.getenv('CHANNELS_WAJIB','').split(',') if c.strip()]
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS','').split(',') if x.strip()]
DAILY_LIMIT = int(os.getenv('DAILY_DOWNLOAD_LIMIT','5'))
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN','')
PAYMENT_CURRENCY = os.getenv('PAYMENT_CURRENCY','USD')
VIP_PRICE = int(os.getenv('VIP_PRICE','500'))
DATABASE_FILE = os.getenv('DATABASE_FILE','telegram_superbot.db')
DATA_DIR = os.getenv('DATA_DIR','bot_data')
TOKEN_BUCKET_CAP = float(os.getenv('TOKEN_BUCKET_CAP','10'))
TOKEN_BUCKET_REFILL = float(os.getenv('TOKEN_BUCKET_REFILL','1.0'))
