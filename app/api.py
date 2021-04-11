from flask import send_file, request

from app import app
from qiskit_backend.music_generator import test_qiskit, generate_wav

@app.route("/api/test")
def test():
    return test_qiskit()

@app.route("/api/generate", methods=["POST"])
def generate():
    generate_wav(request.form['sample_text'])
    return send_file("/tmp/output.wav", as_attachment=True)