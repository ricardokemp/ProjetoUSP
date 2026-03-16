import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Pesquisa USP")

# Função para carregar os dados com cache
@st.cache_data
def carregar_dados():
    # ID da planilha e nome da aba Dashboard
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    sheet_name = "Dashboard"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    # Leitura dos dados
    tabela = pd.read_csv(url)
    return tabela

# Container de Cabeçalho
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")
    st.write("Informações detalhadas sobre o progresso e dados da aba Dashboard.")
    st.write("Dados atualizados em tempo real conforme a planilha do Google Sheets.")

# Container de Exibição de Dados
with st.container():
    st.write("---")
    
    # Carregamento dos dados sem filtros de período
    dados = carregar_dados()
    
    st.write("### Visualização Geral dos Dados")
    # Exibição da tabela completa
    st.dataframe(dados, use_container_width=True, hide_index=True)

    # Verificação simples para exibir gráfico caso existam colunas compatíveis
    if not dados.empty:
        st.write("---")
        st.subheader("Análise Visual")
        # O Streamlit tentará plotar colunas numéricas automaticamente se você usar st.area_chart(dados)
        # Ou você pode especificar colunas: st.area_chart(dados, x="Coluna_X", y="Coluna_Y")
        st.line_chart(dados)

# Rodapé ou Link Externo (opcional, seguindo seu modelo)
with st.container():
    st.write("---")
    st.caption("Sistema de monitoramento acadêmico - Pesquisa USP")
