# secord.py - demonstrate some standard MATLAB commands
# RMM, 25 May 09
# Funções úteis
# e_step = 1/(1+Kp)
# sigma_d = -zeta*wn
# w_d = -wn*sqrt(1-zeta^2)
# wn = 4/(zeta*Ts)
# gain = dcgain(z,p,K)

import os
from matplotlib.pyplot import *   # MATLAB plotting functions
from control.matlab import *  # MATLAB-like functions
from math import *

OS = 15
zeta = -log(OS/100)/sqrt(pow(pi,2) +pow(log(OS/100),2))
zeta_dg = acos(zeta)*180/pi

# Numerador e denominador da função de transferência G(s)
# Neste exemplo: G(s) = 1 / ((s+1)(s+2)(s+3))
num = [1]
den = np.poly([-1, -2, -3])  # Converte os polos em um polinômio do denominador
sys = tf(num, den)             # Cria a função de transferência

print(sys)

figure(1)

# Generate the root locus plot within the created figure
rlocus(sys)
tight_layout()
show()

# Calcula o root locus sem plotar
rlist, klist = rlocus(sys, kvect=np.linspace(0, 100, 10000), plot=False)

# Loop para detectar a instabilidade (primeira parte real positiva)
for i, polos in enumerate(rlist):
    if any(np.real(p) > 0 for p in polos):
        print(f"Sistema fica instável para K ≈ {klist[i]:.4f}")
        break