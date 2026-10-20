"""
Artefacto A03-B (Bloque B): Gantt con línea base y real superpuestas
y cálculo de la desviación por actividad, desde un CSV.

Uso:
    python gantt_linea_base.py cronograma.csv
Salidas:
    gantt_linea_base.png   -> Gantt (barra gris = línea base, barra de color = real)
    desviaciones.csv       -> desviación de inicio, fin y duración por actividad
"""
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLS = ["id", "actividad", "responsable", "inicio_base", "fin_base",
        "inicio_real", "fin_real", "avance_pct"]


def cargar(ruta):
    df = pd.read_csv(ruta)
    faltan = [c for c in COLS if c not in df.columns]
    if faltan:
        raise SystemExit(f"Faltan columnas en el CSV: {faltan}")
    for c in ["inicio_base", "fin_base", "inicio_real", "fin_real"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    if df[["inicio_base", "fin_base"]].isna().any().any():
        raise SystemExit("Todas las actividades necesitan inicio_base y fin_base.")
    return df


def desviaciones(df):
    out = df[["id", "actividad", "responsable"]].copy()
    out["dur_base_dias"] = (df["fin_base"] - df["inicio_base"]).dt.days + 1
    out["dur_real_dias"] = (df["fin_real"] - df["inicio_real"]).dt.days + 1
    out["desv_inicio_dias"] = (df["inicio_real"] - df["inicio_base"]).dt.days
    out["desv_fin_dias"] = (df["fin_real"] - df["fin_base"]).dt.days
    out["desv_duracion_dias"] = out["dur_real_dias"] - out["dur_base_dias"]
    out["estado"] = out["desv_fin_dias"].apply(
        lambda d: "sin dato real" if pd.isna(d)
        else ("a tiempo/adelantada" if d <= 0 else "atrasada"))
    return out


def graficar(df, salida="gantt_linea_base.png"):
    fig, ax = plt.subplots(figsize=(11, 0.45 * len(df) + 1.5))
    for i, r in df.iterrows():
        y = len(df) - i
        ini = r["inicio_base"]
        dur = (r["fin_base"] - ini).days + 1
        ax.barh(y + 0.18, dur, left=ini, height=0.32, color="#b0b0b0",
                label="Línea base" if i == 0 else None)
        if pd.notna(r["inicio_real"]) and pd.notna(r["fin_real"]):
            d2 = (r["fin_real"] - r["inicio_real"]).days + 1
            atras = r["fin_real"] > r["fin_base"]
            ax.barh(y - 0.18, d2, left=r["inicio_real"], height=0.32,
                    color="#d1495b" if atras else "#2e86ab",
                    label="Real (atrasada)" if (atras and i == 0) else None)
    ax.set_yticks([len(df) - i for i in range(len(df))])
    ax.set_yticklabels([f"{r['id']} {r['actividad']}" for _, r in df.iterrows()],
                       fontsize=8)
    ax.xaxis_date()
    fig.autofmt_xdate()
    ax.set_title("Gantt: línea base (gris) vs. real (azul = a tiempo, rojo = atrasada)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(salida, dpi=150)
    return salida


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "datos_demo.csv"
    df = cargar(ruta)
    dev = desviaciones(df)
    dev.to_csv("desviaciones.csv", index=False)
    print(dev.to_string(index=False))
    print("Gráfico:", graficar(df))
