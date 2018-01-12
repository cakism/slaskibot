# coding=UTF-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import App
import logging, telegram

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)

log = logging.getLogger(__name__)


#### MAKE STATIC OR IN A FILE OR SOMETHING
CLEANING_SCHEDULE = {'1_kitchen':'Snadrian','2_big_bath':'Dempan', '3_small_bath':'kakan', '4_livingroom':'Luuli'}
ROOMS = {'1_kitchen':'Köket', '2_big_bath':'Stora badrummet', '3_small_bath':'Lilla badrummet', '4_livingroom':'Vardagsrum+hall'}
USERS = {'snadrian_id':'Snadrian', 'dempan_id':'Dempan', 'luuli_id':'Luuli', 'cakism_id':'kakan'}

# Reply to /start with greeting message
def start(bot, update, args, job_queue, chat_data):
    update.message.reply_text('---SLASKTRATTITRON INITIALIZED---\nUse command /help for available commands')
    chat_id = update.message.chat_id
    job = job_queue.run_once(print_cleaning_schedule, 3, context=chat_id)
    chat_data['job'] = job


# Reply to /help with instructions of use
def help(bot, update):
    update.message.reply_text("""This bot is intended to keep track of the städschema for Slasktrattarnas Kollektiv. The following commands can be used:\n
            \n/print - prints current schedule
            \n/print_my_tasks - sends PM with the tasks you have in your room
            \n/rotate - rotates the schedule one step down - this is done automatically every sunday so probably never use this :)
            \n/help - shows this message :)
            \nhave fun cleaning suckers, i\'m a robot so i dont have to do shit \o/""")

def print_tasks(bot,update):
    user = update.message.from_user
    print("Attempting to print tasks for user: " + str(user))
    username = ''
    for userid, name in USERS.items():
        print(str(App.config(userid)))
        if App.config(userid) == user.id:
            print("Username found: " + name)
            username = name
    for room, room_user in CLEANING_SCHEDULE.items():
        if room_user == username:
            print('Printing tasks for room: ' + room + " and user " + str(user))
            tasks = ''
            for task in App.config(room): tasks += task+'\n'
            bot.send_message(user.id, text=str(tasks))

# Log errors caused by Updates
def error(bot, update, error):
    log.warning('Update "%s" caused error "%s"', update, error)

#Print now command
def print_schedule_command(bot, update, job_queue):
    chat_id = update.message.chat_id
    print(str(update.message.from_user))
    job = job_queue.run_once(print_cleaning_schedule, 1, context=chat_id)

# Print städschema
def print_cleaning_schedule(bot, job):
    print('PRINTING CLEANING SCHEDULE')
    schedule=''

    for key in sorted(ROOMS):
        room = ROOMS[key]
        person = CLEANING_SCHEDULE[key]
        schedule+='*{:20s}* _{:>10s}_'.format(room, person)
        schedule+='\n'
    bot.send_message(job.context, text=
            'Veckans städschema:\n'+schedule, parse_mode=telegram.ParseMode.MARKDOWN)

def rotate(l, n):
    return l[-n:] + l[:-n]

def rotate_schedule(bot, update):
    people=[]
    for key in sorted(CLEANING_SCHEDULE):
        people.append(str(CLEANING_SCHEDULE[key]))
    people_rot = rotate(people, 1)
    print('Rotating people for cleaning schedule, currently '+str(CLEANING_SCHEDULE))
    for idx, key in enumerate(sorted(CLEANING_SCHEDULE)):
        CLEANING_SCHEDULE[key]=people_rot[idx]

    print('After rotation: '+str(CLEANING_SCHEDULE))




# MAIN LOOP
def main():
    """INIT SLASKTRATT_BOT"""

    # Eventhandler takes api token from botfather msg
    updater = Updater(App.config('api_token'))
    jobq = updater.job_queue

    # Dispatcher takes care of handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler('start', start,
        pass_args=True,
        pass_job_queue=True,
        pass_chat_data=True))
    dp.add_handler(CommandHandler('print', print_schedule_command, pass_job_queue=True))
    dp.add_handler(CommandHandler('print_my_tasks', print_tasks))
    dp.add_handler(CommandHandler('rotate', rotate_schedule))
    dp.add_handler(CommandHandler('help', help))

    # Register error handler
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is non-blocking
    # and will stop it gracefully
    updater.idle()


if __name__ == '__main__':
    main()
