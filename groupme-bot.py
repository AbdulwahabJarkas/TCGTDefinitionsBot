"""
GroupMe Bot
Developed by Paul Pfeister, Sam Jarkas
"""

import os
import sys
import importlib
import json
from flask import Flask, request
from helpers import *
import gspread

'''
The bot will automatically log certain items, and log other items when DEBUG is set.
Some command lines might not show colors well, or they may overlap with your theme.
You can change the appearance of entries by replacing these values with other ANSI codes.
'''

#######################################################################################################
######################## Initialization ###############################################################
app = Flask(__name__)
gcp = gspread.service_account_from_dict(json.loads(os.getenv('CLIENT_SECRET')))

# To enable debugging the hard way, type 'True #' after 'Debug = '
DEBUG = (True if os.getenv('BOT_DEBUG') == 'True' else False)
POST_TO = 'https://api.groupme.com/v3/bots/post'
GROUP_RULES = {}
BOT_INFO = {}

if DEBUG:
    print(errcol.debug.value + "Web concurrency is set to " + os.getenv('WEB_CONCURRENCY') + errcol.tail.value)
    if os.getenv('WEB_CONCURRENCY') != '1':
        print(errcol.debug.value + "NOTE: When debugging with concurrency, you may see repetitive log entries."
              + errcol.tail.value)

# Parses bot data from the environment into the format { group_id : [bot_id, bot_name, sheets] }
for bot in (os.getenv('BOT_INFO')).split('; '):
    info = bot.split(', ')
    BOT_INFO[info[0]] = [info[1], info[2], gcp.open_by_key(info[3]) if info[3] != '0' else None]
    print(errcol.log.value + "Parsed Bot named {2} with ID {1} to Group with ID {0}, connected to Sheet ID {3}".format(
        *info)
          + errcol.tail.value)

# When you create global rules for the bot, they will be imported here.
# try:
#     GLOBAL_RULES = __import__('global_rules') #TODO Change to importlib.import_module
#     print(errcol.ok + "Global rules found and added." + errcol.tail)
# except ImportError:
#     print(errcol.warn + "Global rules not found. Bot may load, but it won't do anything." + errcol.tail)

# When you create custom rules for a group, they will be imported here.
for group in BOT_INFO:
    try:
        GROUP_RULES[group] = __import__('group_{}'.format(group))  # TODO Change to importlib.import_module
        print(errcol.ok.value + "Group rules found and added for [G:{}]".format(group) + errcol.tail.value)
    except ImportError:
        if group in GROUP_RULES: del GROUP_RULES[group]
        if DEBUG: print(errcol.debug.value + "Group rules not found for [G:{}]".format(group) + errcol.tail.value)


#######################################################################################################
######################## The actual bot ###############################################################

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    # if data['name'] == 'GroupMe':
    #     return "ok", 200

    if data['name'] == BOT_INFO[data['group_id']][1]:
        return "ok", 200

    logmsg(data)

    if data['group_id'] in GROUP_RULES:
        GROUP_RULES[data['group_id']].run(data, BOT_INFO[data['group_id']], send_message)
        if data['group_id'] == '84634591':
            print(data)
        return "ok", 200

    # global_rules.run(data, BOT_INFO[data['group_id']], send_message)

    return "ok", 200
