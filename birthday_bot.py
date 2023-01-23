from slack_sdk.web import WebClient
from get_calendar_events import GetCalendarEvents

import os
import sys

if __name__ == '__main__':
    """Create message and post to slack channel with given channel id"""

    try:
        # set channel id
        channel_id = sys.argv[1]
    except:
        print('Please provide channel_id as cmd line argumente: \n $ python app_calendar.py  <channel_id>')
        sys.exit(2)

    # get birthdays from SCAN calendar
    C = GetCalendarEvents()
    birthdays = C.get_birthdays()

    # if none has birthday, exit
    if (len(birthdays) == 0):
       exit()

    # we need to pass the 'Bot User OAuth Token'
    slack_token = os.environ['SLACK_BOT_TOKEN']

    # creating an instance of the Webclient class
    client = WebClient(token=slack_token)

    # post birthday greeting(s) on Slack
    for birthday in birthdays:
        response = client.chat_postMessage(channel=channel_id,
                                       username="scanbot",
                                       icon_emoji=":robot_face:",
                                       text=birthday)
