import re


def run(data, bot_info, send):
    if data['user_id'] == '0' and ('joined' in data['text'] or 'added' in data['text']):
        send("Welcome to the Trading Club GroupMe," + data['name'], bot_info[0])
        return True

    cmd = re.search(r'^!(\w+)', data['text'])

    if cmd:
        cmd = cmd.group(1).lower()

        if cmd == 'help':
            send("To use this bot, you must send a message in the format: '!command (paramater' \n"
                 "Currently, the only functional commands are !define (phrase) and !request (phrase). \n"
                 "For example, try !define bitcoin",
                 bot_info[0])

        elif cmd == 'define' or cmd == 'request':
            ws = bot_info[2].get_worksheet(0)
            term = data['text'].split(' ', 1)[1]
            loc = ws.find(re.compile(r'\b{}\b'.format(term), re.I))

            #TODO Add error handling for incorrect argument
            if not term.strip():
                return

            if loc:
                definition = ws.cell(loc.row, 3)

                if definition.value:
                    send("@{}, the definition of {} is: \n\n  {}".format(data['name'], loc.value, definition.value)
                         , bot_info[0])

                else:
                    send("@{}, Term '{}' has been requested, but not yet defined".
                         format(data['name'], term), bot_info[0])

            elif cmd == 'request':
                try:
                    ws.append_row([term])
                except:
                    send("@{}, an error occured when attempted to insert term '{}' into our database. Please contact"
                         " a moderator".format(data['name'], term), bot_info[0])
                else:
                    send("@{}, Term '{}' successfully added to our database, pending definition! "
                         "Thank you for your contribution".format(data['name'], term), bot_info[0])
            else:
                send("@{} Term '{}' has not been requested yet, "
                     "You can use the command !request (phrase) to add it to our requests database!".
                     format(data['name'], term), bot_info[0])

        else:
            send("Invalid command, type !help for more instructions", bot_info[0])

    return



