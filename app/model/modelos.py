import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input, Dropout
from prophet import Prophet
import tensorflow as tf
import random as python_random
from datetime import timedelta
import xgboost as xgb

def _filtrar_2023(df):
    df = df.copy()
    df['Data'] = pd.to_datetime(df['Data'])
    return df[df['Data'] >= pd.to_datetime('2023-01-01')].reset_index(drop=True)

def split_treino_teste(df, split=0.8):
    n = len(df)
    n_treino = int(n * split)
    df_treino = df.iloc[:n_treino].copy()
    df_teste = df.iloc[n_treino:].copy()
    return df_treino, df_teste

def lstm_pipeline(df, dias_futuros=10, janela=15, seed=33):
    df = _filtrar_2023(df)
    df = df.set_index('Data').asfreq('D')
    df['Preço'] = df['Preço'].interpolate(method='linear')
    df_treino, df_teste = split_treino_teste(df)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(df_treino['Preço'].values.reshape(-1, 1))
    # Treinamento
    X_train, y_train = [], []
    for i in range(janela, len(df_treino)):
        X_train.append(scaler.transform(df_treino['Preço'].values[i-janela:i].reshape(-1, 1)).flatten())
        y_train.append(scaler.transform([[df_treino['Preço'].values[i]]])[0, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    python_random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    model = Sequential()
    model.add(Input(shape=(janela, 1)))
    model.add(LSTM(50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=200, batch_size=16, verbose=0)
    # Previsão teste
    X_test = []
    y_true = df_teste['Preço'].values
    precos_full = np.concatenate([df_treino['Preço'].values, df_teste['Preço'].values])
    for i in range(len(df_teste)):
        start_idx = len(df_treino) + i - janela
        end_idx = len(df_treino) + i
        X_window = precos_full[start_idx:end_idx]
        X_test.append(scaler.transform(X_window.reshape(-1, 1)).flatten())
    X_test = np.array(X_test)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    previsoes_teste = model.predict(X_test)
    previsoes_teste = scaler.inverse_transform(previsoes_teste).flatten()
    datas_teste = df_teste.index.values
    df_teste_pred = pd.DataFrame({
        'data': datas_teste,
        'preco_real': y_true,
        'preco_previsto': previsoes_teste,
        'modelo': 'LSTM',
        'tipo': 'teste'
    })
    # Previsão futura
    df_future = df.copy()
    ultima_data = df_future.index.max()
    for _ in range(dias_futuros):
        nova_data = ultima_data + timedelta(days=1)
        ultimos_precos = df_future['Preço'].values[-janela:]
        X_novo = scaler.transform(ultimos_precos.reshape(-1, 1)).reshape(1, janela, 1)
        pred = model.predict(X_novo)[0][0]
        pred_real = scaler.inverse_transform([[pred]])[0, 0]
        df_future.loc[nova_data] = pred_real
        ultima_data = nova_data
    df_futuro = df_future.tail(dias_futuros).reset_index()[['Data', 'Preço']].copy()
    df_futuro = df_futuro.rename(columns={'Data': 'data', 'Preço': 'preco_previsto'})
    df_futuro['preco_real'] = np.nan
    df_futuro['modelo'] = 'LSTM'
    df_futuro['tipo'] = 'futuro'
    # Métricas
    y_true = df_teste['Preço'].values
    mae = mean_absolute_error(y_true, previsoes_teste)
    rmse = np.sqrt(mean_squared_error(y_true, previsoes_teste))
    return mae, rmse, pd.concat([df_teste_pred, df_futuro], ignore_index=True)

def prophet_pipeline(df, dias_futuros=10):
    df = _filtrar_2023(df)
    df = df.set_index('Data').asfreq('D')
    df['Preço'] = df['Preço'].interpolate(method='linear')
    df_treino, df_teste = split_treino_teste(df)
    modelo = Prophet()
    df_prophet = df_treino.reset_index().rename(columns={'Data': 'ds', 'Preço': 'y'})
    modelo.fit(df_prophet)
    # Previsão teste
    future = pd.DataFrame({'ds': df_teste.index.values})
    forecast = modelo.predict(future)
    y_pred = forecast['yhat'].values
    datas_teste = df_teste.index.values
    df_teste_pred = pd.DataFrame({
        'data': datas_teste,
        'preco_real': df_teste['Preço'].values,
        'preco_previsto': y_pred,
        'modelo': 'Prophet',
        'tipo': 'teste'
    })
    # Previsão futura
    ultima_data = df.index.max()
    future_futuro = pd.date_range(ultima_data + timedelta(days=1), periods=dias_futuros, freq='D')
    future_df = pd.DataFrame({'ds': future_futuro})
    forecast_futuro = modelo.predict(future_df)
    df_futuro = pd.DataFrame({
        'data': forecast_futuro['ds'],
        'preco_real': [np.nan]*dias_futuros,
        'preco_previsto': forecast_futuro['yhat'],
        'modelo': 'Prophet',
        'tipo': 'futuro'
    })
    # Métricas
    y_true = df_teste['Preço'].values
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return mae, rmse, pd.concat([df_teste_pred, df_futuro], ignore_index=True)

def xgboost_pipeline(df, dias_futuros=10, seed=33):
    """
    Pipeline de previsão usando XGBoost, seguindo a lógica do leo.ipynb, padronizando saída igual aos outros modelos.
    - Usa apenas dados a partir de 2023
    - Engenharia de features: lags, médias móveis, volatilidade, mês, ano, eventos
    - Split 80/20
    - Previsão para teste e para os próximos dias
    - Retorna DataFrame padronizado: data, preco_real, preco_previsto, modelo, tipo
    """
    df = _filtrar_2023(df)
    df = df.sort_values('Data').reset_index(drop=True)
    df = df.set_index('Data').asfreq('D').reset_index()
    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    df['Preço'] = df['Preço'].interpolate(method='linear')

    # Features
    df['lag_1'] = df['Preço'].shift(1)
    df['lag_7'] = df['Preço'].shift(7)
    df['lag_30'] = df['Preço'].shift(30)
    df['ma_7'] = df['Preço'].rolling(window=7).mean().fillna(0)
    df['ma_30'] = df['Preço'].rolling(window=30).mean().fillna(0)
    df['volatilidade_30d'] = df['Preço'].rolling(window=30).std().fillna(0)
    df['mes'] = df['Data'].dt.month
    df['ano'] = df['Data'].dt.year
    eventos = {
        'crise_2008': ('2008-09-15', '2009-12-31'),
        'pandemia_2020': ('2020-03-11', '2020-12-31'),
        'guerra_2022': ('2022-02-24', '2022-12-31'),
        'opec_2014': ('2014-06-01', '2015-12-31')
    }
    for evento, (inicio, fim) in eventos.items():
        df[evento] = (df['Data'] >= inicio) & (df['Data'] <= fim)
    df = df.dropna()

    features = ['lag_1', 'lag_7', 'lag_30', 'ma_7', 'ma_30', 'volatilidade_30d',
                'mes', 'ano', 'crise_2008', 'pandemia_2020', 'guerra_2022', 'opec_2014']

    # Split 80/20
    n = len(df)
    n_treino = int(n * 0.8)
    df_treino = df.iloc[:n_treino].copy()
    df_teste = df.iloc[n_treino:].copy()
    X_train = df_treino[features]
    y_train = df_treino['Preço']
    X_test = df_teste[features]
    y_test = df_teste['Preço']

    # Treinamento
    model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=seed)
    model.fit(X_train, y_train)

    # Previsão teste
    y_pred = model.predict(X_test)
    datas_teste = df_teste['Data'].values
    df_teste_pred = pd.DataFrame({
        'data': datas_teste,
        'preco_real': y_test.values,
        'preco_previsto': y_pred,
        'modelo': 'XGBoost',
        'tipo': 'teste'
    })

    # Previsão futura (recursiva)
    df_future = df.copy()
    ultima_data = df_future['Data'].max()
    previsoes_futuras = []
    for _ in range(dias_futuros):
        nova_data = ultima_data + timedelta(days=1)
        linha_atual = {
            'Data': nova_data,
            'lag_1': df_future.iloc[-1]['Preço'],
            'lag_7': df_future.iloc[-7]['Preço'] if len(df_future) >= 7 else df_future.iloc[-1]['Preço'],
            'lag_30': df_future.iloc[-30]['Preço'] if len(df_future) >= 30 else df_future.iloc[-1]['Preço'],
            'ma_7': df_future['Preço'].rolling(window=7).mean().iloc[-1],
            'ma_30': df_future['Preço'].rolling(window=30).mean().iloc[-1],
            'volatilidade_30d': df_future['Preço'].rolling(window=30).std().iloc[-1],
            'mes': nova_data.month,
            'ano': nova_data.year,
            'crise_2008': False,
            'pandemia_2020': False,
            'guerra_2022': False,
            'opec_2014': False
        }
        X_novo = pd.DataFrame([linha_atual])[features]
        previsao = model.predict(X_novo)[0]
        linha_atual['Preço'] = previsao
        previsoes_futuras.append(linha_atual)
        df_future = pd.concat([df_future, pd.DataFrame([linha_atual])], ignore_index=True)
        ultima_data = nova_data
    df_previsto = pd.DataFrame(previsoes_futuras)
    df_futuro = pd.DataFrame({
        'data': df_previsto['Data'],
        'preco_real': [np.nan]*dias_futuros,
        'preco_previsto': df_previsto['Preço'],
        'modelo': 'XGBoost',
        'tipo': 'futuro'
    })

    # Métricas
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return mae, rmse, pd.concat([df_teste_pred, df_futuro], ignore_index=True)