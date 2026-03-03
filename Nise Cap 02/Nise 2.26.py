import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# G(s) = (4s + 3) / (8s^2 + 10s + 2)
G = ctl.tf([4, 3], [8, 10, 2])

print("Função de Transferência:")
print(G)

t = np.linspace(0, 20, 2000)

# Resposta ao degrau
t_step, y_step = ctl.step_response(G, T=t)

# Resposta ao impulso
t_imp, y_imp = ctl.impulse_response(G, T=t)

plt.figure()
plt.plot(t_step, y_step)
plt.title("Resposta ao Degrau — x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t)")
plt.grid(True)

plt.figure()
plt.plot(t_imp, y_imp)
plt.title("Resposta ao Impulso — x2(t)")
plt.xlabel("Tempo (s)")
plt.ylabel("x2(t)")
plt.grid(True)

plt.show()