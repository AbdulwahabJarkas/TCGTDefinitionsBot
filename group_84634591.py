import gspread
import os, json


def runws(data, bot_info, send):
    creds = json.loads(os.getenv('CLIENT_SECRET'))
    print(creds, os.getenv('CLIENT_SECRET'))
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open_by_key('1yHAFFnvAwJ3IRmLIk-xK01OHaN_R0xbl3JFCGUFissQ')
    worksheet = sh.get_worksheet(0)
    values_list = worksheet.row_values(1)

    send(str(values_list), bot_info[0])

    return True


def run(data, bot_info, send):
    help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."

    message = data['text']

    if message == '.help':
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send("Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    send("Hi {}! You said: {}".format(data['name'], data['text']), bot_info[0])
    return True
