from app.utils.carregar_dados import carregar_dados
import streamlit as st
import plotly.express as px
import pandas as pd

def exibir():
    st.title("Preço do Petróleo Brent")
    df = carregar_dados()
    if df.empty:
        st.warning("Base de dados não encontrada ou vazia.")
        return
    # Carregar métricas e previsões já calculadas
    resultados = pd.read_csv('data/resultados_modelos.csv')
    previsoes = pd.read_csv('data/previsoes_modelos.csv')

    # Melhor modelo pelo menor RMSE
    melhor_idx = resultados['RMSE'].idxmin()
    melhor_modelo = resultados.loc[melhor_idx, 'Modelo']
    metricas = {'rmse': resultados.loc[melhor_idx, 'RMSE'], 'mae': resultados.loc[melhor_idx, 'MAE']}
    previsoes_df = previsoes[previsoes['modelo'] == melhor_modelo].copy()
    previsoes_df['data'] = pd.to_datetime(previsoes_df['data'])
    
    # Última data e preço mais recente
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values('data')
    ultima_data = df['data'].iloc[-1]
    preco_atual = df[df['data'] == ultima_data]['preco'].iloc[0]

    # prox_dia_data: dia após a maior data do df real
    prox_dia_data = (ultima_data + pd.Timedelta(days=1)).strftime("%d/%m/%Y")
    # Valor previsto para o dia seguinte (primeiro dia da previsão FUTURA, tipo == 'futuro' e data > ultima_data)
    previsoes_futuras = previsoes_df[(previsoes_df['tipo'] == 'futuro') & (previsoes_df['data'] > ultima_data)].copy()
    if not previsoes_futuras.empty:
        prox_dia_valor = previsoes_futuras['preco_previsto'].iloc[0]
    else:
        prox_dia_valor = None
    preco_atual = df['preco'].iloc[-1]
    
    try:
        prox_dia_valor_float = float(prox_dia_valor) if prox_dia_valor is not None else None
        preco_atual_float = float(preco_atual)
    except Exception:
        prox_dia_valor_float = None
        preco_atual_float = None
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Último Preço", f"${preco_atual_float:.2f}" if preco_atual_float is not None else "N/A")
    with col2:
        variacao = df['preco'].pct_change().iloc[-1] * 100
        st.metric("Variação diária", f"{variacao:.2f}%", delta_color="inverse")
    with col3:
        if prox_dia_valor_float is not None and preco_atual_float is not None and preco_atual_float != 0:
            variacao_prevista = ((prox_dia_valor_float / preco_atual_float) - 1) * 100
            delta = f"{variacao_prevista:.2f}%" if variacao_prevista != 0 else None
            delta_color = "normal" if variacao_prevista >= 0 else "inverse"
            st.metric(
                f"Previsão ({prox_dia_data})",
                f"${prox_dia_valor_float:.2f}",
                delta=delta,
                delta_color=delta_color
            )
    with col4:
        st.metric("Última atualização", ultima_data.strftime("%d/%m/%Y"))
    st.subheader("Previsão para o Próximo Dia")
    col1, col2 = st.columns(2)
    with col1:
        if prox_dia_valor_float is not None and preco_atual_float is not None and preco_atual_float != 0:
            variacao_prevista = ((prox_dia_valor_float / preco_atual_float) - 1) * 100
            delta = f"{variacao_prevista:.2f}%" if variacao_prevista != 0 else None
            delta_color = "normal" if variacao_prevista >= 0 else "inverse"
            st.metric(
                f"Preço Previsto para {prox_dia_data}",
                f"${prox_dia_valor_float:.2f}",
                delta=delta,
                delta_color=delta_color
            )
    with col2:
        if melhor_modelo:
            st.metric("Modelo Utilizado", melhor_modelo)
            tooltip = f"RMSE: {metricas['rmse']:.2f}, MAE: {metricas['mae']:.2f}"
            st.info(f"Métricas do modelo: {tooltip}")
    fig = px.line(df, x="data", y="preco", title="Histórico de Preço do Petróleo")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Previsão para os Próximos Dias")
    
    # Gráfico dos últimos 30 dias
    historico = df[['data', 'preco']].copy()
    historico = historico.rename(columns={"data": "Data", "preco": "Preço"})
    historico['Tipo'] = 'Histórico'
    historico_ultimos_30 = historico.sort_values('Data').iloc[-30:]
    previsoes_plot = previsoes_df[previsoes_df['tipo'] == 'futuro'][['data', 'preco_previsto']].copy()
    previsoes_plot = previsoes_plot.rename(columns={"data": "Data", "preco_previsto": "Preço"})
    previsoes_plot['Tipo'] = 'Previsão'
    df_plot = pd.concat([historico_ultimos_30, previsoes_plot], ignore_index=True)
    fig_linha = px.line(
        df_plot,
        x="Data",
        y="Preço",
        color="Tipo",
        title=f"Histórico e Previsão de Preço do Petróleo (Modelo: {melhor_modelo})",
        labels={"Data": "Data", "Preço": "Preço ($)", "Tipo": "Série"}
    )
    st.plotly_chart(fig_linha, use_container_width=True)
    previsoes_df['data_str'] = previsoes_df['data'].dt.strftime('%d/%m/%Y')

exibir()