from slack_sdk.web import WebClient
#from calendar_events import CalendarEvents

import os
import sys

if __name__ == '__main__':

    # set channel ID
    channel_id="C04KGDHATRA"

    # get birthdays from SCAN calendar
    #C = CalendarEvents()
    #birthdays = C.get_birthdays()
    birthdays = "test"

    # if none has birthday, exit
    if (len(birthdays) == 0):
        sys.exit(0)

    # we need to pass the 'Bot User OAuth Token'
    slack_token = os.environ.get('SLACK_BOT_TOKEN')

    # creating an instance of the Webclient class
    client = WebClient(token=slack_token)

    # post birthday greeting(s) on Slack
    for birthday in birthdays:
        response = client.chat_postMessage(channel=channel_id,
                                       username="scanbot",
                                       icon_emoji=":robot_face:",
                                       text=birthday)
