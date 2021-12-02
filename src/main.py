from settings.base import api_key, secrete_key
from mdl.base import MyBinance

mb = MyBinance(
    api_key=api_key,
    secrete_key=secrete_key,
    money='USDT',
    assets=['ETH'],
    pause=60 * 60,
    bucket_size=100.0
)

mb.run()
