import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import pi, tan, atan, log
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.



zeros = []
polos = [-1,-5,-10]
K = 60  # ganho obtido analiticamente


G = zpk(zeros, polos, K)
G_cl = feedback(G, 1)

# Plotando o diagrama de Bode
mag, phase, omega = bode(G, dB=True, Hz=False, omega_limits=(0.01, 100), omega_num=1000)

# Configurações adicionais (opcional)
plt.suptitle("Diagrama de Bode", fontsize=14)
plt.show()