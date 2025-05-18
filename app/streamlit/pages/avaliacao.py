import streamlit as st
import pandas as pd
import numpy as np

# Carregar métricas já calculadas
resultados = pd.read_csv('data/resultados_modelos.csv')

melhor_mae = resultados.loc[resultados['MAE'].idxmin()]
melhor_rmse = resultados.loc[resultados['RMSE'].idxmin()]

st.subheader("Resumo das Métricas")
st.dataframe(resultados, use_container_width=True)

st.subheader("Melhor Modelo (MAE)")
st.success(f"{melhor_mae['Modelo']} com MAE = {melhor_mae['MAE']:.2f}")

st.subheader("Melhor Modelo (RMSE)")
st.success(f"{melhor_rmse['Modelo']} com RMSE = {melhor_rmse['RMSE']:.2f}")

st.info(f"Para prever os próximos 7 dias, recomenda-se utilizar o modelo {melhor_rmse['Modelo']}, pois apresentou o menor erro (RMSE) dentre os avaliados.")
