from flask import Flask, render_template, send_from_directory
from flask import redirect, url_for
from webserver.Localizer import Localizer

_ROOT_DIR = "www"
webapp = Flask(__name__, template_folder=_ROOT_DIR)
Language = Localizer()  # Init the localizer class


@webapp.route("/resources/<path:path>")
def resources(path):
    return send_from_directory("www/resources", path)


@webapp.route("/es")
def es():
    return Localizer.localize_html(Language, "login.html", "es")


@webapp.route("/en")
def en():
    return Localizer.localize_html(Language, "login.html", "en")


@webapp.route("/")
def root():
    return redirect(url_for(Language.DEFAULT))


if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

