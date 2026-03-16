import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa USP", layout="wide")

# Dicionário de coordenadas dos estados brasileiros para o mapa
COORDENADAS_ESTADOS = {
    'São Paulo (SP)': [-23.5505, -46.6333],
    'Pará (PA)': [-1.4558, -48.4902],
    'Rio de Janeiro (RJ)': [-22.9068, -43.1729],
    'Minas Gerais (MG)': [-19.9167, -43.9345],
    'Distrito Federal (DF)': [-15.7801, -47.9292],
    # Você pode adicionar outros estados conforme a necessidade
}

@st.cache_data
def carregar_dados(aba):
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba}"
    return pd.read_csv(url)

# --- CABEÇALHO ---
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")
    st.write("Informações detalhadas sobre o progresso e dados da aba Dashboard.")

# --- SEÇÃO 1: DASHBOARD ---
with st.container():
    st.write("---")
    st.subheader("📊 Dados Consolidados (Dashboard)")
    df_dash = carregar_dados("Dashboard")
    st.dataframe(df_dash, use_container_width=True, hide_index=True)

# --- SEÇÃO 2: MAPA DE ATUAÇÃO ---
with st.container():
    st.write("---")
    st.subheader("🗺️ Localização das Empresas")
    
    try:
        # Carrega a aba de respostas
        df_respostas = carregar_dados("Respostas ao formulário 1")
        
        # Pega a coluna M pelo nome exato que aparece na imagem
        coluna_localizacao = "Em qual estado a empresa atua principalmen"
        
        # Se o pandas ler o nome truncado ou diferente, podemos usar o índice 12 (coluna M)
        estados_serie = df_respostas.iloc[:, 12].dropna()

        # Lista para armazenar as coordenadas encontradas
        pontos_mapa = []

        for estado in estados_serie:
            if estado in COORDENADAS_ESTADOS:
                pontos_mapa.append(COORDENADAS_ESTADOS[estado])
        
        if pontos_mapa:
            # Cria DataFrame necessário para o st.map
            df_mapa = pd.DataFrame(pontos_mapa, columns=['lat', 'lon'])
            st.map(df_mapa)
        else:
            st.info("Nenhum estado mapeado encontrado na coluna M.")
            
    except Exception as e:
        st.error(f"Erro ao gerar o mapa: {e}")

# --- RODAPÉ ---
with st.container():
    st.write("---")
    st.caption("Sistema Pesquisa USP | Dados integrados via Google Sheets")
