import numpy as np
import matplotlib.pyplot as plt
import control as ct

# ------------------------------------------------------------
# Questão 33
# Interpretação:
# As expressões dadas são C(s), isto é, a resposta ao degrau no domínio de Laplace.
# Logo, a função de transferência é T(s) = s*C(s).
# A ideia é verificar se o zero próximo de -2 pode cancelar aproximadamente
# o polo em -2, restando um comportamento dominado pelo fator de 2ª ordem.
# ------------------------------------------------------------

cases = {
    "a": {"z": 4.00, "quad": [1, 3, 10]},
    "b": {"z": 2.50, "quad": [1, 4, 20]},
    "c": {"z": 2.20, "quad": [1, 1, 5]},
    "d": {"z": 2.01, "quad": [1, 5, 20]},
}

# Veredito qualitativo de cancelamento aproximado
# critério didático:
# 1) o zero deve estar perto do polo em -2
# 2) esse polo cancelado deve ser suficientemente mais rápido que o par dominante
verdict = {
    "a": False,
    "b": False,
    "c": True,
    "d": True,
}

reasons = {
    "a": "Não. O zero está em -4, longe do polo em -2; não há cancelamento aproximado.",
    "b": "Não. O zero em -2.5 até está relativamente perto de -2, mas o polo em -2 não é muito mais rápido que o par complexo (-2 ± j4); ele participa fortemente da dinâmica.",
    "c": "Sim. O zero em -2.2 está perto do polo em -2, e esse modo está bem à esquerda do par dominante (-0.5 ± j2.179).",
    "d": "Sim. O zero em -2.01 praticamente cancela o polo em -2, restando claramente a dinâmica de 2ª ordem.",
}

def second_order_specs_from_quad(a1, a0):
    # s^2 + a1 s + a0 = s^2 + 2*zeta*wn*s + wn^2
    wn = np.sqrt(a0)
    zeta = a1 / (2 * wn)
    wd = wn * np.sqrt(1 - zeta**2)

    OS = 100 * np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2))
    Ts = 4 / (zeta * wn)                   # critério de 2%
    Tp = np.pi / wd
    phi = np.arccos(zeta)
    Tr = (np.pi - phi) / wd               # aproximação 0-100%

    return zeta, wn, wd, OS, Ts, Tr, Tp

# ------------------------------------------------------------
# Impressão das explicações
# ------------------------------------------------------------
print("=" * 88)
print("QUESTÃO 33 - Cancelamento aproximado polo-zero")
print("=" * 88)
print("Para cada item, usamos T(s) = s*C(s) e verificamos se o zero próximo de -2")
print("pode cancelar aproximadamente o polo em -2. Quando isso é válido,")
print("o comportamento é aproximado por 1 / (fator quadrático).")
print()

results = {}

for key, data in cases.items():
    z = data["z"]
    q = data["quad"]          # [1, a1, a0]
    a1, a0 = q[1], q[2]

    # Função de transferência exata T(s) = (s+z)/((s+2)(s^2+a1*s+a0))
    T = ct.tf([1, z], np.polymul([1, 2], q))

    # Aproximação mantendo apenas o par do fator quadrático
    # e substituindo o polo em -2 por seu ganho em regime permanente.
    T_dom = 0.5 * ct.tf([1, z], q)

    # Aproximação por cancelamento: T_aprox(s) ~ 1/(s^2+a1*s+a0)
    T_approx = ct.tf([1], q)

    poles = ct.poles(T)
    zeros = ct.zeros(T)

    zeta, wn, wd, OS, Ts, Tr, Tp = second_order_specs_from_quad(a1, a0)

    results[key] = {
        "T": T,
        "T_dom": T_dom,
        "T_approx": T_approx,
        "poles": poles,
        "zeros": zeros,
        "zeta": zeta,
        "wn": wn,
        "wd": wd,
        "OS": OS,
        "Ts": Ts,
        "Tr": Tr,
        "Tp": Tp,
    }

    print(f"Item {key})")
    print(f"  T(s) = (s + {z}) / [ (s+2) ({q[0]} s^2 + {a1} s + {a0}) ]")
    print(f"  Polos exatos : {np.array2string(np.array(poles), precision=4)}")
    print(f"  Zeros exatos : {np.array2string(np.array(zeros), precision=4)}")
    print(f"  Veredito     : {reasons[key]}")
    if verdict[key]:
        print("  Aproximação de 2ª ordem:")
        print(f"    zeta = {zeta:.4f}")
        print(f"    wn   = {wn:.4f} rad/s")
        print(f"    %OS  = {OS:.2f}%")
        print(f"    Ts   = {Ts:.3f} s")
        print(f"    Tr   = {Tr:.3f} s")
        print(f"    Tp   = {Tp:.3f} s")
    else:
        print("  Como o cancelamento não é uma boa aproximação, não usamos as fórmulas")
        print("  de 2ª ordem para estimar os índices transitórios.")
    print("-" * 88)

# ------------------------------------------------------------
# Gráficos
# Uma figura para cada item:
#   esquerda  -> rlocus
#   direita   -> resposta ao degrau (exata e, se couber, aproximada)
# ------------------------------------------------------------
for key in ["a", "b", "c", "d"]:
    res = results[key]
    T = res["T"]
    T_dom = res["T_dom"]
    T_approx = res["T_approx"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), num=f"Item {key}")

    # -------------------------
    # RLocus
    # -------------------------
    ax1 = axes[0]
    ct.rlocus(T, gains=np.linspace(0, 40, 800), ax=ax1)

    # Marca polos e zero do sistema original
    poles = np.array(res["poles"])
    zeros = np.array(res["zeros"])
    ax1.plot(poles.real, poles.imag, 'x', markersize=9, markeredgewidth=2, label='Polos de T(s)')
    ax1.plot(zeros.real, zeros.imag, 'o', markersize=7, fillstyle='none', markeredgewidth=2, label='Zero de T(s)')

    # Se houver aproximação válida, destacar par de 2ª ordem
    if verdict[key]:
        quad_roots = np.roots(cases[key]["quad"])
        ax1.plot(quad_roots.real, quad_roots.imag, 'r*', markersize=11, label='Par dominante (aprox.)')
        title_verdict = "cancelamento aproximado: SIM"
    else:
        title_verdict = "cancelamento aproximado: NÃO"

    ax1.set_title(f"Item {key}) RLocus  |  {title_verdict}")
    ax1.set_xlabel("Parte real")
    ax1.set_ylabel("Parte imaginária")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="best")

    # -------------------------
    # Resposta ao degrau
    # -------------------------
    ax2 = axes[1]

    # Escolher janela de tempo razoável
    if verdict[key]:
        t_end = max(3 * res["Ts"], 6)
    else:
        t_end = 10

    t = np.linspace(0, t_end, 1500)
    t1, y1 = ct.step_response(T, T=t)
    ax2.plot(t1, y1, linewidth=2, label='Resposta exata')

    t_dom, y_dom = ct.step_response(T_dom, T=t)
    ax2.plot(t_dom, y_dom, '-.', linewidth=2, label='Apenas o par de polos')

    if verdict[key]:
        t2, y2 = ct.step_response(T_approx, T=t)
        ax2.plot(t2, y2, '--', linewidth=2, label='Cancelamento aproximado (2ª ordem)')

        txt = (
            f"SIM\n"
            f"%OS = {res['OS']:.2f}%\n"
            f"Ts = {res['Ts']:.3f} s\n"
            f"Tr = {res['Tr']:.3f} s\n"
            f"Tp = {res['Tp']:.3f} s"
        )
    else:
        txt = "NÃO\nNão é adequado usar\ncancelamento aproximado."

    ax2.text(
        0.98, 0.95, txt,
        transform=ax2.transAxes,
        ha="right", va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
    )

    ax2.set_title(f"Item {key}) Resposta ao degrau")
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Saída")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="best")

    fig.tight_layout()

plt.show()
