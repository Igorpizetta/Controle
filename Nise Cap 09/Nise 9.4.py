
import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import *
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.

# ------------------------------------------------------------------
# 1. Especificação: Queremos que K_v = 4 para entrada rampa.
#    Para a planta:
#       G(s) = K/(s(s+3)(s+7))
#    Temos: K_v = lim[s->0] s*G(s) = K/(3*7) = K/21.
#    Logo, para ter K_v = 4, precisamos de:
#         K = 4 * 21 = 84.
# ------------------------------------------------------------------
Kv_desejada = 4
K_desejada_inicial = Kv_desejada * 21
print("K desejado para ter K_v = 4 (sem compensação) =", K_desejada_inicial)

# ------------------------------------------------------------------
# 2. Definindo a planta com o ganho calculado:
#       G(s) = 84/(s(s+3)(s+7))
# ------------------------------------------------------------------
s = tf('s')
G = K_desejada_inicial / (s*(s+3)*(s+7))
print("\nFunção de transferência da planta G(s):")
print(G)

# Calculando o K_v da planta:
Kv_calculado = dcgain(s * G)
print("\nK_v calculado com K =", K_desejada_inicial, "é", Kv_calculado)

# ------------------------------------------------------------------
# 3. Projeto do compensador em atraso (lag network)
#    Usamos a forma: C(s) = (s + z) / (s + p) com z < p.
#    Valores típicos:
#       z = 0.1 e p = 0.01.
# ------------------------------------------------------------------
z = 0.1
p = 0.01
Lag = (s + z) / (s + p)
print("\nCompensador em atraso (lag network):")
print(Lag)

# A função de transferência em malha aberta com compensador é:
L = Lag * G

# ------------------------------------------------------------------
# 4. Fechamento da malha (realimentação unitária)
# ------------------------------------------------------------------
# Sistema SEM compensador:
T_sem_comp = feedback(G, 1)
# Sistema COM compensador:
T_com_comp = feedback(L, 1)

print("\nSistema em malha fechada SEM compensador:")
print(T_sem_comp)

print("\nSistema em malha fechada COM compensador:")
print(T_com_comp)

# ------------------------------------------------------------------
# 5. Simulação da resposta à entrada rampa
# ------------------------------------------------------------------
t = np.linspace(0, 10, 1000)  # intervalo de tempo
u = t                       # entrada rampa: u(t) = t

# Resposta do sistema sem compensador:
y_sem, t_sem, _ = lsim(T_sem_comp, U=u, T=t)
# Resposta do sistema com compensador:
y_com, t_com, _ = lsim(T_com_comp, U=u, T=t)

plt.figure(figsize=(10, 6))
plt.plot(t, u, 'k--', label="Entrada rampa")
plt.plot(t_sem, y_sem, 'b', label="Saída sem compensador")
plt.plot(t_com, y_com, 'g', label="Saída com compensador")
plt.xlabel("Tempo (s)")
plt.ylabel("Saída")
plt.title("Resposta à Entrada Rampa (Malha Fechada)")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------------------------------------------
# 6. Plotando o Lugar das Raízes (Root Locus)
# ------------------------------------------------------------------

# Lugar das raízes para o sistema sem compensador:
plt.figure(figsize=(10, 6))
rlocus(G)
plt.title("Lugar das Raízes - Sistema sem Compensador")

# Lugar das raízes para o sistema com compensador:
plt.figure(figsize=(10, 6))
rlocus(L)
plt.title("Lugar das Raízes - Sistema com Compensador")

plt.show()