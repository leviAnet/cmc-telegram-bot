import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Telegram bot token from environment variable
TOKEN = os.getenv("TOKEN")

# CoinMarketCap API endpoint
CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
CMC_API_KEY = os.getenv("CMC_API_KEY")

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Crypto Bot!")

def get_price(update: Update, context: CallbackContext):
    symbol = context.args[0].upper()
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
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The price of {symbol} is {price:.2f} USD")

def calculate_price(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command format. Use /calc <symbol> <amount>")
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
    total_price = amount * price
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The price of {amount} {symbol} is {total_price:.2f} USD")

def get_crypto(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command format. Use /get <symbol> <amount>")
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
    total_crypto = amount / price
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The amount of {amount} USD is {total_crypto:.8f} {symbol}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define command handlers
    start_handler = CommandHandler('start', start)
    get_price_handler = CommandHandler('p', get_price)
    calc_handler = CommandHandler('calc', calculate_price)
    get_handler = CommandHandler('get', get_crypto)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_price_handler)
    dispatcher.add_handler(calc_handler)
    dispatcher.add_handler(get_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
