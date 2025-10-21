# ...existing code...
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "pred-mai-mef-dhup.csv"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} introuvable. Copiez le CSV dans le dossier data/")
    df = pd.read_csv(path, low_memory=False)
    return df

def summary(df):
    print("Shape:", df.shape)
    print("\nColonnes et types:\n", df.dtypes)
    print("\nAperçu:\n", df.head())
    print("\nStatistiques descriptives:\n", df.describe(include='all').T)
    miss = df.isna().sum()
    print("\nValeurs manquantes par colonne:\n", miss[miss>0])

def try_parse_dates(df):
    # tenter de reconnaître une colonne date
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower() or "jour" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"Colonne convertie en datetime: {col}")
            except Exception:
                pass
    return df

def plot_numeric_distributions(df, out_dir=OUT_DIR, max_plots=8):
    num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num:
        print("Aucune colonne numérique détectée.")
        return
    n = min(len(num), max_plots)
    for i, col in enumerate(num[:n], 1):
        plt.figure(figsize=(6,4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(col)
        fname = os.path.join(out_dir, f"hist_{col}.png")
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        print("Saved", fname)

def plot_correlation(df, out_dir=OUT_DIR):
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2:
        print("Pas assez de colonnes numériques pour corrélation.")
        return
    corr = num.corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1)
    plt.title("Matrice de corrélation")
    fname = os.path.join(out_dir, "corr_matrix.png")
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    print("Saved", fname)

def plot_time_series_if_possible(df, out_dir=OUT_DIR):
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if date_cols and num_cols:
        dcol = date_cols[0]
        vcol = num_cols[0]
        df_sorted = df.dropna(subset=[dcol, vcol]).sort_values(dcol)
        plt.figure(figsize=(10,4))
        plt.plot(df_sorted[dcol], df_sorted[vcol], marker='.', linestyle='-')
        plt.xlabel(dcol); plt.ylabel(vcol)
        plt.title(f"{vcol} over {dcol}")
        fname = os.path.join(out_dir, f"time_{vcol}_by_{dcol}.png")
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        print("Saved", fname)
    else:
        print("Aucune série temporelle détectable (pas de colonne date ou numérique).")

def main():
    df = load_data(DATA_PATH)
    summary(df)
    df = try_parse_dates(df)
    summary(df)  # rapide re-check si date convertie
    plot_numeric_distributions(df)
    plot_correlation(df)
    plot_time_series_if_possible(df)
    print("Exploration terminée. Figures dans", OUT_DIR)

if __name__ == "__main__":
    main()
# ...existing code...