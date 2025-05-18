import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_data(url):
    """
    Obtém dados de preço do petróleo do site IPEA.
    """
    # Obter HTML da página
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Localizar tabela principal
    table = soup.find('table', {'id': 'grd_DXMainTable'})
    if not table:
        raise ValueError("Tabela não encontrada na página")

    # Extrair cabeçalhos
    header_row = table.find('tr', {'id': 'grd_DXHeadersRow0'})
    headers = [header.text.strip() for header in header_row.find_all('td')] if header_row else []

    # Extrair dados
    data = []
    rows = table.find_all('tr', {'id': lambda x: x and x.startswith('grd_DXDataRow')})
    for row in rows:
        cols = row.find_all('td')
        if cols:
            data.append([col.text.strip() for col in cols])

    # Validar dados
    if not (data and headers):
        raise ValueError("Dados ou cabeçalhos não encontrados")
    
    return pd.DataFrame(data, columns=headers[:2])

def process_data(df):
    """
    Limpa e formata os dados obtidos.
    """
    # Renomear colunas
    df.columns = ['data', 'preco']

    # Converter preços para valores numéricos
    df['preco'] = pd.to_numeric(
        df['preco'].str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True),
        errors='coerce'
    ).round(2)

    # Converter datas para formato datetime
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', dayfirst=True).dt.date

    # Remover linhas com valores ausentes
    df.dropna(inplace=True)

    return df

def save_data(df, output_csv):
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Table processed and saved to {output_csv}")

def run_pipeline():
    """
    Executa o pipeline completo: obtenção, processamento e salvamento dos dados.
    """
    url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"
    output_csv = 'data/ipeadata_series.csv'

    df = fetch_data(url)
    df = process_data(df)
    save_data(df, output_csv)