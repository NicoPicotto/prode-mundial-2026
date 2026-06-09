"""
Modelo Dixon-Coles para el PRODE del Mundial 2026.

Reglas del PRODE: 5 puntos por marcador EXACTO, 2 puntos por acertar el SIGNO (1/X/2).

Qué hace, en cuatro pasos:
  1. Toma el rating Elo de cada selección (data.py).
  2. Convierte la diferencia de Elo en goles esperados de cada equipo (lambda).
  3. Arma la matriz de probabilidad de todos los marcadores, con la corrección
     Dixon-Coles que ajusta los marcadores bajos (0-0, 1-0, 1-1...).
  4. Para cada marcador candidato calcula el VALOR ESPERADO de puntos del PRODE
     y elige el que más puntos rinde. Ese es el pick óptimo (no la simple moda).

Uso:
    python src/model.py
Genera output/picks.csv y output/picks.json e imprime la tabla por pantalla.
"""
import csv
import json
import os
import numpy as np
from scipy.stats import poisson

from data import ELO, GRUPOS, HOSTS, FIXTURE

# ---- Parámetros del modelo (tocá estos para recalibrar) ----
MU = 2.60       # goles totales esperados en un partido parejo (promedio mundialista)
BETA = 0.0019   # cuánto pesa la diferencia de Elo en la supremacía de goles
RHO = -0.08     # corrección Dixon-Coles para marcadores bajos
HOST_BONUS = 55  # bonus de Elo para el anfitrión que juega en su país
MAXG = 8        # tope de goles considerados en la matriz


def dc_tau(i, j, lh, la, rho):
    """Factor de corrección Dixon-Coles para los cuatro marcadores bajos."""
    if i == 0 and j == 0: return 1 - lh * la * rho
    if i == 0 and j == 1: return 1 + lh * rho
    if i == 1 and j == 0: return 1 + la * rho
    if i == 1 and j == 1: return 1 - rho
    return 1.0


def lambdas(home, away, host_local=None):
    """Goles esperados de local y visitante a partir de la diferencia de Elo."""
    eh, ea = ELO[home], ELO[away]
    if host_local == home: eh += HOST_BONUS
    if host_local == away: ea += HOST_BONUS
    d = eh - ea
    lh = (MU / 2) * np.exp(BETA * d)
    la = (MU / 2) * np.exp(-BETA * d)
    return lh, la


def score_matrix(lh, la, rho=RHO, maxg=MAXG):
    """Matriz P(i,j) = probabilidad de que el partido termine i (local) a j (visitante)."""
    ph = poisson.pmf(np.arange(maxg + 1), lh)
    pa = poisson.pmf(np.arange(maxg + 1), la)
    M = np.outer(ph, pa)
    for i in range(2):
        for j in range(2):
            M[i, j] *= dc_tau(i, j, lh, la, rho)
    return M / M.sum()


def best_prode_score(M):
    """Marcador (i,j) que maximiza el valor esperado de puntos del PRODE."""
    n = M.shape[0]
    p_home = np.tril(M, -1).sum()   # i > j  -> gana local
    p_draw = np.trace(M)            # i == j -> empate
    p_away = np.triu(M, 1).sum()    # i < j  -> gana visitante
    best, best_ev = None, -1.0
    for i in range(n):
        for j in range(n):
            p_sign = p_home if i > j else (p_draw if i == j else p_away)
            ev = 5 * M[i, j] + 2 * (p_sign - M[i, j])  # exacto=5, signo (no exacto)=2
            if ev > best_ev:
                best_ev, best = ev, (i, j)
    return best, best_ev, (p_home, p_draw, p_away)


def confidence(ph, pd, pa):
    p = max(ph, pd, pa)
    return "Alta" if p >= 0.62 else ("Media" if p >= 0.45 else "Baja")


def run():
    rows = []
    for g, h, a, jor, host in FIXTURE:
        lh, la = lambdas(h, a, host)
        M = score_matrix(lh, la)
        (i, j), ev, (ph, pd, pa) = best_prode_score(M)
        rows.append(dict(grupo=g, jor=jor, local=h, visit=a,
                         lh=round(lh, 2), la=round(la, 2),
                         pick=f"{i}-{j}", pexact=round(M[i, j], 4),
                         ph=round(ph, 3), pd=round(pd, 3), pa=round(pa, 3),
                         ev=round(ev, 3), conf=confidence(ph, pd, pa)))
    return sorted(rows, key=lambda x: (x["grupo"], x["jor"]))


def main():
    rows = run()
    out = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "picks.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out, "picks.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print(f"{'GR':<2} {'J':<1} {'PARTIDO':<34} {'xG':<11} {'1/X/2':<16} {'PICK':<5} {'P.ex':<6} {'EV':<5} CONF")
    print("-" * 92)
    cur = None
    for r in rows:
        if r["grupo"] != cur:
            cur = r["grupo"]
            print(f"\n— GRUPO {cur}: {', '.join(GRUPOS[cur])}")
        part = f"{r['local']} vs {r['visit']}"
        xg = f"{r['lh']:.2f}-{r['la']:.2f}"
        sgn = f"{r['ph']*100:3.0f}/{r['pd']*100:3.0f}/{r['pa']*100:3.0f}%"
        print(f"{r['grupo']:<2} {r['jor']:<1} {part:<34} {xg:<11} {sgn:<16} "
              f"{r['pick']:<5} {r['pexact']*100:4.1f}% {r['ev']:.2f}  {r['conf']}")
    print(f"\nTotal: {len(rows)} partidos. Salida en output/picks.csv y output/picks.json")


if __name__ == "__main__":
    main()
