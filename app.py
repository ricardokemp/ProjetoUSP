import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração da página
st.set_page_config(page_title="Pesquisa USP", layout="wide")

# Coordenadas para o mapa
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
    # A codificação correta evita o erro de 'ascii' que apareceu no seu Streamlit
    aba_codificada = quote(nome_aba)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={aba_codificada}"
    return pd.read_csv(url)

# --- CABEÇALHO ---
st.subheader("Portal de Indicadores")
st.title("Pesquisa USP")

# --- SEÇÃO: INFORMAÇÕES GERAIS ---
st.write("---")
st.subheader("📋 Informações Gerais")

try:
    df_aba_info = carregar_dados("Informações Gerais")
    
    # 1. Gêmeos Digitais (A e C)
    df_gemeos = df_aba_info.iloc[0:5, [0, 2]].copy()
    df_gemeos.columns = ["Qual o nível atual de adoção de Gêmeos Digitais", "%"]
    st.table(df_gemeos)

    # 2. Setor de Atuação (D e F)
    df_setor = df_aba_info.iloc[0:7, [3, 5]].copy()
    df_setor.columns = ["Qual o setor de atuação principal da empresa", "%"]
    st.table(df_setor)

    # 3. Tamanho da Empresa (G e I)
    df_tamanho = df_aba_info.iloc[0:4, [6, 8]].copy()
    df_tamanho.columns = ["Qual o tamanho aproximado da empresa", "%"]
    st.table(df_tamanho)

    # 4. Estados de Atuação (J e L)
    # Pegamos todas as linhas da lista de estados (até a 27, que cobre todos os estados + Outros)
    df_local = df_aba_info.iloc[0:28, [9, 11]].copy()
    df_local.columns = ["Em qual estado a empresa atua principalmente", "%"]
    
    # Filtramos para mostrar apenas estados que possuem participação (> 0%) ou nomes válidos
    # Isso evita mostrar uma lista gigante de 0% se você preferir algo mais enxuto
    st.table(df_local)
    
except Exception as e:
    st.error(f"Erro ao processar as tabelas: {e}")

# --- SEÇÃO: MAPA ---
st.write("---")
st.subheader("🗺️ Localização Geográfica (Respostas Individuais)")

try:
    df_respostas = carregar_dados("Respostas ao formulário 1")
    # Coluna M (índice 12) contém o estado selecionado no formulário
    estados_respondidos = df_respostas.iloc[:, 12].dropna()

    pontos_mapa = []
    for estado in estados_respondidos:
        if estado in COORDENADAS_ESTADOS:
            pontos_mapa.append(COORDENADAS_ESTADOS[estado])
    
    if pontos_mapa:
        df_mapa = pd.DataFrame(pontos_mapa, columns=['lat', 'lon'])
        st.map(df_mapa)
    else:
        st.info("Aguardando dados de localização para preencher o mapa.")
        
except Exception as e:
    st.error(f"Erro ao gerar o mapa: {e}")

st.write("---")
st.caption("© 2026 Pesquisa USP - Dados extraídos em tempo real.")
