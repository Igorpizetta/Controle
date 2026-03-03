import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# G(s) = (3s + 5) / (2s^4 + 17s^3 + 44s^2 + 45s + 20)
G = ctl.tf([3, 5], [2, 17, 44, 45, 20])

print("G(s) = X1(s)/F(s) =")
print(G)

t = np.linspace(0, 20, 3000)

# Resposta ao degrau
t_step, y_step = ctl.step_response(G, T=t)

# Resposta ao impulso
t_imp, y_imp = ctl.impulse_response(G, T=t)

plt.figure()
plt.plot(t_step, y_step)
plt.title("Resposta ao Degrau (F = 1·u(t)) — saída x1(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x1(t) [m]")
plt.grid(True)

plt.figure()
plt.plot(t_imp, y_imp)
plt.title("Resposta ao Impulso (F = δ(t)) — saída x1(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x1(t) [m]")
plt.grid(True)

plt.show()