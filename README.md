# ⚽ PRODE Mundial 2026 — Predictor de marcadores con modelo Dixon-Coles

Un modelo estadístico que pronostica el marcador de los **72 partidos de la fase de grupos** del Mundial 2026, optimizado para un sistema de PRODE específico:

> **5 puntos** si acertás el marcador exacto · **2 puntos** si acertás solo el ganador (el signo 1/X/2).

La gracia no es predecir "el resultado más probable", sino el marcador que **maximiza los puntos esperados** bajo esas reglas. No siempre son lo mismo, y esa diferencia es la ventaja.

---

## 🎯 La idea en una frase

> En vez de jugar cada partido una vez con la intuición, lo "jugamos" miles de veces con la fuerza real de cada selección, anotamos con qué frecuencia sale cada marcador, y elegimos el que más puntos rinde según las reglas del PRODE.

---

## 🧠 Cómo funciona (sin tecnicismos)

Cuatro pasos:

1. **Fuerza de cada equipo.** Partimos del rating Elo de las 48 selecciones (un número que resume qué tan fuerte es cada una). Los valores vienen del laboratorio [DTAI de KU Leuven](https://dtai.cs.kuleuven.be/sports/), uno de los que mejor le pega históricamente, junto al supercomputador de Opta.

2. **De fuerza a goles.** La diferencia de Elo entre dos equipos se traduce en cuántos goles se espera que meta cada uno (lo que se llama *goles esperados* o `lambda`). Cuanto más grande la diferencia, más goles espera el favorito y menos el rival.

3. **El abanico de marcadores.** Con esos goles esperados construimos la probabilidad de **cada** resultado posible (0-0, 1-0, 2-1, etc.) usando un modelo de Poisson con la corrección **Dixon-Coles**, que ajusta los marcadores bajos —en el fútbol real hay más 0-0 y 1-1 de lo que un Poisson simple supondría—.

4. **La jugada óptima.** Acá está el diferencial. Para cada marcador candidato calculamos el **valor esperado de puntos del PRODE** y elegimos el que más rinde:

   ```
   EV(marcador) = 5 × P(ese marcador exacto) + 2 × P(acertar solo el signo)
   ```

   Por eso aparecen tantos 1-0 y 2-0: son los marcadores individuales más frecuentes en el fútbol de selecciones, así que capturan el +5 más seguido sin resignar el +2 del signo.

### 💡 Un hallazgo lindo del modelo

El modelo **casi nunca apuesta al empate**, ni siquiera en los partidos más parejos. No es un capricho: el signo "empate" rara vez supera el ~28-30% de probabilidad, mientras que siempre hay un favorito cuyo signo (ganar) es más probable. Apostar a un 1-0 del favorito rinde más puntos esperados que un 1-1. Lo dedujo la matemática, no nosotros.

---

## 📊 Resultados

Al correr el modelo se generan en `output/`:

- **`PRODE_Mundial_2026.xlsx`** — planilla lista para cargar (hoja *Pronósticos*), las predicciones *Especiales* (campeón, subcampeón, goleador) y una hoja de *Detalle técnico*.
- **`picks.csv`** y **`picks.json`** — los mismos datos en formato crudo.

### Predicciones especiales (óptimas por probabilidad)

| Pronóstico | Elección | Razón |
|---|---|---|
| Campeón | **España** | #1 en Opta (16,1%) y DTAI (24%), co-favorita de mercado |
| Subcampeón | **Francia** | Co-favorita a la final (+240); cuadro opuesto a España |
| Goleador | **Mbappé** | Favorito Bota de Oro (+600): '9' + penalista + recorrido largo |

---

## 🚀 Cómo correrlo

Necesitás Python 3.9+.

```bash
git clone https://github.com/NicoPicotto/prode-mundial-2026.git
cd prode-mundial-2026

# (opcional) entorno virtual
python -m venv .venv && source .venv/bin/activate   # en Windows: .venv\Scripts\activate

pip install -r requirements.txt

# 1) corré el modelo -> imprime la tabla y genera output/picks.{csv,json}
python src/model.py

# 2) generá el Excel -> output/PRODE_Mundial_2026.xlsx
python src/export_xlsx.py
```

> Nota: ejecutá los scripts desde la raíz del repo (`python src/model.py`). Importan `data.py` desde la carpeta `src/`.

---

## 🔧 Cómo adaptarlo (acá está la diversión)

Todo lo editable vive en **`src/data.py`**. No hace falta tocar el modelo.

### Simular una lesión o un cambio de forma
Bajale o subile el Elo a una selección. Por ejemplo, España sin Lamine Yamal:

```python
# en src/data.py
"Espana": 1945,   # antes 1979; le bajamos ~34 puntos por la baja de Yamal
```

Volvé a correr `python src/model.py` y vas a ver cómo el España 3-0 vs Cabo Verde puede pasar a 2-0.

### Cambiar las reglas del PRODE
Si tu PRODE paga distinto, editá la fórmula del valor esperado en `src/model.py`, función `best_prode_score`:

```python
ev = 5 * M[i, j] + 2 * (p_sign - M[i, j])
#    ^puntos exacto      ^puntos por signo
```

### Recalibrar el modelo
Los parámetros están arriba de `src/model.py`:

| Parámetro | Qué controla | Default |
|---|---|---|
| `MU` | goles totales esperados en un partido parejo | `2.60` |
| `BETA` | cuánto pesa la diferencia de Elo en los goles | `0.0019` |
| `RHO` | corrección Dixon-Coles de marcadores bajos | `-0.08` |
| `HOST_BONUS` | bonus de Elo al anfitrión local (MEX/USA/CAN) | `55` |

Subí `MU` y vas a ver más goleadas; subí `BETA` y los favoritos golearán más a los débiles.

---

## 📁 Estructura

```
prode-mundial-2026/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── src/
│   ├── data.py          # ratings Elo + fixture (editá acá)
│   ├── model.py         # el modelo Dixon-Coles + optimización del PRODE
│   └── export_xlsx.py   # genera la planilla en Excel
└── output/              # se genera al correr (picks.csv/json, xlsx)
```

---

## ⚠️ Advertencias honestas

- Es un modelo **probabilístico**: maximiza tus puntos *esperados*, no garantiza nada. El fútbol tiene varianza (por algo lo miramos).
- Los ratings Elo son **pre-torneo** y no "saben" de lesiones de último momento ni de cómo llega anímicamente cada equipo. Para eso está la edición manual de `data.py` y tu ojo futbolero.
- En eliminatorias este PRODE puntúa el resultado a los **90 minutos** (sin alargue ni penales). Este repo cubre solo la fase de grupos; extenderlo a la fase final es un buen próximo paso.

---

## 📚 Fuentes de datos

- Ratings Elo: [DTAI Sports Analytics Lab, KU Leuven](https://dtai.cs.kuleuven.be/sports/)
- Probabilidades de torneo y favoritos: [Opta / The Analyst](https://theanalyst.com/)
- Metodología: Dixon, M.J. & Coles, S.G. (1997), *Modelling Association Football Scores and Inefficiencies in the Football Betting Market*.

---

*Hecho por amor al fútbol y a los datos. Que gane el mejor pronóstico. 🏆*
