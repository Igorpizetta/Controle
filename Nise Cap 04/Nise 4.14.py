import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import sympy as sp


# --------------------------------------------------
# Dados do problema
# --------------------------------------------------
M = 2
fv = 2
Ks = 6

# Equação: M x'' + fv x' + Ks x = f(t)
# Função de transferência: X(s)/F(s) = 1 / (M s^2 + fv s + Ks)

num = [1]
den = [M, fv, Ks]

G = ctl.TransferFunction(num, den)

print("Função de transferência X(s)/F(s):")
print(G)

# --------------------------------------------------
# Polos do sistema
# --------------------------------------------------
polos = ctl.poles(G)
print("\nPolos do sistema:")
print(polos)

# --------------------------------------------------
# Resposta ao degrau: x(t) para f(t) = u(t)
# --------------------------------------------------
t = np.linspace(0, 10, 1000)
t, x = ctl.step_response(G, T=t)

# valor final esperado
x_final = 1 / Ks
print(f"\nValor final x(∞) = {x_final:.4f} m")

# --------------------------------------------------
# Plot das raízes no plano s e da resposta ao degrau
# --------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].scatter(np.real(polos), np.imag(polos), s=80, marker='x', label='Polos')
ax[0].axhline(0, linewidth=1)
ax[0].axvline(0, linewidth=1)
ax[0].grid(True, linestyle='--', alpha=0.7)
ax[0].set_xlabel('Parte real')
ax[0].set_ylabel('Parte imaginária')
ax[0].set_title('Raízes no plano s')
ax[0].legend()

margem_x = max(0.5, 0.2 * np.max(np.abs(np.real(polos))))
margem_y = max(0.5, 0.2 * np.max(np.abs(np.imag(polos))))
ax[0].set_xlim(np.min(np.real(polos)) - margem_x, np.max(np.real(polos)) + margem_x)
ax[0].set_ylim(np.min(np.imag(polos)) - margem_y, np.max(np.imag(polos)) + margem_y)

ax[1].plot(t, x, label='x(t)')
ax[1].axhline(x_final, linestyle='--', label='valor final')
ax[1].grid(True)
ax[1].set_xlabel('Tempo (s)')
ax[1].set_ylabel('x(t) [m]')
ax[1].set_title('Resposta ao degrau do sistema massa-mola-amortecedor')
ax[1].legend()

plt.tight_layout()
plt.show()


# --------------------------------------------------
# Expressão analítica de x(t) usando SymPy
# --------------------------------------------------
s, ts = sp.symbols('s t', positive=True, real=True)

Xs = 1 / (s * (M*s**2 + fv*s + Ks))
xt = sp.inverse_laplace_transform(Xs, s, ts)

print("\nX(s) =")
print(sp.simplify(Xs))

print("\nx(t) =")
print(sp.simplify(xt))
