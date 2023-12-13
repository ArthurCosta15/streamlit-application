import streamlit as st
import pandas as pd
import pages.general as page_geral
import pages.semi_detailed as page_semi_detailed
import pages.detailed as page_detailed

# Carregando os dados
@st.cache_data
def load_data():
    with st.spinner('Carregando dados...'):
        df = pd.read_csv('video_games.csv')
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['month'] = df['release_date'].dt.month
        df['year'] = df['release_date'].dt.year
    return df

df = load_data()

# Título
st.markdown("### Análise de Dados de Jogos em diferentes PLATAFORMAS!")
st.sidebar.markdown("## Projeto Final - Arthur César Ferreira Costa")
st.sidebar.title('Menu')
pages = st.sidebar.selectbox('Níveis', ['Nível Geral', 'Nível Semi-Detalhado', 'Nível Detalhado'])

# Filtro para a plataforma
platform_options = ['Todos'] + list(df['platform'].unique())
selected_platforms = st.multiselect('Selecione a(s) plataforma(s)', platform_options)

# Filtro para o ano de lançamento
release_year = st.slider('Selecione o ano de lançamento', min(df['year']), max(df['year']))

# Filtro para o mês de lançamento
months = {'Todos': 0, 'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
release_month = st.selectbox('Selecione o mês de lançamento', list(months.keys()))

# Convertendo o mês selecionado para número
release_month = months[release_month]

# Filtrar dados
if 'Todos' in selected_platforms:
    df_filtered = df  # Não aplicar filtro de plataforma se 'Todos' estiver selecionado
else:
    df_filtered = df[df['platform'].isin(selected_platforms)]

df_filtered = df_filtered.query('year == @release_year & (month == @release_month | @release_month == 0)')


if pages == 'Nível Geral':
    page_geral.show_general(df_filtered)

if pages == 'Nível Semi-Detalhado':
    page_semi_detailed.show_semi_detailed(df_filtered)

if pages == 'Nível Detalhado':
    page_detailed.show_detailed(df_filtered)
