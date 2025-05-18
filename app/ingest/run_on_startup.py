import os
from app.utils.carregar_dados import carregar_dados
from app.model.modelos import lstm_pipeline, prophet_pipeline, xgboost_pipeline
import pandas as pd
from ipea_data import run_pipeline

def main():
    print("Iniciando a execução do aplicativo...")
    # Executar o pipeline de ingestão de dados primeiro
    print("Iniciando o processo de ingestão de dados...")
    try:
        run_pipeline()
        print("Ingestão de dados concluída com sucesso!")
    except Exception as e:
        print(f"Erro na ingestão de dados: {e}")
        
    # Verificar se os dados estão disponíveis após a ingestão
    df = carregar_dados()
    if df.empty:
        print("Dados não encontrados mesmo após a ingestão. Verificar o pipeline de dados.")
        return
    print(f"Dados carregados com sucesso. Total de registros: {len(df)}")

    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'])
        df = df.rename(columns={'data': 'Data', 'preco': 'Preço'})

    # Avaliação centralizada via modelos.py
    mae_lstm, rmse_lstm, lstm_df = lstm_pipeline(df, dias_futuros=10)
    mae_prophet, rmse_prophet, prophet_df = prophet_pipeline(df, dias_futuros=10)
    mae_xgb, rmse_xgb, xgb_df = xgboost_pipeline(df, dias_futuros=10)

    # Salvar resultados em CSV para uso rápido no Streamlit
    resultados = pd.DataFrame({
        'Modelo': ['LSTM', 'Prophet', 'XGBoost'],
        'MAE': [mae_lstm, mae_prophet, mae_xgb],
        'RMSE': [rmse_lstm, rmse_prophet, rmse_xgb]
    })
    resultados.to_csv('data/resultados_modelos.csv', index=False)
    print("Resultados dos modelos salvos em data/resultados_modelos.csv")

    # Salvar previsões dos dados de teste + próximos 10 dias para cada modelo
    previsoes = pd.concat([
        lstm_df,
        prophet_df,
        xgb_df
    ], ignore_index=True)
    previsoes.to_csv('data/previsoes_modelos.csv', index=False)
    print("Previsões dos modelos salvas em data/previsoes_modelos.csv")

if __name__ == "__main__":
    main()