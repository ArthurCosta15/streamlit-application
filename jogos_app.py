import streamlit as st
import pandas as pd

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
st.sidebar.markdown("## Projeto Final - Arthur César Ferreira Costa")
st.markdown("### Análise de Dados de Jogos em diferentes PLATAFORMAS!")

# Filtros na página principal

# Filtro para a plataforma
platform_options = ['Todos'] + list(df['platform'].unique())
selected_platforms = st.sidebar.multiselect('Selecione a(s) plataforma(s)', platform_options)

# Filtro para o ano de lançamento
release_year = st.sidebar.slider('Selecione o ano de lançamento', min(df['year']), max(df['year']))

# Filtro para o mês de lançamento
months = {'Todos': 0, 'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
release_month = st.sidebar.selectbox('Selecione o mês de lançamento', list(months.keys()))

# Convertendo o mês selecionado para número
release_month = months[release_month]

# Filtrar dados
if 'Todos' in selected_platforms:
    df_filtered = df  # Não aplicar filtro de plataforma se 'Todos' estiver selecionado
else:
    df_filtered = df[df['platform'].isin(selected_platforms)]

df_filtered = df_filtered.query('year == @release_year & (month == @release_month | @release_month == 0)')

# Variáveis para rastrear o estado dos botões
show_general = st.sidebar.button('Nível Geral')
show_semi_detailed = st.sidebar.button('Nível Semi-Detalhado')
show_detailed = st.sidebar.button('Nível Detalhado')

# Mostrar a tabela correspondente ao botão clicado
if show_general:
    st.subheader('Tabela de Nível Geral')
    st.table(df_filtered[['name', 'release_date', 'user_review', 'month', 'year']])

if show_semi_detailed:
    st.subheader('Tabela de Nível Semi-Detalhado')
    df_semi_detailed = df_filtered[['name', 'platform', 'release_date', 'user_review', 'month', 'year']].drop_duplicates()
    st.table(df_semi_detailed)

if show_detailed:
    st.subheader('Tabela de Nível Detalhado')
    # Filtro para selecionar um jogo
    game = st.selectbox('Selecione um jogo', df_filtered['name'].unique())

    # Filtrar dados para o jogo selecionado
    df_game = df_filtered[df_filtered['name'] == game]

    # Verificar se o DataFrame para o jogo não está vazio
    if not df_game.empty:
        # Exibir informações do jogo
        st.table(df_game[['platform', 'release_date', 'user_review']])
    else:
        st.warning("Nenhum jogo selecionado.")
