from slack_sdk.web import WebClient
from get_calendar_events import GetCalendarEvents

import os
import sys
import re

if __name__ == '__main__':
    """Create message and post to slack channel with given channel id"""

    try:
        # set channel id
        channel_id = sys.argv[1]
    except:
        print('Please provide channel_id as cmd line argumente: \n $ python app_calendar.py  <channel_id>')
        sys.exit(2)

    # get email addresses of those who have birthday today
    C = GetCalendarEvents()
    emails = C.get_birthdays()

    # exit if no one has birthday
    if (len(emails) == 0):
       exit()

    # we need to pass the 'Bot User OAuth Token'
    slack_token = os.environ['SLACK_BOT_TOKEN']

    # creating an instance of the Webclient class
    client = WebClient(token=slack_token)

    # post birthday greeting(s) on Slack
    for email in emails:
        # get slack user name
        user_name = client.users_lookupByEmail(email=email)['user']['name']

        # construct and post message
        message = "Happy birthday, <@" + user_name + ">! :tada: \n"
        response = client.chat_postMessage(channel=channel_id,
                                       username="scanbot",
                                       icon_emoji=":robot_face:",
                                       text=message)
