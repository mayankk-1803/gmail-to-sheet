import base64

MAX_CONTENT_LENGTH = 10000  # keep safely under Google Sheets limit


def parse_email(message):
    headers = message["payload"].get("headers", [])
    header_map = {}

    for h in headers:
        header_map[h["name"]] = h["value"]

    body_text = ""
    payload = message["payload"]

    # Handle multipart emails
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and part["body"].get("data"):
                body_text = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
                break
    else:
        if payload["body"].get("data"):
            body_text = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")

    # Trim long email bodies to avoid Google Sheets cell limit
    if len(body_text) > MAX_CONTENT_LENGTH:
        body_text = body_text[:MAX_CONTENT_LENGTH] + " ...[truncated]"

    return {
        "from": header_map.get("From", ""),
        "subject": header_map.get("Subject", ""),
        "date": header_map.get("Date", ""),
        "content": body_text.strip()
    }
