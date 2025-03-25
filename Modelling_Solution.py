import os
from sympy import *
import sympy as sp
os.system('clear')  # Para macOS e Linux

# Variáveis simbólicas
s = symbols('s')
X1, X3, F = symbols('X1 X3 F')

# Constantes do sistema
M = 4      # massas
b1 = 4     # damping da massa 1 (ao solo)
b2 = 4     # damping da massa 2 (ao solo)
b  = 4     # damping da ligação
k  = 5     # constante da mola

# Equação para M1:
# 4 s² X1 = F - 4 s X1 - 1/2*[ 4(sX1 - sX3) + 5(X1 - X3) ]
eq1 = Eq(M * s**2 * X1, F - b1 * s * X1 - (1/2)*( b*(s*X1 - s*X3) + k*(X1 - X3) ))

# Equação para M2:
# 4 s² X3 = -4 s X3 + 1/2*[ 4(sX1 - sX3) + 5(X1 - X3) ]
eq2 = Eq(M * s**2 * X3, -b2 * s * X3 + (1/2)*( b*(s*X1 - s*X3) + k*(X1 - X3) ))

print("Equação para M1:")
pprint(eq1)
print("\nEquação para M2:")
pprint(eq2)

# Resolver o sistema para X1 e X3 em termos de F
sol = solve([eq1, eq2], (X1, X3), dict=True)

if sol:
    solucao = sol[0]
    # Calcula a função de transferência X3(s)/F(s)
    TF = simplify(solucao[X3] / F)
    print("\n✅ Função de transferência X3(s)/F(s):")
    pprint(TF)
else:
    print("❌ Nenhuma solução encontrada. Verifique a modelagem.")
pprint(" ")