import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import pandas as pd


# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
def second_order_specs(num, den):
    """
    Extrai zeta, wn, Ts, Tp, Tr e %OS de um sistema de 2ª ordem
    na forma:
        T(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
    """
    # den = [1, a1, a0] -> s^2 + a1*s + a0
    a2, a1, a0 = den

    wn = np.sqrt(a0)
    zeta = a1 / (2 * wn)

    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta**2)
        Ts = 4 / (zeta * wn)                      # critério de 2%
        Tp = np.pi / wd
        Tr = (np.pi - np.arccos(zeta)) / wd      # 0–100% para subamortecido
        OS = 100 * np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2))
    elif np.isclose(zeta, 1):
        wd = 0.0
        Ts = 4 / (zeta * wn)
        Tp = np.nan
        Tr = np.nan
        OS = 0.0
    else:
        wd = np.nan
        Ts = 4 / (zeta * wn)
        Tp = np.nan
        Tr = np.nan
        OS = 0.0

    return {
        "zeta": zeta,
        "wn": wn,
        "Ts": Ts,
        "Tp": Tp,
        "Tr": Tr,
        "%OS": OS
    }


def print_specs_table(results):
    df = pd.DataFrame(results).T
    pd.set_option("display.float_format", lambda x: f"{x:.6f}")
    print("\nEspecificações calculadas:\n")
    print(df)


def plot_poles_and_step(sys, title):
    poles = ctl.poles(sys)

    # Escolha automática de tempo para simulação
    den = np.squeeze(sys.den[0][0])
    _, a1, a0 = den
    wn = np.sqrt(a0)
    zeta = a1 / (2 * wn)

    # tempo final razoável para visualização
    if zeta > 0:
        tfinal = max(5 * (4 / (zeta * wn)), 5 / wn)
    else:
        tfinal = 10 / wn

    t = np.linspace(0, tfinal, 2000)
    t, y = ctl.step_response(sys, T=t)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), num=title)

    # --------------------------------------------------------
    # Plano-s
    # --------------------------------------------------------
    ax[0].scatter(np.real(poles), np.imag(poles), s=80, marker='x')
    ax[0].axhline(0, linewidth=1)
    ax[0].axvline(0, linewidth=1)
    ax[0].grid(True, linestyle='--', alpha=0.7)
    ax[0].set_title(f"Raízes no plano s\n{title}")
    ax[0].set_xlabel("Parte Real")
    ax[0].set_ylabel("Parte Imaginária")

    # Ajuste de limites
    margem_x = max(1.0, 0.2 * np.max(np.abs(np.real(poles))))
    margem_y = max(1.0, 0.2 * np.max(np.abs(np.imag(poles))) if np.max(np.abs(np.imag(poles))) > 0 else 1.0)
    ax[0].set_xlim(np.min(np.real(poles)) - margem_x, margem_x)
    ax[0].set_ylim(np.min(np.imag(poles)) - margem_y, np.max(np.imag(poles)) + margem_y)

    # --------------------------------------------------------
    # Resposta ao degrau
    # --------------------------------------------------------
    ax[1].plot(t, y, linewidth=2)
    ax[1].axhline(1.0, linestyle='--', linewidth=1)
    ax[1].grid(True, linestyle='--', alpha=0.7)
    ax[1].set_title(f"Resposta ao degrau\n{title}")
    ax[1].set_xlabel("Tempo [s]")
    ax[1].set_ylabel("Saída")

    plt.tight_layout()
    return fig


# ------------------------------------------------------------
# Sistemas do enunciado
# ------------------------------------------------------------
systems = {
    "a": {
        "num": [16],
        "den": [1, 3, 16],
        "label": r"$T(s)=\frac{16}{s^2+3s+16}$"
    },
    "b": {
        "num": [0.04],
        "den": [1, 0.02, 0.04],
        "label": r"$T(s)=\frac{0.04}{s^2+0.02s+0.04}$"
    },
    "c": {
        "num": [1.05e7],
        "den": [1, 1.6e3, 1.05e7],
        "label": r"$T(s)=\frac{1.05\times10^7}{s^2+1.6\times10^3s+1.05\times10^7}$"
    }
}


# ------------------------------------------------------------
# Cálculo das especificações
# ------------------------------------------------------------
results = {}

for key, data in systems.items():
    num = data["num"]
    den = data["den"]

    sys = ctl.TransferFunction(num, den)
    specs = second_order_specs(num, den)

    results[key] = specs

    print(f"\nSistema {key}: {data['label']}")
    print(f"zeta = {specs['zeta']:.6f}")
    print(f"wn   = {specs['wn']:.6f} rad/s")
    print(f"Ts   = {specs['Ts']:.6f} s")
    print(f"Tp   = {specs['Tp']:.6f} s")
    print(f"Tr   = {specs['Tr']:.6f} s")
    print(f"%OS  = {specs['%OS']:.6f} %")

print_specs_table(results)


# ------------------------------------------------------------
# Plotagem
# ------------------------------------------------------------
for key, data in systems.items():
    sys = ctl.TransferFunction(data["num"], data["den"])
    plot_poles_and_step(sys, f"Sistema {key}: {data['label']}")

plt.show()