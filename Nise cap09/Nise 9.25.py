import os
import numpy as np
from sympy import *
from scipy.signal import TransferFunction
import matplotlib.pyplot as plt         # Biblioteca para gráficos
from control.matlab import *  # MATLAB-like functions
from math import *
from utils import *
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.

# Step 1: Given data
Tp = 1.122
zeta = 0.707

# Calculate Imaginary part (wd) and Real part (sigma)
wd = np.pi / Tp
sigma = wd / tan(acos(zeta))

print("Step 1 - Desired pole location calculations:")
print(f"wd (imaginary) = {wd:.2f} rad/s")
print(f"sigma (real) = {sigma:.2f}")

# Desired pole location
s_desired = complex(-sigma, wd)
print(f"Desired closed-loop pole: {s_desired:.2f}")

# Step 2: Original transfer function and PI compensator
# Original system
G = tf([1], [1, 4, 3])

# Lugar das raízes para o sistema sem compensador:
plt.figure(figsize=(10, 6))
rlocus(G)
plt.title("Lugar das Raízes - Sistema sem Compensador")

# PI compensator from solution provided
G_PI = tf([1, 0.1], [1, 0])
print("\nStep 2 - Original and PI Compensator:")
print(f"G(s) = {G}")
print(f"PI compensator Gc_PI(s) = {G_PI}")

plt.figure(figsize=(10, 6))
rlocus(G*G_PI)
plt.title("Lugar das Raízes - Sistema sem Compensador")

# Step 3: Geometry calculation for derivative compensator zero (Zc)
# Given directly by solution geometry:
Zc = 7.71
K = 1.683

print("\nStep 3 - Derivative compensator zero location:")
print(f"Zc = {Zc}")

# Step 4: Final PID controller
# PID compensator:
Gc_PID = tf(np.polymul([1, 0.1], [1, Zc]), [1, 0])
print("\nStep 4 - Final PID compensator:")
print(f"PID compensator Gc(s) = {Gc_PID}")

# Final Open Loop transfer function with compensator
OLTF = K*Gc_PID * G
print("\nOpen Loop Transfer Function with PID compensator:")
print(OLTF)

CLTF = feedback(OLTF, 1)
print("\nClosed Loop Transfer Function with PID compensator:")
print(CLTF)

plt.figure(figsize=(10, 6))
rlocus(OLTF)
plt.title("Lugar das Raízes - Sistema Compensado")


# PARTE 3: Resposta ao degrau

t = np.linspace(0, 5, 1000)
y1, _ = step(G, t)
y2, _ = step(CLTF, t)

plt.figure(figsize=(10, 6))
plt.plot(t, y1, label='Original (sem compensação)')
plt.plot(t, y2, label='Compensado (PID)', linestyle='--')
plt.title('Resposta ao Degrau')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.grid(True)
plt.legend()
plt.show()



# Checking angles visually (Optional)
plt.figure()
plt.title('Pole-Zero Map for PID compensated system')
plt.axvline(-sigma, color='grey', linestyle='--')
plt.plot(-1, 0, 'rx', label='System Pole (-1)')
plt.plot(-3, 0, 'rx', label='System Pole (-3)')
plt.plot(0, 0, 'ro', label='Integrator Pole (0)')
plt.plot(-0.1, 0, 'bo', label='PI Zero (-0.1)')
plt.plot(-Zc, 0, 'bo', label=f'Derivative Zero (-{Zc})')
plt.plot(-sigma, wd, 'g*', markersize=12, label='Desired Pole')
plt.grid()
plt.xlabel('Real Axis')
plt.ylabel('Imaginary Axis')
plt.legend()

