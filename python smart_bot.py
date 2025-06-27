import ccxt
import time
import requests
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# === НАСТРОЙКИ ===
api_key = 'Lrr2C75Qn4iJcfvrFN'
api_secret = 'OYvTwpjiyjcyS1LWL03DQE7f47b1JHnQUnCy'
symbol = 'BTC/USDT:USDT'
amount = 0.001
tp_dollars = 5
timeout_sec = 20 * 60
MAX_REENTRIES = 3

# === TELEGRAM ===
TELEGRAM_TOKEN = '7912609829:AAGu3jGG8Ku4RfIOXUL8aVgjqLBlqOki4_0'
CHAT_ID = '1203769403'

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except:
        print("❌ Ошибка Telegram")

# === ПОДКЛЮЧЕНИЕ К BYBIT ===
exchange = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

def get_price():
    return exchange.fetch_ticker(symbol)['last']

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    send_telegram(msg)

def open_position(side):
    if side == 'long':
        return exchange.create_market_buy_order(symbol, amount)
    else:
        return exchange.create_market_sell_order(symbol, amount)

def close_position(side):
    if side == 'long':
        return exchange.create_market_sell_order(symbol, amount)
    else:
        return exchange.create_market_buy_order(symbol, amount)

def run_strategy():
    log("🚀 Открываю стартовый ЛОНГ и ШОРТ")
    price_entry = get_price()

    # Первые сделки
    open_position('long')
    open_position('short')

    entry_time = time.time()
    long_closed = False
    short_closed = False
    reentries = 0
    trend_direction = None

    while not (long_closed and short_closed):
        price_now = get_price()
        elapsed = time.time() - entry_time

        long_tp = price_entry + (tp_dollars / amount)
        short_tp = price_entry - (tp_dollars / amount)

        # === Закрытие ЛОНГ ===
        if not long_closed and price_now >= long_tp:
            close_position('long')
            log(f"💰 ЛОНГ закрылся в +{tp_dollars}$")
            long_closed = True
            trend_direction = 'long'
            last_price = price_now

        # === Закрытие ШОРТ ===
        if not short_closed and price_now <= short_tp:
            close_position('short')
            log(f"💰 ШОРТ закрылся в +{tp_dollars}$")
            short_closed = True
            trend_direction = 'short'
            last_price = price_now

        # === Переоткрытие по тренду ===
        if trend_direction and reentries < MAX_REENTRIES:
            if trend_direction == 'long' and price_now >= last_price + (tp_dollars / amount):
                open_position('long')
                log(f"🔄 Новый ЛОНГ открыт по тренду ↑ (реентри #{reentries + 1})")
                last_price = price_now
                reentries += 1

            elif trend_direction == 'short' and price_now <= last_price - (tp_dollars / amount):
                open_position('short')
                log(f"🔄 Новый ШОРТ открыт по тренду ↓ (реентри #{reentries + 1})")
                last_price = price_now
                reentries += 1

        # === Закрытие по таймеру ===
        if elapsed > timeout_sec:
            log("⏳ Время вышло. Закрываю всё.")
            if not long_closed:
                close_position('long')
            if not short_closed:
                close_position('short')
            break

        time.sleep(3)

    log("✅ Цикл завершён\n")

# === ОБРАБОТЧИК КОМАНДЫ /start ===
def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Начать', 'Отмена']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        "Начать торговлю?",
        reply_markup=markup
    )

# === ОБРАБОТЧИК ОТВЕТОВ НА КНОПКИ ===
def handle_response(update: Update, context: CallbackContext) -> None:
    user_response = update.message.text
    if user_response == 'Начать':
        update.message.reply_text("Торговля началась!")
        run_strategy()
    elif user_response == 'Отмена':
        update.message.reply_text("Торговля отменена.")

# === НАСТРОЙКА БОТА ===
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_response))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()