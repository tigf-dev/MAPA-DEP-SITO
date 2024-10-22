import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuração da API Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds_path = r"C:\\Users\\Plus\\Documents\\ARQUIVOS PEDRO\\PROJETOS\\RELATÓRIO WHATSAPP\\compact-circlet-429712-t7-77e8a7c33b74.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# --- Carrega os dados da planilha ---
spreadsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1AZ2K-U1i-zyEeqsk42MQzBbrxxNhIPEEhFQ000kouqI/edit?gid=0"
)
worksheet = spreadsheet.worksheet("COLMEIA")
data = worksheet.get_all_records()

# Criação do DataFrame
df = pd.DataFrame(data)

# --- Exibir planilha completa ---
st.title("Sistema de Estoque - Mapeamento de Colmeias")
st.subheader("Visualização Completa da Planilha")
st.dataframe(df)

# --- Tabela estilo Batalha Naval ---
st.subheader("Visualização Estilo Batalha Naval")

# Criar uma tabela para a visualização estilo Batalha Naval
colmeias = df['Localização colmeia'].unique()  # Colunas são as localizações das colmeias
espacos = df['Localização espaços'].unique()  # Linhas são os espaços

# Criação da tabela de batalha naval
tabela_batalha = pd.DataFrame(index=espacos, columns=colmeias)

# Preencher a tabela com as informações
for _, row in df.iterrows():
    col = row['Localização colmeia']
    row_idx = row['Localização espaços']
    if col in tabela_batalha.columns and row_idx in tabela_batalha.index:
        if row['Descrição'] and row['Quantidade'] > 0:
            descricao = f"{row['Descrição']} ({row['Quantidade']})"
            tabela_batalha.at[row_idx, col] = descricao  # Simplesmente atribuir descrição

# Substituir NaN por "Vazio"
tabela_batalha.fillna("Vazio", inplace=True)

# Exibir a tabela de batalha naval
st.table(tabela_batalha)
