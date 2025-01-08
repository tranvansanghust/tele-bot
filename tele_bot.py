import telegram

class TeleBot:
    def __init__(self, telegram_token) -> None:
        self.bot = self.init_bot(telegram_token)
        pass

    def init_bot(self, telegram_token):
        bot = telegram.Bot(token=telegram_token)

        return bot
    
    def send_message(self, chat_id, from_, subject):
        # Send notification via Telegram
        self.bot.send_message(
            chat_id=chat_id,
            text=f"New email from {from_}\nSubject: {subject}"
        )