from flask import render_template, Request
from datetime import datetime


class Localizer:
    """
    This class renders HTML templates along with a
    language dictionary to translate phrases in the page.
    Also passes request information to the HTML template.
    """
    def __init__(self):
        self.SPANISH = "es"
        self.ENGLISH = "en"
        self.DEFAULT = self.SPANISH

        self.LANG = {
            f"{self.SPANISH}": {
                "404": "No se encontró el archivo",
                "SPANISH": "Español",
                "ENGLISH": "Inglés",
                "LOGIN_TITLE": "Inicio de sesión",
                "LOGIN_HEADER": "Iniciar Sesión",
                "USERNAME": "Nombre de usuario",
                "PASSWORD": "Contraseña",
                "LOGIN": "Iniciar Sesión",
                "SELECT_LANG": "Selecciona un idioma",
                "PANEL_TITLE": "Panel de usuario",
                "WELCOME": "Hola"
            },
            f"{self.ENGLISH}": {
                "404": "File not found",
                "SPANISH": "Spanish",
                "ENGLISH": "English",
                "LOGIN_TITLE": "Login to your account",
                "LOGIN_HEADER": "New Session",
                "USERNAME": "Enter username",
                "PASSWORD": "Enter password",
                "LOGIN": "Login to session",
                "SELECT_LANG": "Select your language",
                "PANEL_TITLE": "User Panel",
                "WELCOME": "Welcome"
            }
        }

    def localize_html(self, lang: str, html: str, request: Request):
        """
        Localize HTML template to language specified.
        Passes the Localizer dictionary and request information.
        """
        return render_template(html, Localizer=self, HTML_LANG=lang,
                               Lang=self.LANG[lang], req=request)

    def get_copyright_year(self):
        """Returns the current year for copyright."""
        return datetime.now().year
