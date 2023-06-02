import os
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# CoinMarketCap API endpoint
CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
CMC_API_KEY = 'YOUR_COINMARKETCAP_API_KEY'

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bitcoin Bot!")

def help_command(update: Update, context: CallbackContext):
    response = "Use /p to get the price of any cryptocurrency in USD. For example, /p btc 0.1\n" \
               "Use /get to get the amount of cryptocurrency you can get for a certain amount in USD. For example, /get btc 100"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.HTML)

def get_bitcoin_price(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command format. Use /p btc <amount> or /get btc <amount>")
        return

    symbol = args[0].upper()
    amount = float(args[1])
    parameters = {
        'symbol': symbol,
        'convert': 'USD',
        'CMC_PRO_API_KEY': CMC_API_KEY
    }
    response = requests.get(CMC_API_URL, params=parameters)
    data = response.json()

    if symbol not in data['data']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid symbol. Please provide a valid symbol.")
        return

    price = data['data'][symbol]['quote']['USD']['price']
    if update.message.text.startswith('/p'):
        total_price = amount * price
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The price of {symbol} for {amount} is {total_price:.2f} USD")
    elif update.message.text.startswith('/get'):
        total_crypto = amount / price
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The amount of {symbol} you get for {amount} USD is {total_crypto:.8f}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define command handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    get_bitcoin_price_handler = CommandHandler(['p', 'get'], get_bitcoin_price)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(get_bitcoin_price_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
