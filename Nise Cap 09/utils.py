import numpy as np
from control import rlocus

def encontrar_polos_por_zeta(G, zeta_alvo, num_pontos=1000):
    sigma_range = np.linspace(-10, -0.1, num_pontos)
    wd = sigma_range * np.tan(np.arccos(zeta_alvo))
    polos_alvo = sigma_range + 1j * wd

    rlist, klist = rlocus(G, plot=False)

    melhor_erro = float('inf')
    melhor_polo = None
    melhor_k = None

    for k_idx, polos in enumerate(rlist):
        for p in polos:
            if np.imag(p) != 0:
                zeta_p = -np.real(p) / np.abs(p)
                if abs(zeta_p - zeta_alvo) < 0.01:
                    erro_total = abs(np.imag(p) - wd[np.argmin(abs(sigma_range + 1j * wd - p))])
                    if erro_total < melhor_erro:
                        melhor_erro = erro_total
                        melhor_polo = p
                        melhor_k = klist[k_idx]

    if melhor_polo is not None:
        sigma = np.real(melhor_polo)
        wd = np.imag(melhor_polo)
        return sigma, wd, melhor_k, melhor_polo
    else:
        return None, None, None, None