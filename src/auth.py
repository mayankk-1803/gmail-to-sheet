import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from src.config import GMAIL_SCOPES, SHEETS_SCOPES


SCOPES = GMAIL_SCOPES + SHEETS_SCOPES


def get_credentials():
    creds = None

    # Load existing token if available
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If token is missing or invalid, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return creds
