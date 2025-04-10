"""
Considere o sistema com realimentação unitária mostrado na Figura P9.1, onde:

            G(s) = K / [s(s + 3)(s + 6)]

a. Projete um controlador PI que elimine o erro de regime para uma entrada tipo rampa,
para qualquer valor de K que mantenha o sistema estável.

Solução:
- O sistema precisa ser do tipo 2 para erro nulo com entrada rampa.
- Um controlador PI adiciona um integrador ao sistema, tornando-o tipo 2.
"""

import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import *
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.

# Definindo os parâmetros
K = 100
zeros = []             # Nenhum zero
polos = [0, -3, -6]     # Polos do sistema

# Criando a função de transferência usando zpk
G = zpk(zeros, polos, K)

print("\nFunção de Transferência:")
print(G)

# ========================
# 2. Controle PI
# ========================

# Numerador e denominador do controlador PID
# Gc(s) = (Kd*s^2 + Kp*s + Ki) / s
Gc_z = [-0.01]             # Nenhum zero
Gc_p = [0]     # Polos do sistema
Gc_K = 1
# Criando a função de transferência usando zpk
Gc = zpk(Gc_z, Gc_p, Gc_K)

print("\nFunção de Transferência do Controlador PI:")
print(Gc)

# Sistema em malha fechada com realimentação unitária
Gmf = feedback(Gc * G, 1)

print("\nFunção do sistema em Malha Fechada:")
print(Gmf)

# Vetor de tempo para simulação
t = np.linspace(0, 15, 10000)

# Definindo a entrada rampa (rampa = t)
rampa = t

# Resposta ao degrau da malha fechada
y_out, t_out, x_out = lsim(Gmf, U=rampa, T=t)

# Gráfico do lugar das raízes
plt.figure(1)
rlocus(G)
plt.title("Lugar das Raízes de G(s)")
plt.grid(True)
plt.tight_layout()

# Gráfico do lugar das raízes
plt.figure(2)
rlocus(G*Gc)
plt.title("Lugar das Raízes de G(s)")
plt.grid(True)
plt.tight_layout()

# Plotando a resposta
plt.figure(3)
plt.plot(t_out, y_out, label='Saída do sistema')
plt.plot(t, rampa, 'r--', label='Entrada rampa')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.title('Resposta do Sistema à Entrada Rampa')
plt.grid(True)
plt.legend()
plt.show()