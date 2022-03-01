from flask import Flask, render_template, send_from_directory
from flask import redirect, url_for
from datetime import datetime
from webserver.Localizer import Localizer

_ROOT_DIR = "www"
webapp = Flask(__name__, template_folder=_ROOT_DIR)
Language = Localizer()  # Init the localizer class


def localize_html(lang):
    return render_template(
        "login.html", v1=Language.LANG[lang]["PAGE_TITLE"],
        v2=Language.LANG[lang]["LOGIN_HEADER"], v3=Language.LANG[lang]["USERNAME"],
        v4=Language.LANG[lang]["PASSWORD"], v5=Language.LANG[lang]["LOGIN"],
        v6=Language.LANG[lang]["SELECT_LANG"], v7=Language.LANG[lang]["SPANISH"],
        v8=Language.LANG[lang]["ENGLISH"], year=datetime.now().year)


@webapp.route("/resources/<path:path>")
def resources(path):
    return send_from_directory("www/resources", path)


@webapp.route("/es")
def spanish():
    return localize_html("SPANISH")


@webapp.route("/en")
def english():
    return localize_html("ENGLISH")


@webapp.route("/")
def root():
    return redirect(url_for(Language.DEFAULT))


if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

