# Author : Killian O'Connor
# Date: 10/10/2026
# Description : Create the circuits that multiply by a^(2^k) mod 15 

from qiskit import QuantumCircuit

VALID_A = [2, 4, 7, 8, 11, 13]   # the a values coprime to 15


"""
amod15:
builds a 4-qubit circuit that multiplies the number stored in the qubits by a^power mod 15, using bit shuffling
"""
def amod15(a, power=1):
    U = QuantumCircuit(4, name=f"{a}^{power} mod 15") # creates an empty quantum circuit with 4 qubits
    for i in range(power):
        if a in (2, 13):                 
            U.swap(2, 3); U.swap(1, 2); U.swap(0, 1)
        if a in (7, 8):                  
            U.swap(0, 1); U.swap(1, 2); U.swap(2, 3)
        if a in (4, 11):                 
            U.swap(1, 3); U.swap(0, 2)
        if a in (7, 11, 13):             
            for q in range(4):
                U.x(q)
    return U


"""
cmod15:
takes the multiplication circuit from amod15 and turns it into a controlled  
"""
def c_amod15(a, power=1):
    gate = amod15(a, power).to_gate()
    gate.name = f"{a}^{power} mod 15"
    return gate.control()