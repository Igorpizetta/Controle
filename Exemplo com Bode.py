import control as ct
import matplotlib.pyplot as plt
import numpy as np

# Questão (a)
# G(s) = K / [(s + 4)(s + 10)(s + 15)]

# Criando a função de transferência usando ZPK
# Zeros: nenhum
# Polos: -4, -10, -15
# Ganho: K

K = 100
Z = []
P = [-2,-6,-8]
G = ct.zpk(Z, P, K)

# Fechando a malha do sistema original
T = ct.feedback(G, 1)

print("Função de transferência:")
print(G)
print("Função de transferência do sistema em malha fechada:")
print(T)

plt.figure()
ct.rlocus(G)


# Calculando margens
gm, pm, wgm, wpm = ct.margin(G)
print(f"Sistema sem compensação:")
print(f"Margem de ganho: {20*np.log10(gm):.2f} dB")
print(f"Margem de fase: {pm:.2f} graus")
print(f"Frequência da margem de ganho: {wgm:.2f} rad/s")
print(f"Frequência da margem de fase: {wpm:.2f} rad/s")

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


# Montando o compensador
Kc = 1
Zc = [-2]
Pc = [-5.5]
Gc = ct.zpk(Zc, Pc, Kc)

print("Função de transferência do Controlador:")
print(Gc)
print("Função de transferência do Controlador e do sistema:")
print(G*Gc)

# Fechando a malha com o compensador
Tc = ct.feedback(G*Gc, 1)

# Criação do espaço linear para o tempo
t = np.linspace(0, 20, 2000)
t_step, y_step = ct.step_response(T, T=t) # Resposta ao degrau do sistema sem compensação
t_step_c, y_step_c = ct.step_response(Tc, T=t) # Resposta ao degrau do sistema com compensação

# Plotando as respostas ao degrau no domínio do tempo
plt.figure()
plt.plot(t_step, y_step, label="Sistema sem compensação")
plt.plot(t_step_c, y_step_c, label="Sistema com compensação")
plt.title("Resposta ao Degrau")
plt.xlabel("Tempo (s)")
plt.ylabel("Saída")
plt.grid(True)
plt.legend()


plt.show()