from random import choice
from time import sleep
from datetime import datetime
from binance.spot import Spot
from settings.base import BINANCE_API_KEY, BINANCE_SECRET_KEY, TELEGRAM_CHAT_ID
from mdl.notifications import Binancito


class MyBinance:
    """ My custom binance bot 
        Read: # https://binance-connector.readthedocs.io/en/stable/
    """
    def __init__(
        self,
        api_key,
        secrete_key,
        money='USDT',
        assets=['ETH'],
        bucket_size=100.0,
        telegram_chat_id=TELEGRAM_CHAT_ID,
    ):
        if api_key == '' or secrete_key == '':
            raise ValueError('API key and secrete key are required')
        self.client = Spot(key=BINANCE_API_KEY, secret=BINANCE_SECRET_KEY)
        self.account = None
        # Asset code for some stable coin to buy
        self.money=money
        # Define a list of assets to buy periodically
        self.assets=assets
        # size of each purchase (in "money")
        self.bucket_size=bucket_size

        # To load
        self.balances = None
        self.open_orders = None
        if telegram_chat_id:
            self.binancito = Binancito(main_chat_id=telegram_chat_id)
            # only to answer
            # self.binancito.start()
        else:
            self.binancito = None

    def load_balances(self):
        """ Get all balances
            # sample at data-samples/client-account.py
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
        # read account again
        self.account = self.client.account()
        self.balances = {}
        for balance in self.account['balances']:
            free = float(balance['free'])
            locked = float(balance['locked'])
            if free + locked > 0:
                self.balances[balance['asset']] = {
                    'free': free,
                    'locked': locked
                }
        
        money = self.balances.get(self.money, {})
        free_money = money.get('free', 0.0)
        locked_money = money.get('locked', 0.0)
        self.notify(f'Free Money {self.money}: {free_money} ({locked_money} locked)')
        assets = {k: v for k, v in self.balances.items() if k != self.money}
        for asset, balance in assets.items():
            free = balance.get('free', 0.0)
            locked = balance.get('locked', 0.0)
            self.notify(f' - ASSET {asset}: {free} ({locked} locked)')
        return self.balances

    def have_money_to_invest(self):
        """ Check if we have money to invest """
        money = self.balances.get(self.money, {})
        free_money = money.get('free', 0.0)
        return free_money > self.bucket_size

    def load_open_orders(self, asset='ETH'):
        """ Get all OPEN orders
            # sample at data-samples/get-orders.py
        """
        # response = client.get_orders("ETHUSDT")  # all, open, filled, canceled
        order_code = f'{asset}{self.money}'
        self.open_orders = self.client.get_open_orders(order_code)

    def _order(self, asset, side, order_type, quantity, price=None):
        """ Post a new order """
        if side not in ['BUY', 'SELL']:
            raise ValueError(f'Invalid "side": {side} should be "BUY" or "SELL"')
        if order_type not in ['LIMIT', 'MARKET']:
            raise ValueError(f'Invalid "type": {type} should be "LIMIT" or "MARKET"')

        params = {
            'symbol': f'{asset}{self.money}',
            'side': side,
            'type': order_type
        }
        if order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = 'GTC'
            params['quantity'] = quantity
        elif order_type == 'MARKET':
            # we buy in money
            params['quoteOrderQty'] = quantity

        self.notify(f'Ordering to {side} ({order_type}) {quantity} {asset} at {price}')
        response = self.client.new_order(**params)
        self.notify(f' - Binance responce: {response}')
        return response

    def buy(self, asset):
        """ Buy asset """
        return self._order(asset, 'BUY', 'MARKET', self.bucket_size)

    def sell(self, asset, quantity, price):
        """ Sell asset
            See your orders https://www.binance.com/es/my/orders/exchange/openorder """
        return self._order(asset, 'SELL', 'LIMIT', quantity, price)

    def notify(self, message):
        if self.binancito:
            self.binancito.send_main_user_message(message)
        print(message)

    def run(self):
        """ Run the bot """
        self.load_balances()
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%D %H:%M:%S")
            
        if not self.have_money_to_invest():
            self.notify(f'NOT ENOUGH MONEY TO INVEST {current_time}')
            return

        self.notify(f'OK TO INVEST {current_time}')
        # Buy any asset at a market price
        asset = choice(self.assets)
        response = self.buy(asset)
        # an order is filled with multiple fills. We use the first one
        price = float(response['fills'][0]['price'])
        self.notify(f'  - Order price {price}')
        quantity = float(response['executedQty'])
        # create several sell orders
        # avoid "Filter failure: PRICE_FILTER" error (use right number of decimal digits)
        # avoid "Filter failure: MIN_NOTIONAL"	price * quantity is too low to be a valid order for the symbol.
        # Errors https://github.com/ExplorerUpdateskaykutee/binance-official-api-docs-1/blob/master/errors.md
        # ORDER 1: 50% of the asset to gain 2%
        q1 = round(quantity * 0.5, 4)
        p1 = round(price * 1.015, 2)
        r1 = self.sell(asset, q1, p1)
        # ORDER 2: 30% of the asset to gain 3%
        q2 = round(quantity * 0.3, 4)
        p2 = round(price * 1.02, 2)
        r2 = self.sell(asset, q2, p2)
        # ORDER 3: 20% of the asset to gain 4%
        q3 = round(quantity * 0.2, 4)
        p3 = round(price * 1.025, 2)
        r3 = self.sell(asset, q3, p3)
        self.notify(f'  - Sell orders {p1} {r1["status"]}, {p2} {r2["status"]}, {p3} {r3["status"]}')    
