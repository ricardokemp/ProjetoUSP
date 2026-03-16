import streamlit as st
import pandas as pd

# Configuração da página seguindo seu padrão
st.set_page_config(page_title="Pesquisa USP")

# Função para carregar os dados com cache para não sobrecarregar a rede
@st.cache_data
def carregar_dados():
    # ID da planilha e nome da aba Dashboard
    sheet_id = "1zPn9qNa1EuuoDh1WAmTAPMb_qIPnxO3qchOWZ-z9wKk"
    sheet_name = "Dashboard"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    # Leitura direta do CSV gerado pelo Google Sheets
    tabela = pd.read_csv(url)
    return tabela

# Container de Cabeçalho
with st.container():
    st.subheader("Portal de Indicadores")
    st.title("Pesquisa USP")
    st.write("Informações detalhadas sobre o progresso e dados da aba Dashboard.")
    st.write("Desenvolvido para acompanhamento acadêmico e institucional.")

# Container de Filtros e Gráficos
with st.container():
    st.write("---")
    
    # Carregamento dos dados
    dados = carregar_dados()
    
    # Seletor de período (ajustado para filtrar as linhas da planilha)
    opcoes_periodo = ["7 Dias", "15 Dias", "30 Dias", "Tudo"]
    selecao = st.selectbox("Selecione o período de visualização", opcoes_periodo)
    
    # Lógica de filtro baseada na seleção
    if selecao != "Tudo":
        num_linhas = int(selecao.replace(" Dias", ""))
        dados_filtrados = dados.tail(num_linhas)
    else:
        dados_filtrados = dados

    # Exibição dos dados em formato de tabela interativa
    st.write("### Visualização dos Dados")
    st.dataframe(dados_filtrados, use_container_width=True)

    # Exemplo de gráfico de área (ajuste as colunas 'Data' e 'Valor' conforme sua planilha)
    # Se sua planilha tiver colunas com esses nomes, o gráfico abaixo funcionará:
    if "Data" in dados_filtrados.columns:
        st.write("### Evolução Temporal")
        st.area_chart(dados_filtrados, x="Data")