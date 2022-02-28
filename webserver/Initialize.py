from flask import Flask, request, render_template, send_from_directory

_ROOT_DIR = "www"

webapp = Flask(__name__, template_folder=_ROOT_DIR)

@webapp.route("/")
def root():
    return render_template("login.html")

@webapp.route("/resources/<path:path>")
def resources(path):
    return send_from_directory("www/resources", path)

if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

