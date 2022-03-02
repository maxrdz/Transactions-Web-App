from flask import render_template
from datetime import datetime


class Localizer:
    """
    The Localizer class initializes the localizer base which includes
    the `localize_html()` method for translating HTML templates.
    Every language localizer inherits and extends this class.
    """
    def __init__(self):
        self.HTML_LANG = ""
        self.LANG = {
            "http_error/404.html": {
                "ERROR_MESSAGE": ""
            },
            "login.html": {
                "SPANISH": "",
                "ENGLISH": "",
                "PAGE_TITLE": "",
                "LOGIN_HEADER": "",
                "USERNAME": "",
                "PASSWORD": "",
                "LOGIN": "",
                "SELECT_LANG": ""
            }
        }

    def localize_html(self, html):
        return render_template(
            html, Localizer=self, Lang=self.LANG[html], path=html)

    def get_copyright_year(self):
        return datetime.now().year


class SpanishLocalizer(Localizer):

    def __init__(self):
        super().__init__()
        self.HTML_LANG = "es"
        # /http_error/404.html dictionary
        self.LANG["http_error/404.html"]["ERROR_MESSAGE"] = "Página no encontrada."
        # /login.html dictionary
        self.LANG["login.html"]["HTML_LANG"] = "es"
        self.LANG["login.html"]["SPANISH"] = "Español"
        self.LANG["login.html"]["ENGLISH"] = "Inglés"
        self.LANG["login.html"]["PAGE_TITLE"] = "Inicio de sesión"
        self.LANG["login.html"]["LOGIN_HEADER"] = "Iniciar Sesión"
        self.LANG["login.html"]["USERNAME"] = "Nombre de usuario"
        self.LANG["login.html"]["PASSWORD"] = "Contraseña"
        self.LANG["login.html"]["LOGIN"] = "Iniciar Sesión"
        self.LANG["login.html"]["SELECT_LANG"] = "Selecciona un idioma"


class EnglishLocalizer(Localizer):

    def __init__(self):
        super().__init__()
        self.HTML_LANG = "en"
        # /http_error/404.html dictionary
        self.LANG["http_error/404.html"]["ERROR_MESSAGE"] = "Not Found."
        # /login.html dictionary
        self.LANG["login.html"]["HTML_LANG"] = "en"
        self.LANG["login.html"]["SPANISH"] = "Spanish"
        self.LANG["login.html"]["ENGLISH"] = "English"
        self.LANG["login.html"]["PAGE_TITLE"] = "Login to your account"
        self.LANG["login.html"]["LOGIN_HEADER"] = "Begin Session"
        self.LANG["login.html"]["USERNAME"] = "Enter username"
        self.LANG["login.html"]["PASSWORD"] = "Enter password"
        self.LANG["login.html"]["LOGIN"] = "Login to session"
        self.LANG["login.html"]["SELECT_LANG"] = "Select a language"
