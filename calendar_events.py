from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dateutil.parser import parse as dtparse

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

import re
import os
import sys

# Specify calendar to SCAN google calendar
calendar_id = 'simula.no_9ga7rtt02pjcntlok16886rpjk@group.calendar.google.com'

class CalendarEvents:

    def __init__(self):
        """ setup Google Calendar API. """

        # generate directory with tokens etc for authorization
        self.generate_token_file()

        # get credentials from google API
        self.creds = None
        self.creds = Credentials.from_authorized_user_info(self.token)

        """
        # TODO: How to this without json files? seems like
        # InstalledAppFlow has no function from_client_secrets_info()..
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json')
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        """

        return

    def generate_token_file(self):

        # get environmental variables
        token = os.environ['GOOGLE_API_TOKEN']
        refresh_token = os.environ['GOOGLE_API_REFRESH_TOKEN']
        token_uri = os.environ['GOOGLE_API_TOKEN_URI']
        client_id = os.environ['GOOGLE_API_CLIENT_ID']
        client_secret = os.environ['GOOGLE_API_CLIENT_SECRET']
        scopes = os.environ['GOOGLE_API_SCOPES']
        expiry = os.environ['GOOGLE_API_EXPIRY']

        # data to be written
        token = {"token": token,
                 "refresh_token": refresh_token,
                 "token_uri": token_uri,
                 "client_id": client_id,
                 "client_secret": client_secret,
                 "scopes": [scopes],
                 "expiry": expiry}

        # serializing json
        self.token = token

        return

    def get_birthdays(self):

        # summary of calendar events
        summary = []

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # start today at 00:00
            today = datetime.datetime.today();
            start = (datetime.datetime(today.year, today.month, today.day, 00, 00)).isoformat() + 'Z'
            # end tomorrow at 00:00
            tomorrow = today + datetime.timedelta(days=1)
            end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'

            # get events from today
            events_result = service.events().list(calendarId=calendar_id,
                    timeMin=start, timeMax=end, timeZone="UTC",
                    singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            # add birthday events to summary
            for event in events:

                # check id event is birthday
                birthday_event = bool(re.search('birthday', event['summary']))

                # exclude OiO, seminars, dept. meetings and birthdays
                if birthday_event:
                    summary.append(event['summary'] + '\n')

            return summary

        except HttpError as error:
            print('An error occurred: %s' % error)

    def get_events(self):

        # summary of calendar events
        summary = ""
        # event counter
        i = 0

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # set range for the next 12 months
            start = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            end = (datetime.datetime.utcnow() + relativedelta(months=12)).isoformat('T') + "Z"

            # call API
            events_result = service.events().list(calendarId=calendar_id,
                    timeMin=start, timeMax=end,
                    singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            # if no events found, return
            if not events:
                summary += 'No events found. Please help populate the SCAN calendar :face_with_cowboy_hat:'
                return

            # Prints the start and name of the next 10 events
            for event in events:

                start = event['start'].get('dateTime', event['start'].get('date'))
                # gives date format '26 Dec'
                tmfmt = '%d.%m'

                # make date format look pretty
                stime = dt.strftime(dtparse(start), format=tmfmt)

                # check id event is optimization in Oslo seminar
                oio_event = bool(re.search('OiO', event['summary']))
                # check id event is SCAN department meeting
                dept_meeting_event = bool(re.search('SCAN weekly', event['summary']))
                # check id event is birthday
                birthday_event = bool(re.search('birthday', event['summary']))

                # exclude OiO, seminars, dept. meetings and birthdays
                if not (oio_event or dept_meeting_event or birthday_event):
                    summary += stime + ': ' + event['summary'] + '\n'
                    i += 1

                # if all events found are OiO, seminars, dept. meetings or birthdays
                if i >= 10:
                    return summary

            # if the only events 
            if len(summary) == 0:
                summary += 'No events found. Please help populate the SCAN calendar :face_with_cowboy_hat:'

            return summary

        except HttpError as error:
            print('An error occurred: %s' % error)

if __name__ == '__main__':

    C = CalendarEvents()
    print(C.get_events())
    print(C.get_birthdays())
