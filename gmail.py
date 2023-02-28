from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
from pprint import pprint

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def send_message(service, sender, recipient, subject, message_text):
    message = EmailMessage()

    message.set_content(message_text)

    message['To'] = recipient
    message['From'] = sender
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')


def main():
    service = get_service()

    kuldo = input("Ki legyen az e-mail küldője?: ")
    cimzett = input("Ki legyen az e-mail címzettje?: ")
    targy = input("Írd be az e-mail tárgyát: ")
    uzenetSzovege = input("Írd be az e-mail üzenetének a szövegét: ")

    send_message(service, kuldo, cimzett, targy, uzenetSzovege)

main()