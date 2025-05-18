import sys
import os
# Add the current directory to the path so we can import from app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Run setup first
from setup import setup
setup()

import streamlit as st

st.set_page_config(layout="wide")

pages = {
    "Petróleo Brent": [
        st.Page("app/streamlit/pages/home.py", title="Home"),
        st.Page("app/streamlit/pages/historia.py", title="Eventos Históricos")
    ],
    "Projeto": [
        st.Page("app/streamlit/pages/exploracao.py", title="Exploração de Dados"),
        st.Page("app/streamlit/pages/modelo.py", title="Modelo de Previsão"),
        st.Page("app/streamlit/pages/avaliacao.py", title="Avaliação do Modelo")
    ],
    "Sobre o Projeto": [
        st.Page("app/streamlit/pages/sobre.py", title="Sobre o Projeto")
    ]
}

pg = st.navigation(pages)
pg.run()