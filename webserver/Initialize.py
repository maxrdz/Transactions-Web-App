from flask import Flask, send_from_directory, redirect, url_for, request
from webserver.Localizer import SpanishLocalizer, EnglishLocalizer
from webserver.Database import DatabaseManager


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
        self.SpanishLocalizer = SpanishLocalizer()
        self.EnglishLocalizer = EnglishLocalizer()
        self.DEFAULT_LANG = self.SpanishLocalizer.HTML_LANG
        self.Database = DatabaseManager()

        # User Authentication Query String
        @self.Flask.route("/auth/", methods=["GET"])
        def authentication_query():
            query_strings = request.args
            username = query_strings['username']
            password = query_strings['password']

            auth = self.Database.authenticate_user(username, password)
            return f"Authentication Status Received: {auth}"

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
            """Return site translated in Spanish."""
            if ".html" in path:
                return self.SpanishLocalizer.localize_html(path)
            return redirect(url_for("static_files", path=path))

        # English Localizer
        @self.Flask.route("/en/<path:path>", methods=["GET"])
        def en(path):
            """Return site translated in English."""
            if ".html" in path:
                return self.EnglishLocalizer.localize_html(path)
            return redirect(url_for("static_files", path=path))

        # Website Root
        @self.Flask.route("/", methods=["GET"])
        def root():
            """Website root, redirect to default language."""
            return redirect(url_for("es", path=self.INDEX_PAGE))

    def notify(self, string):
        print(f"[{self.__class__.__name__}]: {string}")

    def launch(self):
        """Starts the Flask web server with host/port."""
        if __name__ == "__main__":
            self.Flask.run(host=self.HOST, port=self.PORT)


# Launch the flask web server
WebApp = FlaskWebApp()
WebApp.launch()
