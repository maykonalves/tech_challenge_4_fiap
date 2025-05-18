import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.carregar_dados import carregar_dados

def exibir():
    st.title("Análise Exploratória (EDA)")

    df = carregar_dados()

    if df.empty:
        st.warning("Base de dados não encontrada.")
        return

    st.subheader("Estatísticas Descritivas")
    df_describe = df.describe()
    count = df_describe.loc["count"]["preco"]
    mean = df_describe.loc["mean"]["preco"]
    std = df_describe.loc["std"]["preco"]
    min = df_describe.loc["min"]["preco"]
    max = df_describe.loc["max"]["preco"]

    st.write(
        f"A base de dados possui {int(count)} registros. "
        f"A média dos preços é {mean:.2f}, com um desvio padrão de {std:.2f}. "
        f"O menor valor registrado foi {min:.2f} e o maior foi {max:.2f}."
    )
    col1, _ = st.columns([1, 2])
    with col1:
        st.dataframe(df['preco'].describe())

    st.subheader("Distribuição dos Preços")
    st.write("O histograma abaixo mostra como os preços estão distribuídos na base de dados, permitindo identificar padrões, assimetrias e possíveis outliers.")
    fig = px.histogram(df, x='preco', nbins=30, marginal="box", title="Distribuição dos Preços")
    st.plotly_chart(fig)

    st.subheader("Boxplot dos Preços")
    st.write("O boxplot abaixo fornece uma visão clara dos quartis e possíveis outliers nos dados de preços.")
    fig2 = px.box(df, y='preco', title="Boxplot dos Preços")
    st.plotly_chart(fig2)

exibir()