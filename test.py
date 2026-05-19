import control as ct
import matplotlib.pyplot as plt
import numpy as np

# Questão (a)
# G(s) = K / [(s + 4)(s + 10)(s + 15)]

K = 2102.76

# Criando a FT usando zpk
# Zeros = nenhum
# Polos = -4, -10, -15
# Ganho = K
G = ct.zpk([], [-4, -10, -15], K)

print(G)

# Frequências para o gráfico
omega = np.logspace(-1, 3, 1000)  # de 10^-1 até 10^3 rad/s

# Diagrama de Bode
plt.figure(figsize=(8, 6))

ct.bode_plot(
    G,
    omega=omega,
    dB=True,
    deg=True,
    grid=True,
    margins=True
)

# Pegando os eixos do gráfico
fig = plt.gcf()
ax_mag = fig.axes[0]    # magnitude
ax_phase = fig.axes[1]  # fase

# Configuração da escala do eixo x
ax_mag.set_xlim([0.1, 1000])
ax_phase.set_xlim([0.1, 1000])

# Configuração da escala do eixo y
ax_mag.set_ylim([-80, 60])       # magnitude em dB
ax_phase.set_ylim([-300, 0])     # fase em graus

# Linhas de referência
ax_mag.axhline(0, color='black', linewidth=0.8)
ax_phase.axhline(-180, color='black', linewidth=0.8)

# Títulos dos eixos
ax_mag.set_ylabel("Magnitude [dB]")
ax_phase.set_ylabel("Fase [graus]")
ax_phase.set_xlabel("Frequência [rad/s]")

plt.show()