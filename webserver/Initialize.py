import os
from flask import Flask, send_from_directory, redirect, url_for
from flask import request, make_response, Request
from flask_session.sessions import SqlAlchemySession
from webserver.Localizer import SpanishLocalizer, EnglishLocalizer
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
        self.INDEX_PAGE = "login.html"
        self.HTTP_ERR = "http_error/"
        self.Flask = Flask(__name__, template_folder=self.ROOT_DIR)
        self.Session = SqlAlchemySession()
        # Required to create a Session secret key for Session
        self.Flask.config.update(SECRET_KEY=str(os.urandom(16)))

        self.SpanishLocalizer = SpanishLocalizer()
        self.EnglishLocalizer = EnglishLocalizer()
        self.DEFAULT_LANG = self.SpanishLocalizer.HTML_LANG
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
                    # TODO: Authenticate user. (Valid session exists)
                    return check_resp

            form = request.form
            username = form['username']
            password = form['password']
            auth = self.Database.authenticate_user(username, password)

            if auth:
                if auth == [True, True]:
                    # TODO: User authenticated to a new session.
                    # Generate Session ID and redirect
                    session_id = self.Database.create_session(username)

                    # Create response with Session ID cookie & user
                    response = make_response("<h1>Authenticated!</h1>")
                    response.set_cookie('User', username)
                    response.set_cookie('SessionID', str(session_id))
                    return response
                else:
                    # TODO: User was not authenticated.
                    return redirect(url_for("root"))
            else:
                # TODO: User account is not activated. (Disabled)
                return "<h1>Sorry, your account is disabled.</h1>"

        # HTTP Code 404 Page
        @self.Flask.errorhandler(404)
        def http_not_found(err_msg):
            """Return HTTP 404 not found page."""
            return self.EnglishLocalizer.localize_html(f"{self.HTTP_ERR}404.html")

        # Serve Static Files
        @self.Flask.route("/<path:path>", methods=["GET"])
        def static_files(path):
            """Send static content such as css and images."""
            return send_from_directory(self.ROOT_DIR, path)

        # Spanish Localizer
        @self.Flask.route("/es/<path:path>", methods=["GET"])
        def es(path):
            """
            Return site translated in Spanish.
            If a page is requested, save current language in cookie.
            """
            language = self.SpanishLocalizer.HTML_LANG

            if ".html" in path:
                localized_html = self.SpanishLocalizer.localize_html(path)
                response = make_response(localized_html)
                response.set_cookie('language', language)
                return response

            return redirect(url_for("static_files", path=path))

        # English Localizer
        @self.Flask.route("/en/<path:path>", methods=["GET"])
        def en(path):
            """
            Return site translated in English.
            If a page is requested, save current language in cookie.
            """
            language = self.EnglishLocalizer.HTML_LANG

            if ".html" in path:
                localized_html = self.EnglishLocalizer.localize_html(path)
                response = make_response(localized_html)
                response.set_cookie('language', language)
                return response

            return redirect(url_for("static_files", path=path))

        # Website Root
        @self.Flask.route("/", methods=["GET"])
        def root():
            """
            Website root, redirect to session language.
            If the client has no language cookie set, use default.
            """
            session_lang = request.cookies.get('language')

            if session_lang:
                return redirect(url_for(session_lang, path=self.INDEX_PAGE))
            else:
                return redirect(url_for(self.DEFAULT_LANG, path=self.INDEX_PAGE))

    def check_session_cookie(self, req: Request):
        """
        Check if user has a Session ID cookie using request given.
        Returns an array [response, status].
        """
        session_id = req.cookies.get('SessionID')

        if session_id is not None:
            username = req.cookies.get('User')
            # If there is no Username cookie, clear SID.
            if username is None:
                response = make_response("<h1>Missing Cookie; Please try again.</h1>")
                response.delete_cookie('SessionID')
                return [response, False]

            valid = self.Database.validate_session(username, session_id)
            if valid:
                response = make_response("<h1>Authenticated using existing session!</h1>")
                return [response, True]
            else:
                # Session is invalid, clear the user's cookie.
                response = make_response("<h1>Your session is no longer valid, retry.</h1>")
                response.delete_cookie('SessionID')
                return [response, False]
        # Return None if no Session ID cookie was found.
        return None

    def notify(self, string):
        print(f"[{self.__class__.__name__}]: {string}")

    def launch(self):
        """Starts the Flask web server with host/port."""
        if __name__ == "__main__":
            self.Flask.run(host=self.HOST, port=self.PORT)


# Launch the flask web server
WebApp = FlaskWebApp()
WebApp.launch()
