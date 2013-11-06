#!/usr/bin/python

import httplib2
import pprint
import gzip
import os
import json

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

# Get your client secret / client id from the client_secret.json file
json_data = open('client_secret.json')
data = json.load(json_data)
CLIENT_ID = data["client_id"]
CLIENT_SECRET = data["client_secret"]
json_data.close()

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
indir = '/Users/miles/Documents/mysqlbkups/20131104'


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
parentId = '0B7OPm7m4AgrnQkd2Sjh3aUw4Zjg'
# Insert a file
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        print root + '/' + f
        # Gzip the file
        f_in = open( root + '/' + f, 'rb')
        f_out = gzip.open( f + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()

        media_body = MediaFileUpload(f + '.gz' , mimetype='text/plain', resumable=True)
        body = {
          'title': f + '.gz',
          'description': 'A SQL Backup File for the DME application',
          'mimeType': 'text/plain',
          'parents': [{'id':parentId}]
        }

        file = drive_service.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(file)
