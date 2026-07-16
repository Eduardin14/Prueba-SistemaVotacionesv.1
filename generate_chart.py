"""
Genera una grafica de barras (Candidatos vs Votos) usando pandas + matplotlib,
leyendo el estado actual de la base de datos.

Uso: python generate_chart.py
Salida: statistics_chart.png en la raiz del proyecto.
"""

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # backend sin GUI, apto para servidores/CI
import matplotlib.pyplot as plt

from src.database.config import SessionLocal
from src.entities.Candidate import Candidate


def build_dataframe() -> pd.DataFrame:
    """Consulta los candidatos y arma un DataFrame de pandas con sus votos."""
    db = SessionLocal()
    try:
        candidates = db.query(Candidate).all()
        data = [{"Candidato": c.name, "Votos": c.votes} for c in candidates]
    finally:
        db.close()

    df = pd.DataFrame(data, columns=["Candidato", "Votos"])
    if df.empty:
        df = pd.DataFrame({"Candidato": [], "Votos": []})
    return df.sort_values("Votos", ascending=False)


def generate_chart(output_path: str = "statistics_chart.png") -> str:
    """Genera y guarda la grafica de barras: Candidatos (eje X) vs Votos (eje Y)."""
    df = build_dataframe()

    plt.figure(figsize=(8, 5))
    if df.empty:
        plt.text(0.5, 0.5, "Aun no hay votos registrados", ha="center", va="center")
    else:
        plt.bar(df["Candidato"], df["Votos"], color="#4C72B0")
        for i, v in enumerate(df["Votos"]):
            plt.text(i, v + 0.05, str(v), ha="center", fontweight="bold")

    plt.title("Resultado de la votacion")
    plt.xlabel("Candidatos")
    plt.ylabel("Votos")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Grafica guardada en: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_chart()
