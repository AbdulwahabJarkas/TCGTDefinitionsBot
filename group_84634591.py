import re


def run(data, bot_info, send):
    if data['user_id'] == '0' and ('joined' in data['text'] or 'added' in data['text']):
        send("Welcome to the Trading Club GroupMe," + data['name'], bot_info[0])
        return True

    cmd = re.search(r'^!(\w+)', data['text'])

    if cmd:
        cmd = cmd.group(1).lower()
        msg = ''
        attachment = None

        if cmd == 'help':
            msg = helper()
        elif cmd == 'define':
            msg, attachment = define(data, bot_info[2].get_worksheet(0))
        elif cmd == 'request':
            msg, attachment = request(data, bot_info[2].get_worksheet(0))
        else:
            msg = "Invalid command, type !help for more instructions"

        send(msg, bot_info[0], attachment)

    return


def helper():
    return "To use this bot, you must send a message in the format: \n\n'!command (paramater)' \n\n " \
           "Currently, the only functional commands are !define (phrase) and !request (phrase). \n\n " \
           "For example, try !define bitcoin"


def define(data, ws):
    # Get Argument Error Handling
    term = data['text'].split(' ', 1)
    if len(term) == 1 or not term[1].strip():
        return "Invalid command formatting, type !help for more instructions", None
    term = term[1].strip()

    # Check Definitions, then aliases.
    loc = ws.find(re.compile(r'^\s*{}\s*$'.format(term), re.I))
    if not loc:
        loc = ws.find(re.compile(r'\b{}\b'.format(term), re.I))

    attachment = [{"loci": [[0, 0]], "type": "mentions", "user_ids": [data['user_id']]}]

    #Check For Definition
    if loc:
        definition = ws.cell(loc.row, 2)
        if loc.col != 1:
            loc = ws.cell(loc.row, 1)

        if definition.value:
            return "@{a}, the definition of {b} is: \n\n{c}"\
                       .format(a=data['name'], b=loc.value, c=definition.value), attachment
        else:
            return "@{}, term '{}' has been requested but not yet defined"\
                       .format(data['name'], term), attachment

    return "@{} Term '{}' has not been requested or aliased yet. " \
           "You can use the command !request (phrase) to add it to our requests database!"\
               .format(data['name'], term), attachment


def request(data, ws):
    # Get Argument Error Handling
    term = data['text'].split(' ', 1)
    if len(term) == 1 or not term[1].strip():
        return "Invalid command formatting, type !help for more instructions", None
    term = term[1].strip()

    # Check Definitions, then aliases.
    loc = ws.find(re.compile(r'^\s*{}\s*$'.format(term), re.I))
    if not loc:
        loc = ws.find(re.compile(r'\b{}\b'.format(term), re.I))
        #Alias Incorrectly identified in col 1
        loc = None if loc.col == 1 else loc

    attachment = [{"loci": [[0, 0]], "type": "mentions", "user_ids": [data['user_id']]}]

    #Check For Definition
    if loc:
        if loc.col != 1:
            loc = ws.cell(loc.row, 1)
        definition = ws.cell(loc.row, 2)

        if definition.value:
            return "@{a}, the definition {b} of is: \n\n{c}".format(a=data['name'], b=loc.value, c=definition.value), attachment
        else:
            return "@{}, term '{}' has been requested but not yet defined"\
                       .format(data['name'], term), attachment

    #Append To Sheets DB
    try:
        ws.append_row([term, '', '', "{}, {}".format(data['user_id'], data['name'])])
    except:
        return "@{}, an error occured when attempting to insert term '{}' into our database. Please contact " \
               "a moderator".format(data['name'], term), attachment
    else:
        return "@{}, Term '{}' successfully added to our database, pending definition! " \
               "Thank you for your contribution".format(data['name'], term), attachment


