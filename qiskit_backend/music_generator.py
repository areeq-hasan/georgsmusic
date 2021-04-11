# import numpy
import numpy as np

# importing qiskit
import qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.compiler import schedule, transpile

from qiskit.test.mock.backends.almaden import FakeAlmaden
backend = FakeAlmaden()

from qiskit.pulse.instructions.play import Play

# importing audio utils
from scipy.io.wavfile import write

# CONSTANTS
sampling_rate = 44100 * 3

def test_qiskit(): return qiskit.__qiskit_version__

def char_to_qc(char_str):
  char_bin = '0'+' '.join(format(ord(x), 'b') for x in char_str)

  char = QuantumRegister(8, name='char')
  output = QuantumRegister(1, name='output')
  meas = ClassicalRegister(8, name='meas')
  char_qc = QuantumCircuit(char, output, meas)

  char_qc.h(char[:])
  char_qc.h(output)
  char_qc.z(output)
  char_qc.barrier()

  for i, bit in enumerate(char_bin):
    if int(bit): char_qc.cx(char[i], output[0])
  char_qc.barrier()

  char_qc.h(char[:])
  char_qc.barrier()

  return char_qc.reverse_bits()

def pulse_schedule_to_complex_waveform(pulse_schedule):
    instructions = pulse_schedule.instructions
    waveform = [instruction[1].pulse.samples for instruction in instructions if type(instruction[1]) == Play]
    waveform = np.concatenate(waveform).ravel()
    return waveform

def complex_waveform_to_amplitude_waveform(waveform): return np.asarray([np.absolute(z) for z in waveform])

def get_audio_waveform(string):
    words = string.split(" ")
    audio_waveform = np.array([])
    for word in words:
        word_waveforms = [ pulse_schedule_to_complex_waveform(schedule(transpile(char_to_qc(char), backend), backend)) for char in word ]
        waveform_size = max([waveform.size for waveform in word_waveforms])
        word_waveform = np.zeros(waveform_size)
        for waveform in word_waveforms: 
            word_waveform = word_waveform + np.pad(waveform, (0, waveform_size - waveform.size), mode='constant')
        audio_waveform = np.concatenate((audio_waveform, complex_waveform_to_amplitude_waveform(waveform))) # concatenate word_waveform to end of audio_waveform
    return audio_waveform

def generate_wav(string):
    data = get_audio_waveform(string)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write('/tmp/output.wav', sampling_rate, scaled)