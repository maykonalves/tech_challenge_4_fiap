# Dashboard de Análise do Petróleo Brent

Este projeto apresenta um dashboard interativo para análise e previsão do preço do petróleo Brent, desenvolvido para o curso de pós-graduação da FIAP.

## Principais Funcionalidades

- Visualização interativa da série histórica de preços
- Análise de eventos geopolíticos e crises econômicas
- Modelos de previsão (XGBoost, Prophet e LSTM)
- Avaliação de performance dos modelos

## Como Executar

### Com Docker

Pré-requisitos: Docker e Docker Compose

```bash
# Iniciar a aplicação
docker-compose up
```

O dashboard estará disponível em: http://localhost:8501

### Com Streamlit Community Cloud

Este projeto está configurado para ser facilmente implantado na plataforma Streamlit Community Cloud:

1. Faça um fork deste repositório para sua conta GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Faça login com sua conta GitHub
4. Clique em "New app"
5. Selecione seu repositório e o arquivo `streamlit_app.py`
6. Clique em "Deploy!"

O app será automaticamente implantado e estará disponível em uma URL pública.