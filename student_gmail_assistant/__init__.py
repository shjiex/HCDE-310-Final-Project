import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from .demo_data import get_demo_messages
from .email_analyzer import analyze_messages
from .google_services import (
    GoogleApiError,
    complete_oauth_flow,
    credentials_configured,
    get_gmail_service,
    load_credentials,
    save_credentials,
    start_oauth_flow,
)

load_dotenv()


def create_app():
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )

    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    app.config["CLIENT_SECRETS_FILE"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRETS", "credentials.json")
    app.config["TOKEN_FILE"] = "token.json"

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    @app.route("/", methods=["GET", "POST"])
    def index():
        mode = request.values.get("mode", "demo")
        query = request.values.get("query", "newer_than:21d")
        messages = get_demo_messages()
        source_label = "Demo dataset"
        google_ready = credentials_configured(app.config["CLIENT_SECRETS_FILE"])
        google_connected = bool(load_credentials(app.instance_path, app.config["TOKEN_FILE"]))

        if request.method == "POST" and mode == "live":
            if not google_connected:
                flash("Connect Google first, or switch to demo mode.", "warning")
            else:
                try:
                    creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
                    gmail_service = get_gmail_service(creds)
                    messages = gmail_service.fetch_recent_messages(
                        query=query,
                        max_results=20,
                        unread_only=False,
                    )
                    source_label = "Live Gmail inbox"
                except GoogleApiError as exc:
                    flash(str(exc), "error")

        analyzed = analyze_messages(messages)

        return render_template(
            "index.html",
            emails=analyzed,
            prefs={"mode": mode, "query": query},
            source_label=source_label,
            google_ready=google_ready,
            google_connected=google_connected,
        )

    @app.route("/email/<message_id>/star", methods=["POST"])
    def star_email(message_id):
        if message_id.startswith("demo-"):
            return jsonify(ok=True)
        creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
        if not creds:
            return jsonify(ok=False, error="Not connected"), 401
        try:
            starred = request.json.get("starred", True)
            get_gmail_service(creds).star_message(message_id, starred)
            return jsonify(ok=True)
        except GoogleApiError as exc:
            return jsonify(ok=False, error=str(exc)), 500

    @app.route("/email/<message_id>/trash", methods=["POST"])
    def trash_email(message_id):
        if message_id.startswith("demo-"):
            return jsonify(ok=True)
        creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
        if not creds:
            return jsonify(ok=False, error="Not connected"), 401
        try:
            get_gmail_service(creds).trash_message(message_id)
            return jsonify(ok=True)
        except GoogleApiError as exc:
            return jsonify(ok=False, error=str(exc)), 500

    @app.route("/connect/google")
    def connect_google():
        if not credentials_configured(app.config["CLIENT_SECRETS_FILE"]):
            flash(
                "Add your Google OAuth client file as credentials.json before connecting.",
                "error",
            )
            return redirect(url_for("index"))

        flow, auth_url, state, code_verifier = start_oauth_flow(
            app.config["CLIENT_SECRETS_FILE"],
            url_for("oauth_callback", _external=True),
        )
        session["oauth_state"] = state
        session["oauth_redirect_uri"] = flow.redirect_uri
        session["oauth_code_verifier"] = code_verifier
        return redirect(auth_url)

    @app.route("/disconnect/google")
    def disconnect_google():
        token_path = Path(app.instance_path) / app.config["TOKEN_FILE"]
        token_path.unlink(missing_ok=True)
        flash("Google account disconnected.", "success")
        return redirect(url_for("index"))

    @app.route("/oauth2callback")
    def oauth_callback():
        try:
            creds = complete_oauth_flow(
                app.config["CLIENT_SECRETS_FILE"],
                session.get("oauth_redirect_uri") or url_for("oauth_callback", _external=True),
                state=session.get("oauth_state"),
                authorization_response=request.url,
                code_verifier=session.get("oauth_code_verifier"),
            )
        except GoogleApiError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        save_credentials(app.instance_path, app.config["TOKEN_FILE"], creds)
        flash("Google account connected! Set source as live Gmail and click ANALYZE INBOX to see your email.", "success")
        return redirect(url_for("index", mode="live"))

    return app
