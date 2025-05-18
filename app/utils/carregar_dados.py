import os
import pandas as pd

def carregar_dados():
    caminho = "data/ipeadata_series.csv"
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        return df
    return pd.DataFrame()