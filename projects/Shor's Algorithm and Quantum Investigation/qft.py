# Author : Killian O'Connor
# Date : 08/10/2026
# Description : Builds the inverse Quantum Fourier Transform that turns the repeating pattern into measurable peaks

from math import pi
from qiskit import QuantumCircuit

"""
qft:
it converts a number stored in the qubits into a pattern of phases, and the inverse converts phases back into a number
    """
def qft(n, inverse=False, do_swaps=True):
    qc = QuantumCircuit(n, name="QFT†" if inverse else "QFT")
    
    for j in reversed(range(n)):
        qc.h(j)
        for k in range(j):
            qc.cp(pi / 2 ** (j - k), k, j)

    if do_swaps:
        for i in range(n // 2):
            qc.swap(i, n - 1 - i)

    return qc.inverse() if inverse else qc # return inverse if called or qc by default