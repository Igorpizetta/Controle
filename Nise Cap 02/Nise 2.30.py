import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# =========================
# Figura P2.15 — parâmetros (altere aqui)
# =========================
M1 = 4.0
M2 = 5.0
M3 = 5.0

K1 = 5.0
K2 = 4.0
K3 = 4.0

fv1 = 2.0
fv2 = 2.0
fv3 = 3.0

# =========================================================
# Equações (forma matricial):  M xdd + C xd + K x = B f(t)
# x = [x1, x2, x3]^T
# =========================================================
M = np.diag([M1, M2, M3])

C = np.array([
    [fv1 + fv2,     0.0,      -fv1],
    [0.0,           fv3,      -fv3],
    [-fv1,         -fv3,   fv1 + fv3]
])

K = np.array([
    [K2 + K3,   -K3,     0.0],
    [-K3,        K3,     0.0],
    [0.0,        0.0,     K1]
])

# entrada é a força aplicada em M2
B = np.array([[0.0],
              [1.0],
              [0.0]])

# =========================================================
# Espaço de estados:
# z = [x1 x2 x3 x1dot x2dot x3dot]^T
# z' = A z + Bd f(t)
# saída: escolha o que você quer observar (ex.: x2)
# =========================================================
Z = np.zeros((3, 3))
I = np.eye(3)
Minv = np.linalg.inv(M)

A_top = np.hstack((Z, I))
A_bot = np.hstack((-Minv @ K, -Minv @ C))
A = np.vstack((A_top, A_bot))

Bd = np.vstack((np.zeros((3, 1)), Minv @ B))

# Saída: x2 (mude para x1 ou x3 se quiser)
# x1 -> C = [1,0,0,0,0,0]
# x2 -> C = [0,1,0,0,0,0]
# x3 -> C = [0,0,1,0,0,0]
Cout = np.array([[0, 1, 0, 0, 0, 0]])
Dout = np.array([[0.0]])

sys = ctl.ss(A, Bd, Cout, Dout)

print("Sistema em espaço de estados (entrada f(t) em M2, saída x2):")
print(sys)

# =========================================================
# (Opcional) Transfer function X2(s)/F(s)
# =========================================================
G = ctl.ss2tf(sys)
print("\nG(s) = X2(s)/F(s) =")
print(G)

# =========================================================
# Respostas ao degrau e impulso
# =========================================================
t = np.linspace(0, 20, 2000)

t_step, y_step = ctl.step_response(sys, T=t)
t_imp,  y_imp  = ctl.impulse_response(sys, T=t)

plt.figure(1)
plt.plot(t_step, y_step)
plt.title("Figura P2.15 — Resposta ao Degrau (f = 1·u(t)) — saída x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t) [m]")
plt.grid(True)

plt.figure(2)
plt.plot(t_imp, y_imp)
plt.title("Figura P2.15 — Resposta ao Impulso (f = δ(t)) — saída x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t) [m]")
plt.grid(True)

plt.show()