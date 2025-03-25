import numpy as np
import matplotlib.pyplot as plt
from control.matlab import *

# ========================
# Definição da Função de Transferência G(s)
# ========================

# G(s) = 1 / ((s+1)(s+2)(s+3))
num = [1]
den = np.poly([-1, -2, -3])  # Cria o polinômio do denominador a partir dos polos
G = tf(num, den)

# Vetor de tempo para simulação
T = np.linspace(0, 10, 1000)

# Lista de ganhos que serão testados
ganhos = [1, 5, 7, 10, 20, 30]

# ========================
# Plotando as respostas para diferentes valores de K
# ========================

plt.figure()
for K in ganhos:
    Gc = K
    Gmf = feedback(Gc * G, 1)          # Fecha a malha com ganho K e realimentação unitária
    Tresp, yout = step(Gmf, T)         # Resposta ao degrau
    plt.plot(yout,Tresp, label=f'K = {K}')  # Plota a curva

# Configurações do gráfico
plt.title("Resposta ao Degrau - Vários Ganhos K")
plt.xlabel("Tempo (s)")
plt.ylabel("Saída")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()