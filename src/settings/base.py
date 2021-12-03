# create a secret.py file with real values

BINANCE_API_KEY=""
BINANCE_SECRET_KEY=""
TELEGRAM_BOT_NAME=""
TELEGRAM_BOT_USERNAME=""
TELEGRAM_TOKEN=""
# CHAT ID to notify
TELEGRAM_CHAT_ID=""

try:
    from settings.secret import *
except (ModuleNotFoundError, ImportError):
    pass
