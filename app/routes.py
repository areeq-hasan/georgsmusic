from app import app

from flask import render_template

@app.route("/test/<name>")
def test(name):
    return render_template("index.html", name=name)