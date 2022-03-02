from flask import Flask, send_from_directory
from flask import redirect, url_for
from webserver.Localizer import EnglishLocalizer
from webserver.Localizer import SpanishLocalizer

_ROOT_DIR = "www"
_INDEX_PAGE = "login.html"
_HTTP_ERR = "http_error/"
webapp = Flask(__name__, template_folder=_ROOT_DIR)
SpanishLocalizer = SpanishLocalizer()
EnglishLocalizer = EnglishLocalizer()
_DEFAULT_LANG = SpanishLocalizer.HTML_LANG


@webapp.errorhandler(404)
def http_not_found(err_msg):
    """Return HTTP 404 not found page."""
    return EnglishLocalizer.localize_html(f"{_HTTP_ERR}404.html")


@webapp.route("/<path:path>", methods=["GET"])
def static_files(path):
    """Send static content such as css and images."""
    return send_from_directory(_ROOT_DIR, path)


@webapp.route("/es/<path:path>", methods=["GET"])
def es(path):
    """Return site translated in Spanish."""
    if ".html" in path:
        return SpanishLocalizer.localize_html(path)
    return redirect(url_for("static_files", path=path))


@webapp.route("/en/<path:path>", methods=["GET"])
def en(path):
    """Return site translated in English."""
    if ".html" in path:
        return EnglishLocalizer.localize_html(path)
    return redirect(url_for("static_files", path=path))


@webapp.route("/", methods=["GET"])
def root():
    """Website root, redirect to default language."""
    return redirect(url_for(_DEFAULT_LANG, path=_INDEX_PAGE))


# Launch the flask web server
if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

