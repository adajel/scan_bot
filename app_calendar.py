from slack_sdk.web import WebClient
from calendar_events import CalendarEvents

import os

class Message:
    """Constructs the text to be displayed"""

    TITLE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
            "Upcoming conferences, visits and other events from the SCAN calendar: \n\n"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "scanbot"
        self.icon_emoji = ":calendar:"
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.TITLE_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_events_block(),
            ],
        }

    def _get_events_block(self):
        #task_checkmark = self._get_checkmark(self.reaction_task_completed)

        # get calendar events to post
        C = CalendarEvents()
        calendar_events = C.get_events()

        text = (
            calendar_events
        )
        information = (
            "Add your conferences and events via the <https://tinyurl.com/5n8zn827|SCAN google calendar>"
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

    # set channel_id
    channel_id="C04KGDHATRA"

    # we need to pass the 'Bot User OAuth Token'
    slack_token = os.environ['SLACK_BOT_TOKEN']

    # creating an instance of the Webclient class
    client = WebClient(token=slack_token)

    # get message from SCAN calendar
    M = Message(channel_id)
    message = M.get_message_payload()

    # post message on Slack
    response = client.chat_postMessage(**message)
