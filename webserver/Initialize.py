from flask import Flask, render_template

webapp = Flask(__name__)

@webapp.route("/")
def root():
    return render_template("www/login.html")

if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=80)

