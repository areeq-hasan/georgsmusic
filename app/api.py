from flask import send_file

from app import app
from qiskit_backend.music_generator import test_qiskit, generate_wav

@app.route("/api/test")
def test():
    return test_qiskit()

@app.route("/api/generate/<string>")
def generate(string):
    generate_wav(string)
    return send_file("/tmp/output.wav", as_attachment=True)