import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import brentq

# -----------------------------
# Funções auxiliares
# -----------------------------
def zeta_from_os(percent_os):
    """Obtém zeta a partir do percentual de overshoot."""
    os = percent_os / 100.0
    f = lambda z: np.exp(-z*np.pi/np.sqrt(1-z**2)) - os
    return brentq(f, 1e-6, 0.999999)

def second_order_from_specs(OS=None, Ts=None, Tp=None):
    """
    Retorna zeta, wn e polos dominantes para um sistema de 2ª ordem
    usando as relações clássicas:
      %OS = exp(-zeta*pi/sqrt(1-zeta²))*100
      Ts(2%) = 4/(zeta*wn)
      Tp = pi/(wn*sqrt(1-zeta²))
    """
    if OS is not None:
        zeta = zeta_from_os(OS)
    else:
        zeta = None

    if Ts is not None and zeta is not None:
        wn = 4.0 / (zeta * Ts)
    elif Tp is not None and zeta is not None:
        wn = np.pi / (Tp * np.sqrt(1 - zeta**2))
    elif Ts is not None and Tp is not None:
        # Resolver o sistema:
        # zeta*wn = 4/Ts
        # wn*sqrt(1-zeta²) = pi/Tp
        a = 4.0 / Ts
        b = np.pi / Tp
        wn = np.sqrt(a*a + b*b)
        zeta = a / wn
    else:
        raise ValueError("Especificações insuficientes.")

    sigma = -zeta * wn
    wd = wn * np.sqrt(1 - zeta**2)
    poles = np.array([sigma + 1j*wd, sigma - 1j*wd])
    return zeta, wn, poles

def step_response_second_order(zeta, wn, t_final=None):
    """Resposta ao degrau do sistema padrão de 2ª ordem: wn²/(s² + 2ζwn s + wn²)."""
    sys = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])
    if t_final is None:
        t_final = max(5*(4/(zeta*wn)), 5)  # horizonte razoável
    t = np.linspace(0, t_final, 1200)
    tout, y = signal.step(sys, T=t)
    return tout, y

# -----------------------------
# Cálculo dos itens
# -----------------------------
cases = {
    "a": {"OS": 12, "Ts": 0.6, "Tp": None},
    "b": {"OS": 10, "Ts": None, "Tp": 5},
    "c": {"OS": None, "Ts": 7, "Tp": 3},
}

results = {}

for key, specs in cases.items():
    zeta, wn, poles = second_order_from_specs(OS=specs["OS"], Ts=specs["Ts"], Tp=specs["Tp"])
    results[key] = {
        "zeta": zeta,
        "wn": wn,
        "poles": poles,
    }

# Mostrar resultados numéricos
for key, r in results.items():
    p1, p2 = r["poles"]
    print(f"Item {key})")
    print(f"  zeta = {r['zeta']:.4f}")
    print(f"  wn   = {r['wn']:.4f} rad/s")
    print(f"  polos = {p1.real:.4f} + j{abs(p1.imag):.4f}  e  {p2.real:.4f} - j{abs(p2.imag):.4f}\n")

# -----------------------------
# Plotagem
# Uma figura para cada item:
# esquerda -> polos no plano-s
# direita  -> resposta ao degrau
# -----------------------------
for key in ["a", "b", "c"]:
    r = results[key]
    zeta = r["zeta"]
    wn = r["wn"]
    poles = r["poles"]
    sigma = poles[0].real
    wd = abs(poles[0].imag)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), num=f"Item {key}")

    # --- Plano-s (localização dos polos) ---
    ax = axes[0]

    # Eixos
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    # Linhas-guia: raio wn e ângulo de amortecimento
    theta = np.linspace(0, np.pi, 400)
    ax.plot(wn*np.cos(theta), wn*np.sin(theta), linestyle='--', linewidth=1, label=r'$\omega_n$')
    ax.plot([0, sigma], [0, wd], linestyle=':', linewidth=1, label=r'linha até polo')
    ax.plot([0, sigma], [0, -wd], linestyle=':', linewidth=1)

    # Polos
    ax.plot(poles.real, poles.imag, 'x', markersize=10, markeredgewidth=2, label='Polos')
    ax.plot([sigma, sigma], [-wd, wd], linestyle='--', linewidth=1, alpha=0.8)

    # Texto
    ax.set_title(
        f"Item {key}) Plano-s\n"
        f"$\\zeta={zeta:.3f}$, $\\omega_n={wn:.3f}$ rad/s\n"
        f"$s={sigma:.3f}\\pm j{wd:.3f}$"
    )
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginária")
    ax.grid(True, alpha=0.3)

    # Limites
    xmax = max(1.2*abs(sigma), 1)
    ymax = max(1.3*wd, 1)
    ax.set_xlim(-xmax*1.8, xmax*0.4)
    ax.set_ylim(-ymax, ymax)
    ax.legend(loc="upper left")

    # --- Resposta ao degrau ---
    ax2 = axes[1]
    t_final = max(2*4/(zeta*wn), 2*(np.pi/(wn*np.sqrt(1-zeta**2))), 2)
    t, y = step_response_second_order(zeta, wn, t_final=t_final*1.5)
    ax2.plot(t, y, linewidth=2)
    ax2.axhline(1.0, linestyle='--', linewidth=1)
    ax2.set_title(f"Item {key}) Resposta ao degrau")
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Saída")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()

plt.show()
