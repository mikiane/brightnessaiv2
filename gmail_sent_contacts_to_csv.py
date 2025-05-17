#!/usr/bin/env python3
"""Extract recipient names and emails from Gmail sent messages.

This script uses the Gmail API to list messages in the user's
'Sent' mailbox, parse the "To" header, and save a CSV file with
unique name/email pairs.

Usage:
  1. Enable the Gmail API on https://console.cloud.google.com/
  2. Create OAuth client credentials and download ``credentials.json``
  3. Install dependencies from ``requirements.txt`` or run:
       pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  4. Run the script: ``python gmail_sent_contacts_to_csv.py``
The first run will open a browser for authentication and create a
``token.json`` file for reuse.
"""

from __future__ import annotations

import csv
import os
from email.utils import getaddresses

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_service() -> "Resource":
    """Return an authorized Gmail API service instance."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def extract_contacts(service: "Resource", max_results: int = 500) -> dict[str, str]:
    """Return a mapping of email -> name from the user's sent messages."""
    results = service.users().messages().list(
        userId="me", labelIds=["SENT"], maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    contacts: dict[str, str] = {}
    for msg in messages:
        msg_detail = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["To"])
            .execute()
        )
        headers = msg_detail.get("payload", {}).get("headers", [])
        for header in headers:
            if header.get("name") == "To" and header.get("value"):
                for name, email in getaddresses([header["value"]]):
                    email = email.strip()
                    if email and email not in contacts:
                        contacts[email] = name
    return contacts


def save_to_csv(contacts: dict[str, str], filename: str = "sent_contacts.csv") -> None:
    """Write the contact dictionary to ``filename`` as CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email"])
        for email, name in contacts.items():
            writer.writerow([name, email])


def main() -> None:
    service = get_service()
    contacts = extract_contacts(service)
    save_to_csv(contacts)
    print(f"Saved {len(contacts)} contacts to sent_contacts.csv")


if __name__ == "__main__":
    main()
