import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import *
from utils import *
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.

# ----------------------------------------
# SISTEMA ORIGINAL: G(s) = K(s+6)/((s+2)(s+3)(s+5))
# ----------------------------------------

zeros = [-6]
polos = [-2, -3, -5]
K = 4.6045  # ganho obtido analiticamente
G = zpk(zeros, polos, K)
G_cl = feedback(G, 1)

# ----------------------------------------
# PARTE 1: Análise do sistema original
# ----------------------------------------

# Polos dominantes do sistema original
# Buscando pela linha de zeta = 0.707, encontramos o valor do polo (ou ponto) que possui a relação angular de 180 graus
zeta = 0.707
sigma, wd, K_corrigido, polo = encontrar_polos_por_zeta(G, zeta)

wn = np.sqrt(sigma**2 + wd**2)
Ts = 4 / (zeta * wn)
Tp = np.pi / wd
OS = np.exp((-zeta * np.pi) / np.sqrt(1 - zeta**2)) * 100

print(f"Sistema Original:")
print(f"  wn = {wn:.3f}, Ts = {Ts:.3f}s, Tp = {Tp:.3f}s, Overshoot = {OS:.2f}%")

# ----------------------------------------
# PARTE 2: Projeto do PD com zero manual
# ----------------------------------------

# Novo wn para reduzir Ts pela metade
wn_novo = 2 * wn
sigma_novo = -zeta * wn_novo
wd_novo = wn_novo * np.sqrt(1 - zeta**2)
polo_desejado = sigma_novo + 1j * wd_novo
print(f"\nPolo desejado: {polo_desejado:.3f}")

# Valor do zero do PD segundo a geometria (não calculado, apenas usado)
zc = 7.21
print(f"Zero do PD (manual): zc = {zc}")

# Controlador PD: D(s) = s + zc
D = zpk([-zc], [], 1)
G_PD = D * G
G_cl_comp = feedback(G_PD, 1)

# ------------------------------------------------------------------
# 3.5. Plotando o Lugar das Raízes (Root Locus)
# ------------------------------------------------------------------

# Lugar das raízes para o sistema sem compensador:
plt.figure(figsize=(10, 6))
rlocus(G)
plt.title("Lugar das Raízes - Sistema sem Compensador")

# Lugar das raízes para o sistema com compensador:
plt.figure(figsize=(10, 6))
rlocus(G_PD)
plt.title("Lugar das Raízes - Sistema com Compensador")

plt.show()

# ----------------------------------------
# PARTE 4: Gráfico de polos, zeros e geometria
# ----------------------------------------

plt.figure(figsize=(8, 6))

# Polos e zeros do sistema original
for p in polos:
    plt.plot(np.real(p), np.imag(p), 'rx', markersize=10)
for z in zeros:
    plt.plot(np.real(z), np.imag(z), 'go', markersize=8)

# Polo desejado
x0, y0 = np.real(polo_desejado), np.imag(polo_desejado)
plt.plot(x0, y0, 'b*', markersize=12, label='Polo desejado')

# Zero do PD
plt.plot(-zc, 0, 'mo', markersize=10, label='Zero PD (manual)')

# Vetor do zero ao polo desejado
plt.plot([x0, -zc], [y0, 0], 'm--', label='Geometria do PD')

# Linha vertical do polo desejado
plt.plot([x0, x0], [0, y0], 'k:', label='Linha vertical')

# Ângulo no gráfico (aproximado como arco)
angulo_deg = 61
raio = 1.5
angulo_rad = np.radians(angulo_deg)
theta = np.linspace(0, angulo_rad, 100)


# Eixos e estilos
plt.axhline(0, color='gray', linestyle=':')
plt.axvline(0, color='gray', linestyle=':')
plt.title("Plano s: Polos, Zeros e Geometria do Compensador PD")
plt.xlabel('Re')
plt.ylabel('Im')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()

# ----------------------------------------
# PARTE 3: Resposta ao degrau
# ----------------------------------------

t = np.linspace(0, 5, 1000)
y1, _ = step(G_cl, t)
y2, _ = step(G_cl_comp, t)

plt.figure(figsize=(10, 6))
plt.plot(t, y1, label='Original (sem compensação)')
plt.plot(t, y2, label='Compensado (PD)', linestyle='--')
plt.title('Resposta ao Degrau')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.grid(True)
plt.legend()
plt.show()


# ----------------------------------------
# PARTE 5: Mostrar polos
# ----------------------------------------

print("Polos do sistema original:", np.round(pole(G_cl), 3))
print("Polos do sistema compensado:", np.round(pole(G_cl_comp), 3))