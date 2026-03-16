import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa USP", layout="wide")

# Dicionário completo de coordenadas (Lat/Lon) dos estados brasileiros
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
def carregar_dados(nome_aba):
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    # O segredo está aqui: substituir espaços por %20 para a URL funcionar
    aba_codificada = nome_aba.replace(" ", "%20")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba_codificada}"
    return pd.read_csv(url)

# --- CABEÇALHO ---
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")
    st.write("Dados integrados da aba Dashboard e localização geográfica.")

# --- SEÇÃO 1: DASHBOARD ---
with st.container():
    st.write("---")
    st.subheader("📊 Dados Consolidados")
    df_dash = carregar_dados("Dashboard")
    st.dataframe(df_dash, use_container_width=True, hide_index=True)

# --- SEÇÃO 2: MAPA ---
with st.container():
    st.write("---")
    st.subheader("🗺️ Localização das Empresas")
    
    try:
        df_respostas = carregar_dados("Respostas ao formulário 1")
        # Coluna M é o índice 12
        estados_na_planilha = df_respostas.iloc[:, 12].dropna()

        pontos_validos = []
        for item in estados_na_planilha:
            if item in COORDENADAS_ESTADOS:
                pontos_validos.append(COORDENADAS_ESTADOS[item])
        
        if pontos_validos:
            map_df = pd.DataFrame(pontos_validos, columns=['lat', 'lon'])
            st.map(map_df)
        else:
            st.warning("Nenhum estado válido encontrado na coluna M para plotar no mapa.")
            
    except Exception as e:
        st.error(f"Erro ao processar o mapa: {e}")

with st.container():
    st.write("---")
    st.caption("Pesquisa USP 2026")
