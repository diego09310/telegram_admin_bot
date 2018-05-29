#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from telegram.error import Unauthorized
from telegram import ParseMode
import json
import logging
import datetime
from config import config_data
import re

groups_data = {}
admin_ids = []

logging.basicConfig(filename=config_data["log"]["logfile"], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=getattr(logging, config_data["log"]["level"]))
log = logging.getLogger()
   
def start(bot, update):
    if is_user_authorized(update.message.from_user.id):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hola, si apareces en mi lista de admins te notificaré cuando alguien invoque a los admins")
    else:
        unauthorized_user(bot, update, "start")

def bot_help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Esta es una lista de comandos que puedes usar para notificar a los admins del grupo: /spam, /notify_admins, /notificar_admins, /admins, /admin y puedes probar con @admin o @admins.")

def notify_admins(bot, update):
    log.info("chat_id" + str(update.message.chat_id))
    if is_message_from_known_group(update.message.chat_id):
        group_id = update.message.chat_id
        admins = get_admins_for_group(group_id)
        bot.sendMessage(chat_id=update.message.chat_id, text="Se ha avisado a los admins")
        for admin in admins:
            try:
                log.info(admin)
                username = update.message.from_user.username or update.message.from_user.first_name or ""
                group_link, username, message_text = sanitize(get_group_link(update.message.chat.id), username, update.message.text)
                bot.sendMessage(chat_id=admin["id"], text="Aviso en el grupo " + group_link + ": \n_" + username + ":_ " + message_text, parse_mode=ParseMode.MARKDOWN)
            except Unauthorized:
                log.error("Bot can't initiate conversation with user " + admin["name"] + ".")
    else:
        log.info("chat_id" + str(update.message.chat_id))
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando debe usarse desde un grupo que conozca el bot.")
        unauthorized_user(bot, update, "notify_admins")


def sanitize(*strings):
    return [re.sub(r'_', '\\_', i) for i in strings]

def is_user_authorized(user_id):
    admin_ids = get_admin_ids(groups_data)
    return user_id in admin_ids

def get_admin_ids(groups):
    global admin_ids
    if not admin_ids:
        admins = flatten_list([group["admins"] for group in groups])
        admin_ids = [admin["id"] for admin in admins]

    return admin_ids

def is_message_from_known_group(group_id):
    known_groups_ids = [group["id"] for group in groups_data]
    return group_id in known_groups_ids

def get_admins_for_group(group_id):
    group = [group for group in groups_data if group["id"] == group_id][0]
    return group["admins"]

def get_group_link(group_id):
    group = [group for group in groups_data if group["id"] == group_id][0]
    link = group["link"]
    if link is not None:
        return link
    else:
        return "@" + group.id

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def load_groups_data():
    global groups_data 
    groups_data = json.load(open(config_data["groups_data_file"]))["groups"]

def unauthorized_user(bot, update, command):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sólo los administradores tienen acceso a este bot.")
    f=open(config_data["log"]["unauthorized"], 'a')
    date=datetime.datetime.now()
    username = update.message.from_user.username or "_nousername_"
    name = update.message.from_user.first_name or "_noname_"
    last_name = update.message.from_user.first_name or "_noname_"
    log = "Date: " + date.strftime('%a %b %d %H:%M:%S %Y') + "\nUsername: " + update.message.from_user.username + " Name: " + update.message.from_user.first_name + " LastName: " + update.message.from_user.last_name + " ID: " + str(update.message.from_user.id) + "\nCommand: " + command
    f.write("%s\n" % log.encode("utf-8"))
    f.close()

def incorrect_data():
    log.warn("Incorrect data in groups.json")
    return

def ignore():
    return

def main():
    log.info("Starting bot...")

    load_groups_data()

    admin_bot = Updater(token=config_data["bot_token"])
    dispatcher = admin_bot.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', bot_help))
    # dispatcher.add_handler(CommandHandler('list_admins', list_admins))
    # dispatcher.add_handler(CommandHandler('add_admin', add_admin))
    # '@admin/@admins' is only detected when bot is not in privacy mode
    dispatcher.add_handler(RegexHandler('/notificar_admins|/notify_admins|/admin[s]*|/spam|@admin[s]*', notify_admins))
    nch_handler=MessageHandler(Filters.text, ignore)

    admin_bot.start_polling()
 
    admin_bot.idle()

if __name__ == '__main__':
    main()

