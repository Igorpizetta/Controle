import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import sympy as sp


# =========================================================
# Helpers: SymPy TF -> python-control TF
# =========================================================
def sympy_to_control_tf(expr, s):
    expr = sp.simplify(expr)
    num, den = sp.fraction(expr)
    num_poly = sp.Poly(sp.expand(num), s)
    den_poly = sp.Poly(sp.expand(den), s)

    num_coeffs = [float(c) for c in num_poly.all_coeffs()]
    den_coeffs = [float(c) for c in den_poly.all_coeffs()]

    # limpa zeros numéricos muito pequenos
    def clean(v, tol=1e-10):
        return [0.0 if abs(x) < tol else x for x in v]

    return ctl.tf(clean(num_coeffs), clean(den_coeffs))


# =========================================================
# P2.17 (a) — Equações do movimento e TF
# Entrada: T(t) aplicada em J2
# Saída: theta1 ou theta2
# =========================================================
def tf_p217_a(saida="theta2"):
    # ---- parâmetros (altere aqui) ----
    J1  = 5.0     # kg·m^2
    J2  = 3.0     # kg·m^2
    D0  = 8.0     # N·m·s/rad  (J1-terra)
    D12 = 1.0     # N·m·s/rad  (entre J1 e J2)
    K12 = 9.0     # N·m/rad    (entre J1 e J2)
    K2g = 3.0     # N·m/rad    (J2-terra)

    s = sp.Symbol('s')
    Th1, Th2, T = sp.symbols('Th1 Th2 T')

    # Equações em Laplace (CI=0):
    # (J1 s^2 + (D0+D12)s + K12) Th1 - (D12 s + K12) Th2 = 0
    # -(D12 s + K12) Th1 + (J2 s^2 + D12 s + K12 + K2g) Th2 = T
    A11 = J1*s**2 + (D0 + D12)*s + K12
    A12 = -(D12*s + K12)
    A21 = -(D12*s + K12)
    A22 = J2*s**2 + D12*s + K12 + K2g

    # Resolve para Th1 e Th2 em função de T:
    sol = sp.solve([sp.Eq(A11*Th1 + A12*Th2, 0),
                    sp.Eq(A21*Th1 + A22*Th2, T)], (Th1, Th2), simplify=True)

    if saida.lower() == "theta1":
        Gsym = sp.simplify(sol[Th1] / T)
    else:
        Gsym = sp.simplify(sol[Th2] / T)

    return sympy_to_control_tf(Gsym, s)


# =========================================================
# P2.17 (b) — Equações do movimento e TF (clássico)
#
# Topologia:
# T -> J1 -- (K1 em série com D1) -- J2 -- (K2 em série com (D2 || K3)) -- J3
#
# Eliminação "clássica" dos nós internos em Laplace:
#   τ12 = A(s) (Θ1-Θ2),   A(s)= K1*D1*s/(K1 + D1*s)   (série K1 e D1)
#   τ23 = B(s) (Θ2-Θ3),   B(s)= K2*(D2*s + K3)/(K2 + D2*s + K3) (K2 em série com paralelo)
#
# Dinâmica dos rotores:
#   J1 s^2 Θ1 = T - τ12
#   J2 s^2 Θ2 = τ12 - τ23
#   J3 s^2 Θ3 = τ23
# =========================================================
def tf_p217_b(saida="theta2"):
    # ---- parâmetros (altere aqui) ----
    J1 = 1.0
    J2 = 1.0
    J3 = 1.0

    K1 = 1.0
    D1 = 1.0

    K2 = 1.0
    D2 = 1.0
    K3 = 1.0

    s = sp.Symbol('s')
    Th1, Th2, Th3, T = sp.symbols('Th1 Th2 Th3 T')

    A = (K1*D1*s) / (K1 + D1*s)
    B = (K2*(D2*s + K3)) / (K2 + D2*s + K3)

    tau12 = A*(Th1 - Th2)
    tau23 = B*(Th2 - Th3)

    eq1 = sp.Eq(J1*s**2*Th1, T - tau12)
    eq2 = sp.Eq(J2*s**2*Th2, tau12 - tau23)
    eq3 = sp.Eq(J3*s**2*Th3, tau23)

    sol = sp.solve([eq1, eq2, eq3], (Th1, Th2, Th3), simplify=True)

    s_out = saida.lower()
    if s_out == "theta1":
        Gsym = sp.simplify(sol[Th1] / T)
    elif s_out == "theta3":
        Gsym = sp.simplify(sol[Th3] / T)
    else:
        Gsym = sp.simplify(sol[Th2] / T)

    return sympy_to_control_tf(Gsym, s)


# =========================================================
# Simulação (degrau/impulso) em múltiplas janelas
# =========================================================
t = np.linspace(0, 20, 2000)

# -------- (a) --------
Ga = tf_p217_a(saida="theta2")   # mude para "theta1" se quiser
print("P2.17(a)  G_a(s) = Theta_out(s)/T(s) =")
print(Ga)

t_step_a, y_step_a = ctl.step_response(Ga, T=t)
t_imp_a,  y_imp_a  = ctl.impulse_response(Ga, T=t)

plt.figure(1)
plt.plot(t_step_a, y_step_a)
plt.title("P2.17(a) — Resposta ao Degrau (T = 1·u(t))")
plt.xlabel("Tempo (s)")
plt.ylabel("theta(t) [rad]")
plt.grid(True)

plt.figure(2)
plt.plot(t_imp_a, y_imp_a)
plt.title("P2.17(a) — Resposta ao Impulso (T = δ(t))")
plt.xlabel("Tempo (s)")
plt.ylabel("theta(t) [rad]")
plt.grid(True)


# -------- (b) --------
Gb = tf_p217_b(saida="theta2")   # ou "theta1" / "theta3"
print("\nP2.17(b)  G_b(s) = Theta_out(s)/T(s) =")
print(Gb)

t_step_b, y_step_b = ctl.step_response(Gb, T=t)
t_imp_b,  y_imp_b  = ctl.impulse_response(Gb, T=t)

plt.figure(3)
plt.plot(t_step_b, y_step_b)
plt.title("P2.17(b) — Resposta ao Degrau (T = 1·u(t))")
plt.xlabel("Tempo (s)")
plt.ylabel("theta(t) [rad]")
plt.grid(True)

plt.figure(4)
plt.plot(t_imp_b, y_imp_b)
plt.title("P2.17(b) — Resposta ao Impulso (T = δ(t))")
plt.xlabel("Tempo (s)")
plt.ylabel("theta(t) [rad]")
plt.grid(True)

plt.show()