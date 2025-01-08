from fastapi import FastAPI, Request
from telegram import Update, Bot
from pydantic import BaseModel
from typing import Optional

from telegram.ext import Dispatcher, CommandHandler, CallbackContext, Updater
import schedule
import time
import threading
import uvicorn
import json

from auto_poll import start, add_poll, TELEGRAM_BOT_TOKEN

app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]


@app.post('/webhook')
async def webhook(request: TelegramWebhook):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    update = Update.de_json(request.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    print(request.__dict__)
    
    dispatcher = Dispatcher(bot, None, workers=4)
    dispatcher = Dispatcher(bot, None, workers=0)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_poll))

    # handle webhook request
    dispatcher.process_update(update)
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=run_schedule).start()
    uvicorn.run(app, host="0.0.0.0", port=5001)