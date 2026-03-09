import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import control as ct

OS = 15.0
Ts = 0.7

def zeta_from_os(percent_os):
    os = percent_os / 100.0
    f = lambda z: np.exp(-z*np.pi/np.sqrt(1-z**2)) - os
    return brentq(f, 1e-6, 0.999999)

zeta = zeta_from_os(OS)
wn = 4 / (zeta * Ts)

sigma = zeta * wn
wd = wn * np.sqrt(1 - zeta**2)

p1 = -sigma + 1j*wd
p2 = -sigma - 1j*wd

G = ct.tf([wn**2], [1, 2*zeta*wn, wn**2])

print("Especificações:")
print(f"  %OS = {OS:.1f}%")
print(f"  Ts  = {Ts:.3f} s\n")

print("Parâmetros:")
print(f"  zeta = {zeta:.6f}")
print(f"  wn   = {wn:.6f} rad/s")

print("Polos:")
print(f"  s1 = {p1.real:.6f} + j{p1.imag:.6f}")
print(f"  s2 = {p2.real:.6f} - j{abs(p2.imag):.6f}")

print("Função de transferência:")
print(G)

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

ax1 = axes[0]
ct.rlocus(G, gains=np.linspace(0, 20, 600), ax=ax1)
ax1.plot([p1.real, p2.real], [p1.imag, p2.imag], 'rx', markersize=10, markeredgewidth=2, label='Polos desejados')

theta = np.linspace(0, 2*np.pi, 500)
ax1.plot(wn*np.cos(theta), wn*np.sin(theta), ':', linewidth=1, label=r'$\omega_n$')
ax1.plot([-sigma, -sigma], [-1.2*wd, 1.2*wd], '--', linewidth=1, label=r'$\sigma=\zeta\omega_n$')
ax1.plot([0, p1.real], [0, p1.imag], ':', linewidth=1)
ax1.plot([0, p2.real], [0, p2.imag], ':', linewidth=1)

ax1.set_title("Plano s / Lugar das raízes")
ax1.set_xlabel("Parte real")
ax1.set_ylabel("Parte imaginária")
ax1.grid(True, alpha=0.3)
ax1.legend(loc="best")

ax2 = axes[1]
t = np.linspace(0, 2.0, 1200)
t_out, y_out = ct.step_response(G, T=t)
ax2.plot(t_out, y_out, linewidth=2, label='Resposta ao degrau')
ax2.axhline(1.0, linestyle='--', linewidth=1, label='Valor final')
ax2.axhline(1.02, linestyle=':', linewidth=1)
ax2.axhline(0.98, linestyle=':', linewidth=1)
ax2.axvline(Ts, linestyle='--', linewidth=1, label=f'Ts = {Ts:.2f} s')

Tp = np.pi / wd
Mp = np.exp(-zeta*np.pi/np.sqrt(1-zeta**2))
ax2.plot([Tp], [1 + Mp], 'o', markersize=6, label='Pico teórico')

ax2.set_title("Resposta ao degrau")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Saída")
ax2.grid(True, alpha=0.3)
ax2.legend(loc="best")

plt.tight_layout()
plt.show()