# Scopes required for this project
# gmail.modify is needed because we mark emails as read
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

# Full access is required to append rows
SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# Paste your Google Sheet ID here
SPREADSHEET_ID = "1hd676HZf_dN4QKIpyuPCCwRx9R3HGbSzwee-IzOJIW8"