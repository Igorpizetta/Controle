
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import *


OS = 0.1

zeta = -ln(OS) / sqrt(pi**2 + ln(OS)**2)
print(f"Zeta para overshoot de {OS*100:.1f}%: {zeta:.4f}")


# Definindo os parâmetros
K = 4.6045
zeros = [-6]             # Nenhum zero
polos = [ -2, -3, -5]     # Polos do sistema

# Criando a função de transferência usando zpk
G = zpk(zeros, polos, K)

print("\nSistema em malha aberta:")
print(G)

# Gráfico do lugar das raízes
plt.figure(1)
rlocus(G)
plt.title("Lugar das Raízes de G(s)")
plt.grid(True)
plt.tight_layout()


K = 0.1
zeros = [-7.21,-0.05]             # Nenhum zero
polos = [-0.01]     # Polos do sistema

# Criando a função de transferência usando zpk
Gc = zpk(zeros, polos, K)


# Gráfico do lugar das raízes
plt.figure(2)
rlocus(G*Gc)
plt.title("Lugar das Raízes de G(s)Gc(s)")
plt.grid(True)
plt.tight_layout()


# Criação do sistema em malha fechada

Gmf = feedback(G, 1)
Gmfc = feedback(Gc * G, 1)

print("\nSistema em malha fechada sem compensação:")
print(Gmf)

print("\nSistema em malha fechada com compensação:")
print(Gmfc)


stepinfo_Gmf = stepinfo(Gmf)
stepinfo_Gmfc = stepinfo(Gmfc)
print("\nInformações da resposta ao degrau - Sistema sem compensação:")
print(f"Tempo de subida: {stepinfo_Gmf} s")


# Plotar a resposta ao degrau
t = np.linspace(0, 60, 20000)
y1, _ = step(Gmf, t)
y2, _ = step(Gmfc, t)

plt.figure(figsize=(10, 6))
plt.plot(t, y1, label='Original (sem compensação)')
plt.plot(t, y2, label='Compensado')
plt.title('Resposta ao Degrau')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.grid(True)
plt.legend()

plt.show()