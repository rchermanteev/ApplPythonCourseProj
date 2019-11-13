from tokens import TELEGRAM_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import handlers
from logger import logger


class Bot:

    # handlers
    start_handler = CommandHandler('start', handlers.start, pass_user_data=True)
    photo_handler = MessageHandler(Filters.photo, handlers.photo, pass_user_data=True)
    unknown_handler = MessageHandler(Filters.command, handlers.unknown, pass_user_data=True)

    def __init__(self):
        print(TELEGRAM_TOKEN)
        self.updater = Updater(token=TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(self.start_handler)
        self.dispatcher.add_handler(self.photo_handler)
        self.dispatcher.add_handler(self.unknown_handler)

    def start(self):
        self.updater.start_polling()
        logger.info('Bot running')


if __name__ == "__main__":
    b = Bot()
    b.start()
