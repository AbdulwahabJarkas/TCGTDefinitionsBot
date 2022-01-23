import re

def run(data, bot_info, send):
    if data['user_id'] == '0' and ('joined' in data['text'] or 'added' in data['text']):
        send("Welcome to the Trading Club GroupMe," + data['name'], bot_info[0])
        return True

    cmd = re.search(r'^!(\w+)', data['text'])
    if cmd:
        cmd = cmd.group(1)

        if cmd == 'help':
            send("Help command is under construction", bot_info[0])

        if cmd == 'define':
            send("Define command is under construction", bot_info[0])

        else:
            send("Incorrect command, type !help for more instructions")

    return



