# https://binance-connector.readthedocs.io/en/stable/

import json
from binance.spot import Spot
from settings.base import api_key, secrete_key

client = Spot(
    key=api_key,
    secret=secrete_key
)

print(client.time())
account = client.account()
balances = {}
for balance in account['balances']:
    free = float(balance['free'])
    locked = float(balance['locked'])
    if free + locked > 0:
        balances[balance['asset']] = {
            'free': free,
            'locked': locked
        }

# print(json.dumps(balances, indent=4))

"""
{
    "ETH": {
        "free": 6.85e-05,
        "locked": 99.99
    },
    "USDT": {
        "free": 0.102321,
        "locked": 0.0
    }
}
"""

response = client.get_orders("ETHUSDT")  # all, open, filled, canceled
print(response)

# response = client.get_open_orders("ETHUSDT")

# # Post a new order
# params = {
#     'symbol': 'ETHUSDT',
#     'side': 'SELL',
#     'type': 'LIMIT',
#     'timeInForce': 'GTC',
#     'quantity': 0.002,
#     'price': 9500
# }
# response = client.new_order(**params)
# print(response)