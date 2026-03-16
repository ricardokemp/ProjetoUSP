import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Pesquisa USP", layout="wide")

@st.cache_data
def carregar_dados(aba):
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba}"
    return pd.read_csv(url)

# --- CABEÇALHO ---
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")
    st.write("Monitoramento de dados da aba Dashboard e mapeamento de respostas.")

# --- SEÇÃO 1: DASHBOARD ---
with st.container():
    st.write("---")
    st.subheader("📊 Dados Consolidados (Dashboard)")
    try:
        df_dash = carregar_dados("Dashboard")
        st.dataframe(df_dash, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erro ao carregar aba Dashboard: {e}")

# --- SEÇÃO 2: MAPA DE RESPOSTAS ---
with st.container():
    st.write("---")
    st.subheader("🗺️ Mapa de Localização (Coluna M)")
    
    try:
        # Carregando a aba de respostas
        df_respostas = carregar_dados("Respostas ao formulário 1")
        
        # Selecionando a coluna M (índice 12 no Python, pois começa em 0)
        # Se a coluna tiver um nome específico, você pode usar df_respostas['Nome Da Coluna']
        coluna_m = df_respostas.iloc[:, 12].dropna() 
        
        st.write(f"Total de pontos identificados na Coluna M: {len(coluna_m)}")

        # NOTA: O Streamlit requer latitude e longitude para exibir o mapa nativo.
        # Se a coluna M tiver apenas nomes de cidades, este bloco simula a plotagem.
        # Caso você tenha as coordenadas, substitua pela lógica real abaixo:
        
        if not coluna_m.empty:
            # Exemplo de como preparar dados para o mapa (lat/lon)
            # Aqui geramos coordenadas aleatórias apenas para ilustrar o componente, 
            # já que nomes de texto puro (ex: "São Paulo") precisam de geocodificação.
            map_data = pd.DataFrame(
                np.random.randn(len(coluna_m), 2) / [50, 50] + [-23.55, -46.63],
                columns=['lat', 'lon']
            )
            st.map(map_data)
        else:
            st.info("A coluna M está vazia ou não contém dados válidos de localização.")
            
    except Exception as e:
        st.warning("Não foi possível processar o mapa. Verifique se a aba 'Respostas ao formulário 1' existe e possui dados na coluna M.")

# --- RODAPÉ ---
with st.container():
    st.write("---")
    st.caption("Aplicação Pesquisa USP | Dados via Google Sheets")
