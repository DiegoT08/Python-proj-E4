# visualize_histogramme.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Dataset import load_data, select_numeric

# Dossier de sortie pour les images
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

def plot_loyer_distribution(df):
    """Histogramme du loyer prédictif."""
    plt.figure(figsize=(8,5))
    plt.hist(df["loypredm2"].dropna(), bins=50, edgecolor='black')
    plt.title("Distribution des loyers prédits par commune")
    plt.xlabel("Loyer prédit (€/m²)")
    plt.ylabel("Nombre de communes")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "hist_loypredm2.png"))
    plt.close()
    print("✅ Histogramme des loyers enregistré.")

def plot_boxplot_typpred(df):
    """Boxplot des loyers par type de maille."""
    if "TYPPRED" not in df.columns:
        print("Colonne TYPPRED non trouvée, boxplot ignoré.")
        return
    plt.figure(figsize=(8,5))
    df.boxplot(column="loypredm2", by="TYPPRED", grid=False)
    plt.title("Variation des loyers prédits selon le type de maille")
    plt.suptitle("")
    plt.xlabel("Type de maille")
    plt.ylabel("Loyer prédit (€/m²)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "boxplot_typpred.png"))
    plt.close()
    print("✅ Boxplot par type de maille enregistré.")

def plot_correlation(df):
    """Matrice de corrélation pour les colonnes numériques."""
    numeric_df = select_numeric(df)
    if numeric_df.shape[1] < 2:
        print("Pas assez de colonnes numériques pour corrélation.")
        return
    corr = numeric_df.corr()
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1)
    plt.title("Matrice de corrélation des variables numériques")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "corr_matrix.png"))
    plt.close()
    print("✅ Matrice de corrélation enregistrée.")

def main():
    df = load_data()
    plot_loyer_distribution(df)
    plot_boxplot_typpred(df)
    plot_correlation(df)
    print(f"✅ Toutes les figures sauvegardées dans {OUT_DIR}")

if __name__ == "__main__":
    main()