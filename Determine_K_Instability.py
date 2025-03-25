import numpy as np
import matplotlib.pyplot as plt
from control.matlab import *

# Numerador e denominador da função de transferência G(s)
# Neste exemplo: G(s) = 1 / ((s+1)(s+2)(s+3))
num = [1]
den = np.poly([-1, -2, -3])  # Converte os polos em um polinômio do denominador
sys = tf(num, den)             # Cria a função de transferência

# Gera o root locus com muitos pontos de ganho para alta resolução
kvec = np.linspace(0, 100, 10000)
rlist, klist = rlocus(sys, kvect=kvec, plot=False)

# Busca o ganho crítico onde a parte real de algum polo fica positiva
K_instavel = None
p_instaveis = None

for i, polos in enumerate(rlist):
    if any(np.real(p) > 0 for p in polos):
        K_instavel = klist[i]
        p_instaveis = polos
        break

# Exibe o resultado
if K_instavel:
    print(f"Sistema se torna instável para K ≈ {K_instavel:.4f}")
else:
    print("Sistema permanece estável para todos os valores de K no intervalo.")

# === Plot com marcação do ponto crítico ===
plt.figure()
rlocus(sys, kvect=kvec)
plt.axvline(0, color='gray', linestyle='--')  # eixo imaginário

# Destaca os polos instáveis
if p_instaveis is not None:
    for p in p_instaveis:
        if np.real(p) > 0:
            plt.plot(np.real(p), np.imag(p), 'rx', markersize=10, label=f'K ≈ {K_instavel:.2f}')
    plt.legend()

plt.title("Root Locus com ponto de instabilidade detectado")
plt.xlabel("Re(s)")
plt.ylabel("Im(s)")
