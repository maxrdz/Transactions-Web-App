from flask import Flask, render_template

webapp = Flask(__name__, template_folder="www")

@webapp.route("/")
def root():
    return render_template("login.html", var="test var")

if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

