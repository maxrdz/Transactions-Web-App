import os
from flask import Flask, send_from_directory, redirect, url_for
from flask import request, make_response, Request
from flask_session.sessions import SqlAlchemySession
from webserver.Localizer import Localizer
from webserver.Database import DatabaseManager

# Flask Session Type
SESSION_TYPE = 'sqlalchemy'


class FlaskWebApp:
    """
    Main class, initializes Flask server and
    programs website routes and languages.
    """
    def __init__(self):
        self.HOST = "0.0.0.0"
        self.PORT = 80  # HTTP
        self.ROOT_DIR = "www"
        self.HTTP_ERR = "http_error/"
        # Flask initialize
        self.Flask = Flask(__name__, template_folder=self.ROOT_DIR)
        self.Session = SqlAlchemySession()
        self.Flask.config.update(SECRET_KEY=str(os.urandom(16)))
        # Project Modules
        self.Localizer = Localizer()
        self.Database = DatabaseManager()

        # User Authentication
        @self.Flask.route("/auth", methods=["POST"])
        def authentication_form():
            # Check if user already has a session cookie
            session_check = self.check_session_cookie(request)
            if session_check:
                check_resp = session_check[0]
                check_status = session_check[1]

                if check_status is False:
                    return check_resp  # Send error response
                else:
                    # Authenticated with an existing session.
                    return redirect(url_for("user_panel"))

            form = request.form
            username = form['username']
            password = form['password']
            auth = self.Database.authenticate_user(username, password)

            if auth:
                if auth == [True, True]:
                    # User authenticated successfully.
                    session_id = self.Database.create_session(username)

                    # Create response with Session ID cookie & user
                    response = make_response("<h1>Authenticated!</h1>")
                    response.set_cookie('User', username)
                    response.set_cookie('SessionID', str(session_id))
                    return response
                else:
                    # User was not authenticated.
                    return redirect(url_for("root"))
            else:
                # User account is not activated. (Disabled)
                return "<h1>Sorry, your account is disabled.</h1>"

        # User Panel Page
        @self.Flask.route("/panel", methods=["GET"])
        def user_panel():
            session_check = self.check_session_cookie(request)
            if not session_check:  # Redirect unauthorized requests
                return redirect("root")

            lang = self.check_language_cookie(request)
            return self.Localizer.localize_html(lang, "panel.html")

        # User Login Screen
        @self.Flask.route("/login", methods=["GET"])
        def user_login():
            lang = self.check_language_cookie(request)
            return self.Localizer.localize_html(lang, "login.html")

        # Set new preferred language cookie
        @self.Flask.route("/lang", methods=["POST"])
        def request_language():
            language = request.form['lang']
            response = make_response(redirect("root"))
            response.set_cookie('language', language)
            return response

        # Serve Static Files
        @self.Flask.route("/<path:path>", methods=["GET"])
        def static_content(path):
            """Send static content such as CSS and images."""
            return send_from_directory(self.ROOT_DIR, path)

        # Website Root
        @self.Flask.route("/", methods=["GET"])
        def root():
            """
            Website root, redirect to session language.
            If the client has no language cookie set, use default.
            """
            session_check = self.check_session_cookie(request)
            if session_check:
                return redirect(url_for("user_panel"))  # Redirect to user panel.

            return redirect(url_for("user_login"))  # New user, send to login page.

        # HTTP Code 404 Page
        @self.Flask.errorhandler(404)
        def http_not_found(err_msg):
            """Return 'HTTP 404: Not Found' page"""
            lang = self.check_language_cookie(request)
            return self.Localizer.localize_html(
                lang, f"{self.HTTP_ERR}404.html")

    def check_language_cookie(self, req: Request):
        """
        Check for a preferred language cookie, returns language.
        """
        language = req.cookies.get('language')
        # Return if no language cookie found.
        if language is None:
            return self.Localizer.DEFAULT

        # If cookie exists, detect language.
        try:
            dummy = self.Localizer.LANG[language]
        except KeyError:
            # Language invalid, return default
            return self.Localizer.DEFAULT

        return language  # Valid language detected

    def check_session_cookie(self, req: Request):
        """
        Check if user has a Session ID cookie using request given.
        Returns an array [response, status].
        """
        session_id = req.cookies.get('SessionID')

        # Return None if no Session ID cookie was found.
        if session_id is None:
            return None

        username = req.cookies.get('User')
        # If there is no Username cookie, clear SID.
        if username is None:
            response = make_response()
            response.delete_cookie('SessionID')
            return [response, False]

        valid = self.Database.validate_session(username, session_id)
        if valid:
            self.Database.renew_session(username)  # Update expiration timestamp
            return [None, True]
        else:
            # Session is invalid, clear the user's cookie.
            response = make_response()
            response.delete_cookie('SessionID')
            return [response, False]

    def notify(self, string):
        print(f"[{self.__class__.__name__}]: {string}")

    def launch(self):
        """Starts the Flask web server with host/port."""
        if __name__ == "__main__":
            self.Flask.run(host=self.HOST, port=self.PORT)


# Launch the flask web server
WebApp = FlaskWebApp()
WebApp.launch()
