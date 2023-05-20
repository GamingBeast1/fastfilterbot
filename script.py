import os
from dotenv import load_dotenv

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from telegraph import Telegraph
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token from environment variable
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Telegraph Token from environment variable
TELEGRAPH_TOKEN = os.getenv('TELEGRAPH_TOKEN')

# Initialize Telegraph
telegraph = Telegraph(TELEGRAPH_TOKEN)

# Initialize Updater
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)


# Command handler for /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome, {user.first_name}!")


# Command handler for /help command
def help(update: Update, context: CallbackContext) -> None:
    help_message = "This is a file filter bot. It can perform various operations on files.\n\n" \
                   "Available commands:\n" \
                   "/start - Start the bot\n" \
                   "/help - Show help message\n" \
                   "/shorten - Shorten a URL\n" \
                   "/filter - Filter files\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


# Command handler for /shorten command
def shorten(update: Update, context: CallbackContext) -> None:
    url = context.args[0] if len(context.args) > 0 else None
    if url:
        # Shorten the URL using Telegraph
        shortened_url = telegraph.create_page(url=url)['url']
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Shortened URL: {shortened_url}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a URL to shorten.")


# Command handler for /filter command
def filter_files(update: Update, context: CallbackContext) -> None:
    file_name = context.args[0] if len(context.args) > 0 else None
    if file_name:
        # Filter files based on the provided file name
        # Implement your logic here
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Filtering files with name: {file_name}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a file name to filter.")


# Message handler for handling all other messages
def handle_message(update: Update, context: CallbackContext) -> None:
    # Handle other message types
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown command or message.")


# Set up command handlers
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("shorten", shorten))
updater.dispatcher.add_handler(CommandHandler("filter", filter_files))
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))


# Start the bot
updater.start_polling()
updater.idle()
