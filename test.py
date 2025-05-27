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
polos = [0, -5, -11]     # Polos do sistema

# Criando a função de transferência usando zpk
G = zpk(zeros, polos, K)

print("\nFunção de Transferência:")
print(G)

# Gráfico do lugar das raízes
plt.figure(1)
rlocus(G)
plt.title("Lugar das Raízes de G(s)")
plt.grid(True)
plt.tight_layout()

# Salvar primeiro
plt.savefig("rlocus.pdf", format='pdf')  # salvar antes de mostrar

plt.show()

