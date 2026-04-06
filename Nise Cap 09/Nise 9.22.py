import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import pi, tan, atan, log
from utils import *


# PARTE A: Definindo especificações de ultrapassagem de 30%
PO = 0.30
zeta = -np.log(PO) / np.sqrt(pi**2 + (np.log(PO))**2)  # Fator de amortecimento
theta_deg = np.arccos(zeta) * (180 / pi)

# Determinação do polo dominante no lugar das raízes
# Segundo a resolução, os polos são: -1.464 ± j3.818
sigma = 1.464
omega_d = 3.818
s1 = complex(-sigma, omega_d)

# K necessário para passar pela raiz dominante
mag = abs(s1 * (s1 + 5) * (s1 + 11))
K = 1 / mag

# Tempo de pico
Tp = pi / omega_d

# Ganho de velocidade Kv
Kv = K / (5 * 11)

# PARTE C: Compensador avanço-atraso
# Nova ultrapassagem: 15%, novo tempo de pico: Tp / 2
PO_new = 0.15
Tp_new = Tp / 2
zeta_new = -np.log(PO_new) / np.sqrt(pi**2 + (np.log(PO_new))**2)
omega_d_new = pi / Tp_new
omega_n_new = omega_d_new / np.sqrt(1 - zeta_new**2)

# Novo polo desejado
sigma_new = zeta_new * omega_n_new
wd_new = omega_n_new * np.sqrt(1 - zeta_new**2)
s_new = complex(-sigma_new, wd_new)

# Supondo zero do avanço em -5, encontra o polo do compensador
angle_required = 180 - 171.2
angle_rad = np.deg2rad(angle_required)
pc = wd_new / tan(angle_rad)

# Novo ganho compensado
K_lead = 4430
Kv_compensated = K_lead / (11 * pc)
Kv_required = Kv * 30
improvement = Kv_required / Kv_compensated

# G_lag = (s + z_lag) / (s + p_lag) com ganho de melhoria de 15.97
z_lag = 0.01597
p_lag = z_lag / improvement

# Resultados para exibição
import pandas as pd

data = {
    "Descrição": [
        "ζ (30% OS)", "θ (graus)", "K para OS=30%", "Tp (s)", "Kv não compensado",
        "ζ (15% OS)", "Tp desejado", "σ novo", "ω_d novo", "Polo Compensador (pc)",
        "Kv desejado", "Kv com avanço", "Melhoria necessária (lag)", "Zero do lag", "Polo do lag"
    ],
    "Valor": [
        zeta, theta_deg, K, Tp, Kv,
        zeta_new, Tp_new, sigma_new, wd_new, pc,
        Kv_required, Kv_compensated, improvement, z_lag, p_lag
    ]
}
