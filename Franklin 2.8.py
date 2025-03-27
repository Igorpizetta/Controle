import os
from sympy import *

import numpy as np                      # Biblioteca para operações numéricas e vetores
import matplotlib.pyplot as plt
from control.matlab import *  # MATLAB-like functions
from math import *

os.system('clear')  # Para macOS e Linux

# Variáveis simbólicas
s = symbols('s')
X, Y, U = symbols('X Y U')
M, m, b,k = symbols('M m b k')
# Constantes do sistema
#M = 4      # massas
#b  = 4     # damping da ligação
#k  = 5     # constante da mola

# Equação para m:
eq1 = Eq(0 , m * s**2*X + b * s * (X - Y) +  k*(X-Y))

# Equação para M:
eq2 = Eq(U , M * s**2*Y + b * s * (Y - X) +  k*(Y-X))

print("Equação para M1:")
pprint(eq1)
print("\nEquação para M2:")
pprint(eq2)

# Resolver o sistema para X1 e X3 em termos de F
sol = solve([eq1, eq2], (X, Y), dict=True)

if sol:
    solucao = sol[0]
    # Calcula a função de transferência X3(s)/F(s)
    TF = simplify(solucao[Y] / U)
    print("\n✅ Função de transferência Y(s)/F(s):")
    pprint(TF)
else:
    print("❌ Nenhuma solução encontrada. Verifique a modelagem.")
pprint(" ")


# ========================
# 1. Substituindo valores para obter a Função de Transferência Numérica
# ========================

# === Substituindo constantes simbólicas por valores numéricos ===
substituicoes = {M: 1, m: 10, b: 5, k: 1}
TF_num = TF.subs(substituicoes)
pprint(TF_num)

# Extrai numerador e denominador
num_sym, den_sym = TF_num.as_numer_denom()

# Usa Poly para extrair coeficientes em s
num_poly = Poly(num_sym, s)
den_poly = Poly(den_sym, s)

# Converte para coeficientes reais
num_coeffs = [float(c) for c in num_poly.all_coeffs()]
den_coeffs = [float(c) for c in den_poly.all_coeffs()]

# Cria sistema de controle
sistema = tf(num_coeffs, den_coeffs)

# Mostra os polos e zeros do sistema
print("\n🎯 Polos do sistema:")
for p in pole(sistema):
    print(f"  {p}")

print("\n🎯 Zeros do sistema:")
for z in zero(sistema):
    print(f"  {z}")

plt.figure(1)
rlocus(sistema)
plt.tight_layout()

# ========================
# 2. Fechando a Malha com Controle Proporcional (K)
# ========================

# Vetor de tempo para simulação
T = np.linspace(0, 100, 10000)

# Definição do ganho proporcional
K = 1  # Pode ser alterado para estudar o efeito de diferentes ganhos

# Sistema em malha fechada com realimentação unitária: Gmf = (K*G)/(1 + K*G)
Gmf = feedback(K*sistema, 1)

# Resposta ao degrau da malha fechada
T_closed, yout_closed = impulse(Gmf, T)

# Gráfico da resposta em malha fechada
plt.figure(2)
plt.plot(yout_closed,T_closed, label=f'K = {K}')
plt.title("Resposta ao Degrau - Malha Fechada")
plt.grid(True)
plt.xlabel("Tempo (s)")
plt.ylabel("Saída")
plt.legend()
plt.tight_layout()
plt.show()