from mail_fetcher import MailBox
from tele_bot import TeleBot
import time

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, Filters, ConversationHandler, MessageHandler
from telegram import Update


# Function that will be called when a user sends the /start command
async def start(update: Update, context: CallbackContext) -> None:
    # Get the user's chat ID
    chat_id = update.message.chat_id
    # Get the user's username (if available)
    username = update.message.from_user.username
    # Send a welcome message
    update.message.reply_text(f"Hello {username}! Your chat ID is {chat_id}.")
    # Print the chat ID to the console (or save it as needed)
    print(f"User {username} started the bot. Chat ID: {chat_id}")

    await update.message.reply_text(f"Hi! {username}")

    async def start_check_mail():
        # mail authentication
        username = "tranvansangdv11@gmail.com"
        password = "jryg yzev fifd sxfq"
        mail_box = MailBox(username=username, password=password)

        while True:
            
            # Wait for 60 seconds before checking again
            sender, subject = mail_box.get_newest_mail()
            await update.message.reply_text(f"You recieved a mail from {sender} about {subject}")

            time.sleep(60)

    await start_check_mail()

    # todo get user

# Username handler
def get_username(update: Update, context: CallbackContext) -> int:
    context.user_data['username'] = update.message.text
    update.message.reply_text("Got it! Now, please enter your password:")
    return PASSWORD

# Password handler
def get_password(update: Update, context: CallbackContext) -> int:
    context.user_data['password'] = update.message.text
    username = context.user_data['username']
    password = context.user_data['password']

    # Here, you should handle the username and password securely (e.g., hashing the password, etc.)
    update.message.reply_text(f"Username: {username}\nPassword: {password}\n(Handle this data securely!)")

    # Clear the sensitive data after processing
    context.user_data.clear()

    return ConversationHandler.END

# Cancel command handler
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation canceled.")
    return ConversationHandler.END




# async def send_noti_new_mail(update: Update, context: CallbackContext):
#     await


if __name__ == "__main__":

    # mail authentication
    username = "tranvansangdv11@gmail.com"
    password = "jryg yzev fifd sxfq"

    # tele token
    tele_token = "7151406086:AAHTs9TzjqPg3od8XvdiNP0LYepeVvFkpaQ"

    USERNAME, PASSWORD = range(2)



    tele_bot = TeleBot(telegram_token=tele_token)

    app = ApplicationBuilder().token(tele_token).build()

    app.add_handler(CommandHandler("start", start))


    # Conversation handler to manage states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, get_username)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # app.add_handler(CommandHandler("start", start))
    

    app.run_polling()

