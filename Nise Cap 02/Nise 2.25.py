import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# G(s) = (s+1)/(s^4 + 2 s^3 + 2 s^2)
G = ctl.tf([1, 1], [1, 2, 2, 0, 0])

t = np.linspace(0, 20, 4000)

# Resposta ao degrau
t_step, y_step = ctl.step_response(G, T=t)

# Resposta ao impulso
t_imp, y_imp = ctl.impulse_response(G, T=t)

plt.figure()
plt.plot(t_step, y_step)
plt.title("Resposta ao Degrau (F = 1·u(t)) — saída x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t) [m]")
plt.grid(True)

plt.figure()
plt.plot(t_imp, y_imp)
plt.title("Resposta ao Impulso (F = δ(t)) — saída x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t) [m]")
plt.grid(True)

plt.show()