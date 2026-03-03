import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# Vetor de tempo
t = np.linspace(0, 20, 1000)

# =========================
# Sistema (a) — X3(s)/F(s)
# Ga(s) = (0.8125 s + 1.25) / (s^4 + 6.25 s^3 + 10.75 s^2 + 3.75 s)
# =========================
Ga = ctl.tf([0.8125, 1.25], [1.0, 6.25, 10.75, 3.75, 0.0])

print("Ga(s) = X3(s)/F(s) do sistema (a) =")
print(Ga)

t_step_a, y_step_a = ctl.step_response(Ga, T=t)
t_imp_a,  y_imp_a  = ctl.impulse_response(Ga, T=t)

plt.figure(1)
plt.plot(t_step_a, y_step_a)
plt.title("Sistema (a) — Resposta ao Degrau")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)

plt.figure(2)
plt.plot(t_imp_a, y_imp_a)
plt.title("Sistema (a) — Resposta ao Impulso")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)


# =========================
# Sistema (b) — X3(s)/F(s)
# Gb(s) = (0.28385417 s^2 + 0.82291667 s + 0.0390625) /
#         (s^5 + 2.77083333 s^4 + 9.05208333 s^3 + 0.4296875 s^2)
# =========================

Gb = ctl.tf(
    [0.28385417, 0.82291667, 0.0390625],
    [1.0, 2.77083333, 9.05208333, 0.4296875, 0.0, 0.0]
)

print("\nGb(s) = X3(s)/F(s) do sistema (b) =")
print(Gb)

t_step_b, y_step_b = ctl.step_response(Gb, T=t)
t_imp_b,  y_imp_b  = ctl.impulse_response(Gb, T=t)

plt.figure(3)
plt.plot(t_step_b, y_step_b)
plt.title("Sistema (b) — Resposta ao Degrau")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)

plt.figure(4)
plt.plot(t_imp_b, y_imp_b)
plt.title("Sistema (b) — Resposta ao Impulso")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)

# Mostra todas as janelas (vai bloquear até você fechar)
plt.show()