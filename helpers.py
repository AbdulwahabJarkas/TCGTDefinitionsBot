from enum import Enum
import requests

POST_TO = 'https://api.groupme.com/v3/bots/post'

class errcol(Enum):
    severe  = '\033[31m[ SEVERE ]\033[00m '  # if something critical is caught
    warn    = '\033[33m[ WARN ]\033[0m '  # not critical, but still bad
    ok      = '\033[32m[ OK ]\033[00m '  # something good happens that might not always happen
    debug = '\033[35m[ BOT-DEBUG ]\033[00m '  # prefix for log entries when debugging
    log = '\033[36m[ BOT-LOG ]\033[00m '  # prefix for all other log entries
    usrmsg  = '\033[36m[ MESSAGE ]\033[00m '  # prefix for captured messages
    botmsg  = '\033[33m[ BOT MSG ]\033[00m '  # prefix for messages by the bot (  i.e. [ MESSAGE ] [ BOT ] Botname: Message  )
    sysmsg  = '\033[00m[ GroupMe ]\033[00m '  # Same as above, but for system messages like topic changes
    tail    = '\033[00m'  # suffix for log entries (normally just clears formatting)

def attach_type(attachments):
    types = {
            'image'    : '[IMG] ',
            'location' : '[LOC] ',
            'poll'     : '',
            'event'    : ''
            }
    typelist = ''
    for attachment in attachments:
        try:
            typelist += types[attachment['type']]
        except KeyError:
            print(errcol.warn.value + 'Attachment type {} unknown.'.format(attachment['type']) + errcol.tail.value)
    return typelist

def logmsg(data):
    try:
        sender_type = data['sender_type']
    except KeyError as missing_key:
        print(errcol.warn.value + "Message data does not contain a sender_type." + errcol.tail.value)
    else:
        if sender_type == 'user':
            print(errcol.usrmsg.value + "{}: {}{}".format(data['name'], attach_type(data['attachments']), data['text'])
                  + errcol.tail.value)
        elif sender_type == 'system':
            print(errcol.sysmsg.value + data['text'] + errcol.tail.value)
        elif sender_type == 'bot':
            print(errcol.botmsg.value + "{}: {}{}".format(data['name'], attach_type(data['attachments']) ,data['text'])
                  + errcol.tail.value)

def send_message(msg, bot_id):

    print(errcol.sysmsg.value + 'Posting Message' + msg + 'from' + bot_id + errcol.tail.value)

    data = {
            'bot_id' : bot_id,
            'text' : msg,
            }

    requests.post(POST_TO, json=data)
