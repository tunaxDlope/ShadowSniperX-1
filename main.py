import ccxt
import pandas as pd
from ta.trend import EMAIndicator
from telegram import Bot

import os

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

def send_alert(message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

def scan_market():
    exchange = ccxt.binance()
    symbols = ['BTC/USDT', 'ETH/USDT']

    for symbol in symbols:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=100)
        df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        ema9 = EMAIndicator(close=df['close'], window=9).ema_indicator()
        ema20 = EMAIndicator(close=df['close'], window=20).ema_indicator()

        if ema9.iloc[-1] > ema20.iloc[-1] and ema9.iloc[-2] <= ema20.iloc[-2]:
            send_alert(f"🚀 BUY Signal: {symbol} (EMA 9/20 crossover)")
        elif ema9.iloc[-1] < ema20.iloc[-1] and ema9.iloc[-2] >= ema20.iloc[-2]:
            send_alert(f"🔻 SELL Signal: {symbol} (EMA 9/20 crossover)")

if __name__ == '__main__':
    scan_market()
