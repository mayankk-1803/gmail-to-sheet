from googleapiclient.discovery import build


def append_rows(credentials, spreadsheet_id, rows):
    service = build("sheets", "v4", credentials=credentials)

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:E",  # 5 columns now
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()
