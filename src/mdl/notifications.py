import telegram
from settings.base import TELEGRAM_TOKEN

from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Updater, Filters


class Binancito:
    def __init__(self, token=TELEGRAM_TOKEN, main_chat_id=None):
        self.bot = Bot(token=token)
        self.main_chat_id = main_chat_id
        self.token = token
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

    def start(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start_callback))
        self.dispatcher.add_handler(MessageHandler(Filters.all, self.catch_all))
        if self.main_chat_id:
            self.bot.send_message(chat_id=self.main_chat_id, text="Bot started")
        self.updater.start_polling()

    def send_main_user_message(self, text):
        self.bot.send_message(chat_id=self.main_chat_id, text=text)

    def catch_all(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user_says = update.message.text
        update.message.reply_text(f"Catch all {user_says} trough {chat_id}")

    def start_callback(self, update: Update, context: CallbackContext):
        # save the chat id for future reference
        chat_id = update.effective_chat.id
        user_says = update.message.text
        update.message.reply_text(f"Welcome to my bot! {user_says} trough {chat_id}")
        # user_says = " ".join(context.args)
        # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


    # def get_me(self):
    #     """ something like
    #     {
    #         'can_read_all_group_messages': False,
    #         'username': 'PolaciaBot',
    #         'supports_inline_queries': False,
    #         'can_join_groups': True,
    #         'id': 5079759794,
    #         'first_name': 'binancito',
    #         'is_bot': True
    #     }
    #     """
    #     return self.bot.get_me()
        
    # def get_updates(self):
    #     """ 
    #     {'update_id': 218946040, 'message': {'message_id': 23833, 'date': 1626017436, 'text': 'Hi!', 'chat': {'type': 'private', 'last_name': 'Doe', 'username': 'JohnDoe', 'id': 1234567890, 'first_name': 'John'}, 'from': {'last_name': 'Doe', 'username': 'JohnDoe', 'id': 1234567890, 'is_bot': False, 'language_code': 'de', 'first_name': 'John'}, ...}}
    #     """
    #     updates = self.bot.get_updates()
    #     return updates[0]
    