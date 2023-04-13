from django.core.management.base import BaseCommand
from coinbase.models import TradingSettings, Trade
from django.conf import settings

import ccxt
import time



# PRODUCTION
exchange = ccxt.coinbasepro({
    'apiKey': settings.COINBASE_API_KEY,
    'secret': settings.COINBASE_API_SECRET,
    'password': settings.COINBASE_API_PASSPHRASE,
    'enableRateLimit': True,
})

#SANDBOX 
exchange = ccxt.coinbasepro({
    "apiKey": "bac3e369fcb59289a9282af99b9c8524",
    "secret": "x7ExpiRjvz3c1/ZcPX8dx4GWXySin2LMCRcWuwbvMOlEYOc7otsaL6/GCEs3WuO74JYDcoxywsoUjb9sM9AJIA==",
    "password": "4ihprsr6na",
    "enableRateLimit": True,
    'urls': {
        'api': {
            'public': 'https://api-public.sandbox.pro.coinbase.com',
            'private': 'https://api-public.sandbox.pro.coinbase.com',
        },
    },
})

class Command(BaseCommand):
    help = 'Run the scalping strategy for trading.'

    def handle(self, *args, **options):
        
        settings = TradingSettings.objects.first()

        if not settings or not settings.is_active:
            print("Trading is not active.")
            return

        symbols = settings.trading_symbols

        for symbol in symbols:
            try:
                balance = exchange.fetch_balance()
                base_currency_balance = balance[settings.base_currency]['free']
                quote_currency = symbol.split('/')[0]
                quote_currency_balance = balance[quote_currency]['free']

                if base_currency_balance >= settings.initial_investment * settings.investment_percentage:
                    buy_order = exchange.create_market_buy_order(symbol, base_currency_balance * settings.investment_percentage)
                    buy_price = buy_order['price']
                    trade = Trade(
                        symbol=symbol,
                        status=Trade.OPEN,
                        investment_amount=base_currency_balance * settings.investment_percentage,
                        purchase_price=buy_price,
                    )
                    trade.save()
                    print('Buy order:', buy_order)

                open_trades = Trade.objects.filter(symbol=symbol, status=Trade.OPEN)

                for open_trade in open_trades:
                    current_price = exchange.fetch_ticker(symbol)['ask']
                    profit_loss = (current_price - open_trade.purchase_price) / open_trade.purchase_price

                    if profit_loss >= settings.sell_threshold or profit_loss <= -settings.stop_loss_threshold:
                        sell_order = exchange.create_market_sell_order(symbol, quote_currency_balance)
                        open_trade.status = Trade.CLOSED
                        open_trade.sale_price = sell_order['price']
                        open_trade.profit_loss = profit_loss
                        open_trade.save()
                        print('Sell order:', sell_order)

            except Exception as e:
                print(f"Error trading {symbol}: {e}")