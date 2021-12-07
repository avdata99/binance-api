from settings.base import BINANCE_API_KEY, BINANCE_SECRET_KEY
from mdl.base import MyBinance

mb = MyBinance(
    api_key=BINANCE_API_KEY,
    secrete_key=BINANCE_SECRET_KEY,
    money='USDT',
    assets=['ETH'],
    bucket_size=100.0
)

mb.run()
