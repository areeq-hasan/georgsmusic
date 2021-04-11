from app import app
from flask import jsonify

# import numpy
import numpy as np

# importing qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.compiler import schedule

from qiskit.test.mock.backends.almaden import FakeAlmaden
backend = FakeAlmaden()

from qiskit.pulse.instructions.play import Play

def test_qiskit():
    return qiskit.__qiskit__version__