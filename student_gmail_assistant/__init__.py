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

ANALYSIS_BATCH_SIZE = 50


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
        per_page = request.values.get("per_page", "10")
        analysis_started = request.method == "POST"
        messages = get_demo_messages()
        google_ready = credentials_configured(app.config["CLIENT_SECRETS_FILE"])
        google_connected = bool(load_credentials(app.instance_path, app.config["TOKEN_FILE"]))

        has_more = False

        if request.method == "POST" and mode == "live":
            if not google_connected:
                flash("Connect Google first, or switch to demo mode.", "warning")
            else:
                try:
                    creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
                    gmail_service = get_gmail_service(creds)
                    messages, next_token = gmail_service.fetch_recent_messages(
                        query=query,
                        max_results=ANALYSIS_BATCH_SIZE,
                    )
                    session["next_page_token"] = next_token
                    session["last_query"] = query
                    has_more = bool(next_token)
                except GoogleApiError as exc:
                    flash(str(exc), "error")

        analyzed = analyze_messages(messages)

        return render_template(
            "index.html",
            emails=analyzed,
            prefs={"mode": mode, "query": query, "per_page": per_page},
            google_ready=google_ready,
            google_connected=google_connected,
            analysis_started=analysis_started,
            has_more=has_more,
        )

    @app.route("/load-more", methods=["POST"])
    def load_more():
        page_token = session.get("next_page_token")
        if not page_token:
            return jsonify(ok=False, error="No more emails"), 400
        creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
        if not creds:
            return jsonify(ok=False, error="Not connected"), 401
        try:
            query = session.get("last_query", "newer_than:21d")
            gmail_service = get_gmail_service(creds)
            messages, next_token = gmail_service.fetch_recent_messages(
                query=query,
                max_results=ANALYSIS_BATCH_SIZE,
                page_token=page_token,
            )
            session["next_page_token"] = next_token
            analyzed = analyze_messages(messages)
            html = render_template("_email_cards.html", emails=analyzed)
            return jsonify(ok=True, html=html, has_more=bool(next_token))
        except GoogleApiError as exc:
            return jsonify(ok=False, error=str(exc)), 500

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

    @app.route("/email/<message_id>/read", methods=["POST"])
    def read_email(message_id):
        if message_id.startswith("demo-"):
            return jsonify(ok=True)
        creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
        if not creds:
            return jsonify(ok=False, error="Not connected"), 401
        try:
            read = request.json.get("read", True)
            get_gmail_service(creds).mark_read(message_id, read)
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

    @app.route("/email/<message_id>/untrash", methods=["POST"])
    def untrash_email(message_id):
        if message_id.startswith("demo-"):
            return jsonify(ok=True)
        creds = load_credentials(app.instance_path, app.config["TOKEN_FILE"])
        if not creds:
            return jsonify(ok=False, error="Not connected"), 401
        try:
            get_gmail_service(creds).untrash_message(message_id)
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
        flash("Google account connected! Choose demo data or live Gmail, then click ANALYZE INBOX.", "success")
        return redirect(url_for("index"))

    return app
