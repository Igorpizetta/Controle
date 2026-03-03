import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# Parâmetros
m = 5
c = 4
k = 5

# Função de transferência
G = ctl.tf([1], [m, c, k])

# Vetor de tempo
t = np.linspace(0, 20, 1000)

# Resposta ao degrau
t_step, y_step = ctl.step_response(G, t)

# Resposta ao impulso
t_imp, y_imp = ctl.impulse_response(G, t)

# Plot degrau
plt.figure()
plt.plot(t_step, y_step)
plt.title('Resposta ao Degrau')
plt.xlabel('Tempo (s)')
plt.ylabel('x(t)')
plt.grid()
plt.show()

# Plot impulso
plt.figure()
plt.plot(t_imp, y_imp)
plt.title('Resposta ao Impulso')
plt.xlabel('Tempo (s)')
plt.ylabel('x(t)')
plt.grid()
plt.show()