# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
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

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# Specify calendar is form SCAN calendar
calendar_id = 'simula.no_9ga7rtt02pjcntlok16886rpjk@group.calendar.google.com'

class CalendarEvents:

    def __init__(self):
        """ setup Google Calendar API. """

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        return

    def get_birthdays(self):

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # summary of calendar events
            summary = []

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

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # summary of calendar events
            summary = ""
            # event counter
            i = 0

            # set range for the next 12 months
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            inAmonth = (datetime.datetime.utcnow() + relativedelta(months=12)).isoformat('T') + "Z"

            # call API
            events_result = service.events().list(calendarId=calendar_id,
                    timeMin=now, timeMax=inAmonth,
                    singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                summary += 'No upcoming events found.'
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

                # only include up to 10 events
                if i > 10:
                    return summary

            return summary

        except HttpError as error:
            print('An error occurred: %s' % error)

if __name__ == '__main__':

    C = CalendarEvents()
    print(C.get_events())
    print(C.get_birthdays())
