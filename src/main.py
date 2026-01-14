import time
from src.auth import get_credentials
from src.gmail_service import get_gmail_service
from src.sheets_service import append_rows
from src.email_parser import parse_email
from src.config import SPREADSHEET_ID


def main():
    credentials = get_credentials()
    gmail = get_gmail_service(credentials)

    # Only emails from last 24 hours
    one_day_ago = int(time.time()) - (24 * 60 * 60)

    response = gmail.users().messages().list(
        userId="me",
        q=f"is:unread in:inbox after:{one_day_ago}"
    ).execute()

    messages = response.get("messages", [])
    sheet_rows = []

    for item in messages:
        msg = gmail.users().messages().get(
            userId="me",
            id=item["id"],
            format="full"
        ).execute()

        email = parse_email(msg)

        # Exclude automated / no-reply emails
        sender = email["from"].lower()
        if "no-reply" in sender or "noreply" in sender:
            continue

        sheet_rows.append([
            email["from"],
            email["subject"],
            email["date"],
            email["content"],
            email["labels"]
        ])

        # Mark email as read
        gmail.users().messages().modify(
            userId="me",
            id=item["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    if sheet_rows:
        append_rows(credentials, SPREADSHEET_ID, sheet_rows)
        print(f"{len(sheet_rows)} emails logged successfully.")
    else:
        print("No qualifying emails found.")


if __name__ == "__main__":
    main()
