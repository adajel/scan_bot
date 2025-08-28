from slack_sdk.web import WebClient
from get_calendar_events import GetCalendarEvents

import os
import sys

class Message:
    """Constructs the text to be displayed"""

    TITLE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
            "Upcoming conferences and other relevant events from the SCAN calendar: \n\n"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.username = "scanbot"
        self.icon_emoji = ":calendar:"
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "channel": self.channel_id,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "unfurl_links": False,
	        "unfurl_media": False,
            "blocks": [
                self.TITLE_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_events_block(),
            ],
        }

    def _get_events_block(self):
        # get calendar events to post
        C = GetCalendarEvents()
        calendar_events = C.get_events()

        text = (
            calendar_events
        )
        information = (
            "Add new events via the <https://tinyurl.com/5n8zn827|SCAN calendar>."
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "divider"},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]

if __name__ == '__main__':
    """Create message and post to slack channel with given channel id"""
    try:
        # set channel id
        channel_id = sys.argv[1]
    except:
        print('Please provide channel_id as cmd line argumente: \n $ python app_calendar.py  <channel_id>')
        sys.exit(2)

    # we need to pass the 'Bot User OAuth Token'
    slack_token = os.environ['SLACK_BOT_TOKEN']

    # creating an instance of the Webclient class
    client = WebClient(token=slack_token)

    # get message from SCAN calendar
    M = Message(channel_id)
    message = M.get_message_payload()

    # post message on Slack
    response = client.chat_postMessage(**message)
