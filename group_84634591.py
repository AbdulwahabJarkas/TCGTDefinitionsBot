import re


def run(data, bot_info, send):
    if data['user_id'] == '0' and ('joined' in data['text'] or 'added' in data['text']):
        send("Welcome to the Trading Club GroupMe," + data['name'], bot_info[0])
        return True

    cmd = re.search(r'^!(\w+)', data['text'])

    if cmd:
        cmd = cmd.group(1).lower()

        if cmd == 'help':
            send("Currently, the only functional command is !define (phrase). For example, try !define bitcoin",
                 bot_info[0])

        elif cmd == 'define':
            ws = bot_info[2].get_worksheet(0)
            term = data['text'].split(' ', 1)[1]
            loc = ws.find(re.compile(r'\b{}\b'.format(term), re.I))

            if loc:
                definition = ws.cell(loc.row, 3)

                if definition.value:
                    send("@{}, the definition of {} is: \n\n  {}".format(data['name'], loc.value, definition.value)
                         , bot_info[0])

                else:
                    send("Term has been requested, but not yet defined", bot_info[0])

            else:
                send("Term has not been requested yet", bot_info[0])

        else:
            send("Incorrect command, type !help for more instructions", bot_info[0])

    return



