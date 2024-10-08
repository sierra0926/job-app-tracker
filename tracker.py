import os
import pickle
import base64

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'sierrasthomas@gmail.com'


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()

print("hello")

def getMessages():
    results = service.users().messages().list(userId='me',labelIds= ['Jobs'])
    messages = results.get("messages", [])

    if not results:
        print("label does not exist")
    else:
        message_count = 0
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            message_count = message_count + 1
            email_data = msg["payload"]["headers"]
            for values in email_data:
                name = values["name"]
                if name == "From":
                    from_name = values["value"]
                    print(from_name)
                    subject = [j["value"] for j in email_data if j["name"] == "Subject"]
                    print(subject)

            # I added the below script.
            for p in msg["payload"]["parts"]:
                if p["mimeType"] in ["text/plain", "text/html"]:
                    data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                    print(data)
getMessages()
    