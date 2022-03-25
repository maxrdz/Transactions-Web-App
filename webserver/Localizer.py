from flask import render_template
from datetime import datetime


class Localizer:
    """
    The Localizer class initializes the localizer base which includes
    the `localize_html()` method for translating HTML templates.
    Every language localizer inherits and extends this class.
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
                "PAGE_TITLE": "Inicio de sesión",
                "LOGIN_HEADER": "Iniciar Sesión",
                "USERNAME": "Nombre de usuario",
                "PASSWORD": "Contraseña",
                "LOGIN": "Iniciar Sesión",
                "SELECT_LANG": "Selecciona un idioma",
                "WELCOME": "Hola"
            },
            f"{self.ENGLISH}": {
                "404": "File not found",
                "SPANISH": "Spanish",
                "ENGLISH": "English",
                "PAGE_TITLE": "Login to your account",
                "LOGIN_HEADER": "New Session",
                "USERNAME": "Enter username",
                "PASSWORD": "Enter password",
                "LOGIN": "Login to session",
                "SELECT_LANG": "Select your language",
                "WELCOME": "Welcome"
            }
        }

    def localize_html(self, lang, html):
        return render_template(html, Localizer=self, HTML_LANG=lang,
                               Lang=self.LANG[lang], path=html)

    def get_copyright_year(self):
        return datetime.now().year
