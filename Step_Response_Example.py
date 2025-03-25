# Importação das bibliotecas necessárias
import numpy as np                      # Biblioteca para operações numéricas e vetores
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *            # Funções estilo MATLAB para controle
from math import *                      # Funções matemáticas

# ========================
# 1. Definição do Sistema em Malha Aberta
# ========================

# Numerador e denominador da função de transferência G(s)
# Neste exemplo: G(s) = 1 / ((s+1)(s+2)(s+3))
num = [1]
den = np.poly([-1, -2, -3])  # Converte os polos em um polinômio do denominador
G = tf(num, den)             # Cria a função de transferência

# Impressão da função de transferência
print("Sistema em malha aberta G(s):")
print(G)

# ========================
# 2. Fechando a Malha com Controle Proporcional (K)
# ========================

# Vetor de tempo para simulação
T = np.linspace(0, 20, 10000)

# Definição do ganho proporcional
K = 200  # Pode ser alterado para estudar o efeito de diferentes ganhos

# Controlador proporcional (Gc = K)
Gc = K

# Sistema em malha fechada com realimentação unitária: Gmf = (K*G)/(1 + K*G)
Gmf = feedback(Gc * G, 1)

# Resposta ao degrau da malha fechada
T_closed, yout_closed = step(Gmf, T)

# Gráfico da resposta em malha fechada
plt.figure(1)
plt.plot(yout_closed,T_closed, label=f'K = {K}')
plt.title("Resposta ao Degrau - Malha Fechada")
plt.grid(True)
plt.xlabel("Tempo (s)")
plt.ylabel("Saída")
plt.legend()
plt.tight_layout()