import base64
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GoogleApiError(Exception):
    pass


def credentials_configured(client_secrets_file):
    return Path(client_secrets_file).exists()


def load_credentials(instance_path, token_file):
    token_path = Path(instance_path) / token_file
    if not token_path.exists():
        return None

    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    # If the saved token expired, refresh it automatically
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())
    return creds


def save_credentials(instance_path, token_file, creds):
    token_path = Path(instance_path) / token_file
    token_path.write_text(creds.to_json())


def start_oauth_flow(client_secrets_file, redirect_uri):
    """Step 1 of Google login: redirect the user to Google's sign-in page."""
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=SCOPES,
            redirect_uri=redirect_uri,
        )
        auth_url, state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
        )
        return flow, auth_url, state, flow.code_verifier
    except FileNotFoundError as exc:
        raise GoogleApiError("Google OAuth client file not found.") from exc
    except Exception as exc:
        raise GoogleApiError(f"Unable to start Google OAuth flow: {exc}") from exc


def complete_oauth_flow(client_secrets_file, redirect_uri, state, authorization_response, code_verifier=None):
    """Step 2 of Google login: exchange the code Google sent back for real credentials."""
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=SCOPES,
            state=state,
            redirect_uri=redirect_uri,
        )
        flow.code_verifier = code_verifier
        flow.fetch_token(authorization_response=authorization_response)
        return flow.credentials
    except Exception as exc:
        raise GoogleApiError(f"Unable to complete Google OAuth flow: {exc}") from exc


class GmailClient:
    def __init__(self, service):
        self.service = service

    def star_message(self, message_id, starred):
        labels_to_add = ["STARRED"] if starred else []
        labels_to_remove = [] if starred else ["STARRED"]
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"addLabelIds": labels_to_add, "removeLabelIds": labels_to_remove},
            ).execute()
        except HttpError as exc:
            raise GoogleApiError(f"Failed to update star: {exc}") from exc

    def mark_read(self, message_id, read):
        labels_to_add = [] if read else ["UNREAD"]
        labels_to_remove = ["UNREAD"] if read else []
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"addLabelIds": labels_to_add, "removeLabelIds": labels_to_remove},
            ).execute()
        except HttpError as exc:
            raise GoogleApiError(f"Failed to update read status: {exc}") from exc

    def trash_message(self, message_id):
        try:
            self.service.users().messages().trash(userId="me", id=message_id).execute()
        except HttpError as exc:
            raise GoogleApiError(f"Failed to trash message: {exc}") from exc

    def untrash_message(self, message_id):
        try:
            self.service.users().messages().untrash(userId="me", id=message_id).execute()
        except HttpError as exc:
            raise GoogleApiError(f"Failed to untrash message: {exc}") from exc

    def fetch_recent_messages(self, query, max_results=100, page_token=None):
        try:
            kwargs = {"userId": "me", "q": query.strip(), "maxResults": min(max_results, 500)}
            if page_token:
                kwargs["pageToken"] = page_token
            response = self.service.users().messages().list(**kwargs).execute()
            refs = response.get("messages", [])
            next_token = response.get("nextPageToken")
            messages = [get_message_details(self.service, ref["id"]) for ref in refs]
            return messages, next_token
        except HttpError as exc:
            raise GoogleApiError(f"Failed to fetch Gmail messages: {exc}") from exc


def get_message_details(service, message_id):
    payload = (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="full")
        .execute()
    )
    headers = {h["name"]: h["value"] for h in payload.get("payload", {}).get("headers", [])}

    return {
        "id": payload["id"],
        "thread_id": payload.get("threadId"),
        "subject": headers.get("Subject", "(No subject)"),
        "sender": headers.get("From", "Unknown sender"),
        "snippet": payload.get("snippet", ""),
        "body": _extract_body(payload.get("payload", {})),
        "timestamp": payload.get("internalDate"),
        "label_ids": payload.get("labelIds", []),
        "thread_url": f"https://mail.google.com/mail/u/0/#inbox/{payload.get('threadId')}",
    }


def _extract_body(part):
    """Recursively pull the plain-text (or HTML) body out of a MIME message part."""
    if not part:
        return ""

    body = part.get("body", {})
    data = body.get("data")
    if data and part.get("mimeType") in {"text/plain", "text/html"}:
        return _decode_base64(data)

    for child in part.get("parts", []):
        value = _extract_body(child)
        if value:
            return value
    return ""


def _decode_base64(data):
    # Gmail encodes email bodies in base64url. Pad it to a multiple of 4, then decode.
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="ignore")


def get_gmail_service(creds):
    try:
        service = build("gmail", "v1", credentials=creds)
        return GmailClient(service)
    except Exception as exc:
        raise GoogleApiError(f"Unable to initialize Gmail service: {exc}") from exc
