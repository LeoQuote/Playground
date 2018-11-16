import logging
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from rules.models import Rule, TeleUser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
ADMIN_LIST = []

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
        new_tele_user.status = 'start'
        response_text = "Welcome back!"
    except TeleUser.DoesNotExist:
        new_tele_user = TeleUser(
            tele_id = user.id,
            first_name = user.first_name,
            last_name = user.last_name,
            username = user.username,
            is_bot = user.is_bot,
            status = 'start',
            status_since = datetime.now()
        )
        response_text = "Thanks for coming, please chat with me."
    new_tele_user.json_data = str(user)
    new_tele_user.save()

    bot.send_message(chat_id=update.message.chat_id, text=response_text)

@log_message
def set_rules_entry(bot, update):
    user = TeleUser.objects.get(tele_id = update.message.from_user.id)
    user.status = 'rule_trigger'
    user.save()
    bot.send_message(chat_id=update.message.chat_id, text='已进入修改规则模式, 请输入触发语句')


class text_message_handler:
    def __init__(self, user, message):
        self.user = user
        self.message = message
    
    @property
    def response(self):
        return self.dispatch()
    def on_start(self):
        try:
            matched_rule = Rule.objects.get(trigger_text = self.message, is_complete =True)
            return matched_rule.response_text
        except Rule.DoesNotExist:
            return "没有对应规则, 试试 /set 设置一个吧"
    def dispatch(self):
        def func_not_found():
            return "系统内部错误: 未找到当前{}模式下的对应方法".format(self.user.status)
        func_name = "on_{}".format(self.user.status)
        func = getattr(self, func_name, func_not_found)
        return func()
    def on_rule_trigger(self):
        # 设置规则模式 步骤 2 输入 触发语句
        # status: rule_trigger
        # next_status: rule_response
        new_rule = Rule(
            trigger_text = self.message,
            added_by = self.user
        )
        new_rule.save()
        self.user.status = 'rule_response'
        self.user.save()
        return "请输入响应语句"
    def on_rule_response(self):
        # 设置规则模式 步骤3 输入 响应语句
        # status: rule_response
        # next_status: start
        new_rule = Rule.objects.filter(added_by = self.user, is_complete=False)[0]
        new_rule.response_text = self.message
        new_rule.is_complete = True
        new_rule.save()
        self.user.status = 'start'
        self.user.save()
        return "规则已保存"
@log_message
def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

@is_admin
@log_message
def enter_rules(bot, update):
    user = TeleUser.objects.get(tele_id = update.message.from_user.id)
    user.status = 'rule_trigger'
    user.status_since = datetime.now()
    user.save()
    bot.send_message(chat_id=update.message.chat_id, text='已进入修改规则模式, 请输入触发语句')

@log_message
def echo(bot, update):
    if update.message.from_user.username == 'Leocx':
        bot.send_message(chat_id=update.message.chat_id, text='好的主人')
    u = TeleUser.objects.get(tele_id = update.message.from_user.id)
    m = update.message.text
    h = text_message_handler(u, m)
    response_text = h.response 
    if response_text:
        bot.send_message(chat_id=update.message.chat_id, text=response_text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='你难到我了...')

class Command(BaseCommand):
    help = 'start telegram bot'
    
    def handle(self, *args, **options):
        updater = Updater('748269063:AAE_P3N8DD6oYABQRQk1yszDGX9nm4wVy1U',request_kwargs={'proxy_url':'http://127.0.0.1:1080'})
        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(Filters.text, echo)
        set_handler = CommandHandler('set', enter_rules)
        updater.dispatcher.add_handler(echo_handler)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(CommandHandler('hello', hello))
        updater.dispatcher.add_handler(set_handler)

        updater.start_polling()
        logging.info('Robot started')
        updater.idle()
