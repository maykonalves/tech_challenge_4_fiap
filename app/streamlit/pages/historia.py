import streamlit as st
import plotly.graph_objs as go
from app.utils.carregar_dados import carregar_dados

def plot_grafico_evolucao_preco_petroleo():
    def add_ponto_interesse(fig, ponto, text_index, label, cor):
        fig.add_trace(
            go.Scatter(
                x=[ponto.data.values[0]],
                y=[ponto.preco.values[0]],
                mode="markers",
                text=1,
                marker=dict(color=cor, size=10, line=dict(color="white", width=1)),
                name=label,
            )
        )
        fig.add_annotation(
            x=ponto.data.values[0],
            y=ponto.preco.values[0] + 15,
            text=text_index,
            showarrow=False,
            font=dict(color="white", size=18),
            bgcolor=cor,
            borderwidth=1,
            bordercolor="white",
            )

    df = carregar_dados()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df.data, y=df.preco, mode="lines", name="Preço do barril de petróleo")
    )
    add_ponto_interesse(
        fig, df.query('data == "2007-01-16"'), 1, "1. Ciclo especulativo (2007)"
    , "green")    
    add_ponto_interesse(
        fig, df.query('data == "2008-07-07"'), 2, "2. Crise financeira global (2008)"
    , "red")
    add_ponto_interesse(
        fig, df.query('data == "2014-06-01"'), 3, "3. OPEP mantém ritmo de produção (2014)"
    , "red")
    add_ponto_interesse(
        fig, df.query('data == "2015-05-15"'), 4, "4. Boom de Xisto (2015)"
    , "red")
    add_ponto_interesse(
        fig, df.query('data == "2020-01-30"'), 5, "5. Pandemia de COVID-19 (2020)"
    , "red")
    add_ponto_interesse(
        fig, df.query('data == "2022-02-01"'), 6, "6. Guerra Rússia-Ucrânia (2022)"
    , "green")
    add_ponto_interesse(
        fig, df.query('data == "2025-03-04"'), 7, "7. Guerras tarifárias (2025)"
    , "red")

    fig.update_layout(
        title="Evolução do preço do barril de petróleo Brent ao longo das decádas (1987 até hoje)",
        xaxis_title="Data",
        yaxis_title="Preço em US$",
        height=640,
        legend=dict(
            x=0,  # Move to the left
            y=1,
            xanchor="left",
            yanchor="top",
            font=dict(size=16),  # Aumenta o tamanho do texto da legenda
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

def mostrar_detalhes_eventos():
    st.header("Detalhes dos Eventos Históricos")
    
    tabs = st.tabs([
        "1. Ciclo especulativo (2007)", 
        "2. Crise financeira global (2008)", 
        "3. OPEP mantém produção (2014)", 
        "4. Boom de Xisto (2015)", 
        "5. Pandemia de COVID-19 (2020)", 
        "6. Guerra Rússia-Ucrânia (2022)",
        "7. Guerras tarifárias (2025)"
    ])
    
    with tabs[0]:
        st.subheader("Ciclo especulativo (2007)")
        st.markdown("""
        Em 2007, o mercado de petróleo experimentou uma forte alta especulativa, impulsionada por:
        
        - Aumento constante da demanda global, especialmente de economias emergentes como China e Índia
        - Capacidade limitada de produção e refino
        - Forte interesse de investidores especulativos no mercado de commodities
        - Tensões geopolíticas no Oriente Médio
        
        Isso levou o preço do petróleo a subir rapidamente, iniciando um ciclo que culminaria com preços recordes em 2008.
        """)
    
    with tabs[1]:
        st.subheader("Crise financeira global (2008)")
        st.markdown("""
        A crise financeira global de 2008 teve um impacto severo no mercado de petróleo:
        
        - Após atingir pico histórico próximo de US$147 em julho de 2008
        - Colapso do banco Lehman Brothers em setembro de 2008 desencadeou pânico nos mercados
        - Recessão global levou a uma queda abrupta na demanda por petróleo
        - Preços despencaram mais de 70% em poucos meses, chegando a menos de US$40
        
        Esta foi uma das quedas mais rápidas e acentuadas da história do petróleo, mostrando como fatores econômicos globais podem afetar drasticamente a commodity.
        """)
    
    with tabs[2]:
        st.subheader("OPEP mantém ritmo de produção (2014)")
        st.markdown("""
        Em novembro de 2014, a OPEP (Organização dos Países Exportadores de Petróleo) tomou uma decisão surpreendente:
        
        - Manter os níveis de produção apesar da queda nos preços globais
        - Estratégia liderada pela Arábia Saudita para defender participação de mercado
        - Tentativa de pressionar produtores de maior custo, especialmente os de xisto nos EUA
        - Resultado: preços continuaram caindo, de US$100+ para menos de US$50
        
        Esta decisão marcou uma mudança fundamental na política da OPEP, que historicamente costumava cortar produção para sustentar preços.
        """)
    
    with tabs[3]:
        st.subheader("Boom de Xisto (2015)")
        st.markdown("""
        A revolução do xisto nos EUA transformou o mercado global de petróleo:
        
        - Novas tecnologias como fracking e perfuração horizontal viabilizaram exploração de enormes reservas
        - Produção americana saltou de ~5 milhões de barris/dia em 2008 para mais de 9 milhões em 2015
        - Eficiência crescente reduziu custos de produção, tornando produtores resilientes mesmo com preços baixos
        - EUA se tornaram um dos maiores produtores mundiais, reduzindo importações
        
        Este fenômeno alterou permanentemente o equilíbrio no mercado global de energia, reduzindo o poder da OPEP de controlar preços.
        """)
    
    with tabs[4]:
        st.subheader("Pandemia de COVID-19 (2020)")
        st.markdown("""
        A pandemia de COVID-19 causou um choque sem precedentes no mercado de petróleo:
        
        - Lockdowns globais e restrições de viagens reduziram dramaticamente a demanda
        - Em abril de 2020, os futuros de petróleo WTI chegaram a preços negativos (-US$37)
        - Produtores enfrentaram desafio de armazenamento com capacidade limitada
        - OPEP+ implementou cortes históricos de produção (9,7 milhões de barris/dia)
        
        Foi o maior choque de demanda na história do petróleo, demonstrando a vulnerabilidade do setor a crises de saúde global.
        """)
    
    with tabs[5]:
        st.subheader("Guerra Rússia-Ucrânia (2022)")
        st.markdown("""
        A invasão russa da Ucrânia em fevereiro de 2022 desestabilizou o mercado energético global:
        
        - Rússia é um dos maiores exportadores mundiais de petróleo e gás
        - Sanções ocidentais contra Rússia restringiram oferta e rotas de transporte
        - Preços dispararam acima de US$120 por barril em março de 2022
        - Países consumidores liberaram reservas estratégicas para tentar conter altas
        
        O conflito destacou a importância geopolítica do petróleo e a vulnerabilidade das cadeias globais de suprimento de energia durante conflitos internacionais.
        """)

    with tabs[6]:
        st.subheader("Guerras tarifárias (2025)")
        st.markdown("""
        A guerra tarifaria entre EUA e China teve um impacto significativo no mercado de petróleo:
        
        - Aumento das tarifas sobre produtos chineses levou a uma desaceleração econômica
        - Aumento da incerteza sobre a demanda global de petróleo
        - Preços do petróleo caíram devido a preocupações com a desaceleração econômica
        """)

def exibir():
    st.title("História do Petróleo Brent")

    with st.container():
        st.markdown(
            """
            Ao longo das décadas, uma série de eventos significativos, como guerras e revoluções, moldaram o contexto geopolítico global de suas respectivas eras. Esses acontecimentos desempenharam um papel crucial na flutuação dos preços da commodity do petróleo, uma vez que é uma peça fundamental na economia mundial.\n
            A seguir, serão detalhados 7 desses eventos cruciais, ordenados de forma cronológica, conforme a seguir:
            * 1. Ciclo especulativo (2007)
            * 2. Crise financeira global (2008)
            * 3. OPEP mantém ritmo de produção (2014)
            * 4. Boom de Xisto (2015)
            * 5. Pandemia de COVID-19 (2020)
            * 6. Guerra Rússia-Ucrânia (2022)
            * 7. Guerras tarifárias (2025)\n
        """
        )

        plot_grafico_evolucao_preco_petroleo()
        
        mostrar_detalhes_eventos()

exibir()