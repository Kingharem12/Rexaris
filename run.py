from telegram_superbot.app import start_all
import asyncio

if __name__ == '__main__':
    # entrypoint: start all bot instances
    asyncio.run(start_all())
