from flask import render_template
from datetime import datetime

# Languages Support
# "/es" - Spanish
# "/en" - English


class Localizer:

    def __init__(self):
        self.DEFAULT = "es"
        self.LANG = {
            "es": {
                "HTML_LANG": "es",
                "PAGE_TITLE": "Inicio de sesión",
                "LOGIN_HEADER": "Iniciar Sesión",
                "USERNAME": "Nombre de usuario",
                "PASSWORD": "Contraseña",
                "LOGIN": "Iniciar Sesión",
                "SELECT_LANG": "Selecciona un idioma",
                "SPANISH": "Español",
                "ENGLISH": "Inglés"
            },
            "en": {
                "HTML_LANG": "en",
                "PAGE_TITLE": "Login to your account",
                "LOGIN_HEADER": "Begin Session",
                "USERNAME": "Enter username",
                "PASSWORD": "Enter password",
                "LOGIN": "Login to session",
                "SELECT_LANG": "Select a language",
                "SPANISH": "Spanish",
                "ENGLISH": "English"
            }
        }

    def localize_html(self, html, language):
        return render_template(
            html, Localizer=self, lang=language, date=datetime.now())
