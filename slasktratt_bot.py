# coding=UTF-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config, logging

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)

log = logging.getLogger(__name__)

CLEANING_SCHEDULE = {'kitchen':'Snadrian','big_bath':'Dempan', 'small_bath':'J-Dawg', 'livingroom':'Luuli'}


# Reply to /start with greeting message
def start(bot, update, args, job_queue, chat_data):
    update.message.reply_text('---SLASKTRATTITRON INITIALIZED---')
    print_cleaning_schedule(bot, update, chat_data)


# Reply to /help with instructions of use
def help(bot, update):
    update.message.reply('This bot is intended to keep track of the städschema for Slasktrattarnas Kollektiv. The following commands can be used: --TODO--')

# Echo the last message
def echo(bot, update):
    update.message.reply_text(update.message.text)

# Log errors caused by Updates
def error(bot, update, error):
    log.warning('Update "%s" caused error "%s"', update, error)

# Print städschema
def print_cleaning_schedule(bot, update, chat_data):
    """ PRINTING CLEANING SCHEDULE"""
    schedule=''

    for x in range(1,4):
        schedule+=str(ROOMS[x] + '\t' + PEOPLE[x]+ '\n')

    bot.send_message(chat_id=update.message.chat_id, text=
            'Veckans städschema:\n'+schedule)

def rotate(l, n):
    return l[n:] + l[:n]

def rotate_schedule(schedule):
    people = CURRENT_SCHEDULE.values()
    people_rot = rotate(people, 1)
    print('Rotating people for cleaning schedule, currently '+people)
    print('After rotation: '+people_rot)
    CURRENT_SCHEDULE['kitchen':people_rot[0]]
    CURRENT_SCHEDULE['big_bath':people_rot[1]]
    CURRENT_SCHEDULE['small_bath':people_rot[2]]
    CURRENT_SCHEDULE['livingroom':people_rot[3]]





# MAIN LOOP
def main():
    """INIT SLASKTRATT_BOT"""

    # Eventhandler takes api token from botfather msg
    updater = Updater(config.api_token)
    jobq = updater.job_queue

    # Dispatcher takes care of handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler('start', start,
        pass_args=True,
        pass_job_queue=True,
        pass_chat_data=True))
    dp.add_handler(CommandHandler('print', print_cleaning_schedule))
    dp.add_handler(CommandHandler('help', help))

    # Register error handler
    dp.add_error_handler(error)



