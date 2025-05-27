import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import control
import os
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.
# Sistema original
A = np.array([[0, 1], [-7.2, -9.3]])
B = np.array([[0], [1]])
C = np.array([[1, 0]])
D = np.array([[0]])

# Especificações
zeta = 0.707
ts = 0.114
w_n = 4.6/(ts*zeta)

# Polos desejados
s1 = complex(-zeta * w_n, w_n * np.sqrt(1 - zeta**2))
s2 = np.conj(s1)
poles_desired = [s1, s2]
print(poles_desired)

# Cálculo dos polos desejados (raízes do polinômio de 2ª ordem)
char_poly = [1, 2 * zeta * w_n, w_n ** 2]
p = np.roots(char_poly)
print(p)

# Cálculo do ganho K por posicionamento de polos
K = control.place(A, B, poles_desired)

# Sistema em malha fechada: A - BK
A_cl = A - B @ K
sys_cl = signal.StateSpace(A_cl, B, C, D)

# Resposta ao degrau
t, y = signal.step(sys_cl)


# Gráfico
plt.figure()
plt.plot(t, y)
plt.title("Resposta ao Degrau - Sistema com Realimentação de Estados")
plt.xlabel("Tempo [s]")
plt.ylabel("Saída y(t)")
plt.grid(True)
plt.show()

# Exibir ganho K e verificar polos
print("Ganho de realimentação de estado K:", K)
print("Polos do sistema em malha fechada:", np.linalg.eigvals(A_cl))