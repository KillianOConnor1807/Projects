# Author : Killian O'Connor
# Date : 10/10/2026
# Description : assembles the circuit, runs the simulation, interprets the output and retries until it gets factors.

import math
import random
from fractions import Fraction
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from qft import qft
from modexp import c_amod15, VALID_A

N = 15
N_COUNT = 8                                   # counting qubits
TARGET = list(range(N_COUNT, N_COUNT + 4))    # the 4 qubits holding the number being multiplied


def build_circuit(a):
    # builds the circuit
    qc = QuantumCircuit(N_COUNT + 4, N_COUNT)

    # put every counting qubit into superposition
    for i in range(N_COUNT):
        qc.h(i)

    # set the target register to the number 1
    qc.x(TARGET[0])

    # counting qubit j controls multiplication by a^(2^j) mod N
    for j in range(N_COUNT):
        m = pow(a, 2 ** j, N)
        if m != 1:                      # multiplying by 1 does nothing
            qc.append(c_amod15(m), [j] + TARGET)

    # turn the phase pattern into measurable peaks, then measure
    qc.compose(qft(N_COUNT, inverse=True), qubits=range(N_COUNT), inplace=True)
    qc.measure(range(N_COUNT), range(N_COUNT))
    return qc


def find_period(a):
    # runs the circuit and works out the period r from the measurements.
    sim = AerSimulator()
    qc = transpile(build_circuit(a), sim)
    counts = sim.run(qc, shots=1024).result().get_counts()

    # show what was measured
    print("Measurements (decimal : count):")
    for bits in counts:
        print(int(bits, 2), ":", counts[bits])

    # turn each measurement into a candidate period
    for bits in counts:
        measured = int(bits, 2)
        r = Fraction(measured, 2 ** N_COUNT).limit_denominator(N).denominator
        print("measured", measured, "-> candidate r =", r)
        if pow(a, r, N) == 1:           # only accept a genuine period
            return r
    return None


def factors_from_period(a, r):
    # works out the factors of N from a and r, or returns None.
    if r % 2 == 1:
        return None                     # odd period can't be halfed 
    y = pow(a, r // 2, N)
    if y == N - 1:
        return None
    for f in (math.gcd(y - 1, N), math.gcd(y + 1, N)):
        if 1 < f < N:
            return f, N // f
    return None


def shor():
    print("*****************************************")
    print(f"Shor's algorithm : N = {N}")
    for attempt in range(1, 11):
        a = random.choice(VALID_A)
        print(f"\nAttempt {attempt}: a = {a}")

        r = find_period(a)
        if r is None:
            print("\nNo valid period found\n")
            continue

        print(f"Period r = {r}")
        result = factors_from_period(a, r)
        if result is not None:
            print(f"Result: {N} = {result[0]} x {result[1]}")
            return

    print("Error")


shor()