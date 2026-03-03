import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# G(s) = 3 / (8 s^4 + 12 s^3 + 26 s^2 + 18 s)
G = ctl.tf([3], [8, 12, 26, 18, 0])

print("G(s) = X3(s)/F(s) =")
print(G)

t = np.linspace(0, 20, 4000)

# Resposta ao degrau
t_step, y_step = ctl.step_response(G, T=t)

# Resposta ao impulso
t_imp, y_imp = ctl.impulse_response(G, T=t)

plt.figure()
plt.plot(t_step, y_step)
plt.title("Resposta ao Degrau (F = 1·u(t)) — saída x3(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)

plt.figure()
plt.plot(t_imp, y_imp)
plt.title("Resposta ao Impulso (F = δ(t)) — saída x3(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x3(t) [m]")
plt.grid(True)

plt.show()