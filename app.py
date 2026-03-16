import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração da página
st.set_page_config(page_title="Pesquisa USP", layout="wide")

COORDENADAS_ESTADOS = {
    'Acre (AC)': [-9.02, -70.81], 'Alagoas (AL)': [-9.57, -36.78], 'Amapá (AP)': [1.41, -51.77],
    'Amazonas (AM)': [-3.41, -65.85], 'Bahia (BA)': [-12.96, -38.51], 'Ceará (CE)': [-3.71, -38.54],
    'Distrito Federal (DF)': [-15.78, -47.93], 'Espírito Santo (ES)': [-19.19, -40.34], 'Goiás (GO)': [-16.64, -49.31],
    'Maranhão (MA)': [-2.55, -44.30], 'Mato Grosso (MT)': [-12.64, -55.42], 'Mato Grosso do Sul (MS)': [-20.51, -54.54],
    'Minas Gerais (MG)': [-18.10, -44.38], 'Pará (PA)': [-1.45, -48.48], 'Paraíba (PB)': [-7.06, -35.55],
    'Paraná (PR)': [-24.89, -51.55], 'Pernambuco (PE)': [-8.28, -35.07], 'Piauí (PI)': [-7.73, -42.73],
    'Rio de Janeiro (RJ)': [-22.84, -43.15], 'Rio Grande do Norte (RN)': [-5.22, -36.52], 'Rio Grande do Sul (RS)': [-30.01, -51.22],
    'Rondônia (RO)': [-11.50, -63.58], 'Roraima (RR)': [2.73, -62.07], 'Santa Catarina (SC)': [-27.24, -50.21],
    'São Paulo (SP)': [-23.55, -46.63], 'Sergipe (SE)': [-10.90, -37.07], 'Tocantins (TO)': [-10.17, -48.33]
}

@st.cache_data
def carregar_dados(nome_aba, skip_rows=0):
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    aba_codificada = quote(nome_aba)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba_codificada}"
    # Pulamos as linhas iniciais se necessário para evitar que o título vire dado
    return pd.read_csv(url, skiprows=skip_rows)

# --- CABEÇALHO ---
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")

# --- SEÇÃO 1: INFORMAÇÕES GERAIS ---
with st.container():
    st.write("---")
    st.subheader("📋 Informações Gerais")
    try:
        # Aqui está o truque: pulamos a 1ª linha (o título) para o pandas ler os dados certos
        df_dash = carregar_dados("Dashboard", skip_rows=1)
        
        # Agora pegamos as colunas certas (A e C da planilha original)
        # O pandas verá a Coluna A como índice 0 e a Coluna C como índice 2
        df_final = df_dash.iloc[0:5, [0, 2]].copy()
        
        # Nomeamos as colunas manualmente para ficar bonito no Streamlit
        df_final.columns = ["Qual o nível atual de adoção de Gêmeos Digitais", "%"]
        
        # st.table força o visual limpo, sem barras de rolagem estranhas
        st.table(df_final)
        
    except Exception as e:
        st.error(f"Erro ao organizar os dados: {e}")

# --- SEÇÃO 2: MAPA ---
with st.container():
    st.write("---")
    st.subheader("🗺️ Em qual estado a empresa atua principalmente")
    
    try:
        # Para a aba de respostas, não pulamos linhas para não perder o cabeçalho do Forms
        df_respostas = carregar_dados("Respostas ao formulário 1")
        estados_serie = df_respostas.iloc[:, 12].dropna()

        pontos_validos = []
        for estado in estados_serie:
            if estado in COORDENADAS_ESTADOS:
                pontos_validos.append(COORDENADAS_ESTADOS[estado])
        
        if pontos_validos:
            df_mapa = pd.DataFrame(pontos_validos, columns=['lat', 'lon'])
            st.map(df_mapa)
        else:
            st.info("Aguardando novas localizações.")
            
    except Exception as e:
        st.error(f"Erro no mapa: {e}")

with st.container():
    st.write("---")
    st.caption("© 2026 Pesquisa USP")
