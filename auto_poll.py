import os
from telegram.ext import Updater, CommandHandler
from telegram import Poll
import schedule
import time
from datetime import datetime

TELEGRAM_BOT_TOKEN = '6309138916:AAG0QCtOdLNqNewuMaLLQE6IeG0mqFSMSXc'
TARGET_CHAT_ID = 'YOUR_TARGET_CHAT_ID'

poll_data = {
    'time': None,
    'question': None,
    'options': []
}

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Hello! I'm a bot that creates weekly polls. Use /add to set up a poll.")

def add_poll(update, context):
    message = update.message.text.split("\n", 1)[1]  # Remove the /add command
    lines = message.split('\n')
    
    if len(lines) < 3:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Please provide time, question, and at least two options. Each on a new line.")
        return

    poll_data['time'] = lines[0].strip()
    poll_data['question'] = lines[1].strip()
    poll_data['options'] = [option.strip() for option in lines[2:] if option.strip()]

    if len(poll_data['options']) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Please provide at least two options for the poll.")
        return

    setup_weekly_poll(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=f"Poll scheduled for {poll_data['time']} with question: {poll_data['question']}")

def create_poll(update, context):
    context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=poll_data['question'],
        options=poll_data['options'],
        is_anonymous=False,
        allows_multiple_answers=False
    )
    print(f"Poll created at {datetime.now()}")

def setup_weekly_poll(update, context):
    schedule.clear()  # Clear any existing schedules
    day, time = poll_data['time'].lower().split()
    
    if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Invalid day. Please use full day names like 'Monday'.")
        return

    schedule_func = getattr(schedule.every(), day)
    schedule_func.at(time).do(create_poll, update, context)
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=f"Weekly poll has been scheduled for every {day.capitalize()} at {time}.")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_poll))

    updater.start_polling()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()