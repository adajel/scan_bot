import json
import os

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
json_object = json.dumps(token, indent=7)

print(json_object)
 
with open("token.json", "w") as outfile:
    outfile.write(json_object)

#credentials = {'client_id': '162572154667-t93qvhq7uue66oee5mjium23jhkk9ga8.apps.googleusercontent.com',
#               'project_id': 'get-calendar-events-2023',
#               'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
#               'token_uri': 'https://oauth2.googleapis.com/token',
#               'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
#               'client_secret': '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',
#               'redirect_uris': ['http://localhost']}


