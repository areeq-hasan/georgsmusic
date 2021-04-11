from app import app

from flask import render_template

from app.api import test_qiskit

@app.route("/")
def index(): return "georgsmusic"