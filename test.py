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

# System
K = 1
p = [-5,-5,-5]
z = []
sys = zpk(z,p,K)

print(zeta)
print(zeta_dg)
print(sys)