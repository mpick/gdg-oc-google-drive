#!/usr/bin/python

import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

# Copy your credentials from the console
CLIENT_ID = '331847266991.apps.googleusercontent.com' #'YOUR_CLIENT_ID'
CLIENT_SECRET = 'PJNQLdTRMH0tlJuEcAfUU-Mu' #'YOUR_CLIENT_SECRET'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
FILENAME = 'document.txt'

# Path to the credentials
CRED_FILENAME = 'credentials'

### for storing token
storage = Storage(CRED_FILENAME)

if not storage.get():
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    ### Storing access token and a refresh token in CRED_FILENAME
    storage.put(credentials)
else:
    ### Getting access_token, expires_in,token_type,Refresh_token info from CRED_FILENAME to 'credentials'
    credentials = storage.get()

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': 'My document',
  'description': 'A test document',
  'mimeType': 'text/plain'
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)
