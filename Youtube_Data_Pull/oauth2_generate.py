from __future__ import print_function
import httplib2
import os
import pandas as pd
import sys
import csv
import datetime

from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.



# Remove keyword arguments that are not set
#
def get_authenticated_service():
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    flow=flow_from_clientsecrets(CLIENT_SECRETS_FILE,scope=SCOPES)
    #Storage("%s-oauth2.json"% sys.argv[0])
    storage=Storage("youtube_data.py-oauth2.json")
    credentials=storage.get()
    if credentials is None or credentials.invalid:
        credentials=tools.run_flow(flow,storage)
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)



client = get_authenticated_service()
print('oauth2.py generated')
