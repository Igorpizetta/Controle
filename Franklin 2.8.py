import os
from sympy import *

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