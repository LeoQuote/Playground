from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from rules.models import Rule, TeleUser
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
ADMIN_LIST = ['Leocx']
TELE_TOKEN = ''
def log_message(func):
    def wrapper(*args, **kwargs):
        logging.info('received message from {}, \"{}\"'.format(args[1].message.from_user.username, args[1].message.text))
        return func(*args, **kwargs)
    return wrapper

def is_admin(func):
    def wrapper(*args, **kwargs):
        if args[1].message.from_user.username in ADMIN_LIST:
            return func(*args, **kwargs)
        args[0].send_message(chat_id=args[1].message.chat_id, text="This method is for admin only")
    return wrapper



@log_message
def start(bot, update):
    user = update.message.from_user 
    try:
        new_tele_user = TeleUser.objects.get(tele_id = user.id)
        response_text = "Welcome back!"
    except TeleUser.DoesNotExist:
        new_tele_user = TeleUser(**user)
        response_text = "Thanks for coming, please chat with me."
    new_tele_user.json_data = user
    new_tele_user.save()

    bot.send_message(chat_id=update.message.chat_id, text=response_text)




@log_message
def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

@log_message
def echo(bot, update):
    if update.message.from_user.username == 'Leocx':
        bot.send_message(chat_id=update.message.chat_id, text='好的主人')
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

updater = Updater(TELE_TOKEN,request_kwargs={'proxy_url':'http://127.0.0.1:1080'})
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
updater.dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
logging.info('Robot started')
updater.idle()