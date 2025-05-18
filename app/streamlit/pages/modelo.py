import streamlit as st
import pandas as pd
import numpy as np

st.markdown("""
Esta página apresenta um comparativo entre três modelos de previsão do preço do petróleo: **LSTM**, **Prophet** e **XGBoost**. 

Cada aba traz um resumo do modelo, suas métricas de desempenho (MAE e RMSE), as previsões para os próximos 7 dias e um gráfico comparativo entre os valores reais e previstos nos últimos 30 dias. Use esta análise para identificar qual modelo melhor se adapta ao comportamento recente da série temporal.
""")

# Carregar métricas e previsões já calculadas
resultados = pd.read_csv('data/resultados_modelos.csv')
previsoes = pd.read_csv('data/previsoes_modelos.csv')
previsoes['data'] = pd.to_datetime(previsoes['data'])

abas = st.tabs(["LSTM", "Prophet", "XGBoost"])

for i, modelo in enumerate(["LSTM", "Prophet", "XGBoost"]):
    with abas[i]:
        st.header(modelo)
        if modelo == "LSTM":
            st.markdown("""
            O modelo **LSTM** (Long Short-Term Memory) é uma rede neural recorrente capaz de capturar padrões temporais complexos e dependências de longo prazo. É especialmente útil para séries temporais com não linearidades e sazonalidades.
            """)
        elif modelo == "Prophet":
            st.markdown("""
            O **Prophet** é um modelo aditivo desenvolvido pelo Facebook, projetado para lidar com séries temporais com forte sazonalidade e efeitos de feriados. É fácil de ajustar e interpretar, mas pode apresentar limitações em séries altamente voláteis.
            """)
        else:
            st.markdown("""
            O **XGBoost** é um modelo de aprendizado de máquina baseado em árvores de decisão, muito eficiente para séries temporais quando há engenharia de features adequada. Ele pode capturar padrões complexos e não lineares, sendo robusto a diferentes tipos de dados.
            """)
        metrica = resultados[resultados['Modelo'] == modelo].iloc[0]
        st.metric("MAE", f"{metrica['MAE']:.2f}")
        st.metric("RMSE", f"{metrica['RMSE']:.2f}")
        # Filtrar dados reais e previstos do modelo
        prev_modelo = previsoes[previsoes['modelo'] == modelo][['data', 'preco_real', 'preco_previsto']]
        # Plotar ambos os valores reais e previstos
        grafico = prev_modelo.set_index('data').sort_index()
        st.line_chart(grafico[['preco_real', 'preco_previsto']].rename(columns={
            'preco_real': 'Preço Real',
            'preco_previsto': 'Preço Previsto'
        }), use_container_width=True)
        st.caption("Comparação entre os valores reais dos últimos 30 dias e as previsões para os próximos 7 dias.")
        # Exibir tabela com valor real e previsto
        tabela = prev_modelo.rename(columns={
            'data': 'Data',
            'preco_real': 'Preço Real',
            'preco_previsto': 'Preço Previsto'
        })
        st.dataframe(tabela, use_container_width=True)
        st.markdown("---")