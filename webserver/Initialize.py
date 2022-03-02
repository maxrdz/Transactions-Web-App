from flask import Flask, render_template, send_from_directory
from flask import redirect, url_for
from webserver.Localizer import EnglishLocalizer
from webserver.Localizer import SpanishLocalizer

_ROOT_DIR = "www"
webapp = Flask(__name__, template_folder=_ROOT_DIR)
SpanishLocalizer = SpanishLocalizer()
EnglishLocalizer = EnglishLocalizer()


@webapp.route("/resources/<path:path>")
def resources(path):
    return send_from_directory("www/resources", path)


@webapp.route("/es")
def es():
    return SpanishLocalizer.localize_html("login.html")


@webapp.route("/en")
def en():
    return EnglishLocalizer.localize_html("login.html")


@webapp.route("/")
def root():
    return redirect(url_for(SpanishLocalizer.DEFAULT))


if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

