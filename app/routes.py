from flask import render_template

from app import app

@app.route("/")
def index_route(): return render_template("index.html")

@app.route("/generate")
def generate_route(): return render_template("generate.html")

# UI
# add stream generator for wait period
# audio waveform embedded in site