import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Selectbox na barra lateral para escolher o gráfico a ser exibido
selected_chart = st.sidebar.selectbox('Escolha um gráfico', ['Nenhum'] + ['Plataformas Mais Populares', 'Tendências ao Longo do Tempo', 'Distribuição de Avaliações de Usuários'])

# Verifica se uma opção válida foi selecionada
if selected_chart:
    # Gráficos
    if selected_chart == 'Plataformas Mais Populares':
        platform_counts = df_filtered['platform'].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(platform_counts.index, platform_counts.values, color='skyblue')
        plt.xlabel('Plataforma')
        plt.ylabel('Número de Jogos')
        plt.title('Número de Jogos por Plataforma')
        st.pyplot(plt)

    elif selected_chart == 'Tendências ao Longo do Tempo':
        monthly_trends = df_filtered.groupby(['year', 'month']).size().reset_index(name='count')
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_trends['year'].astype(str) + '-' + monthly_trends['month'].astype(str), monthly_trends['count'], marker='o')
        plt.xlabel('Data de Lançamento')
        plt.ylabel('Número de Jogos Lançados')
        plt.title('Tendências de Lançamento de Jogos ao Longo do Tempo')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif selected_chart == 'Distribuição de Avaliações de Usuários':
        user_review_distribution = df_filtered['user_review'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(user_review_distribution, labels=user_review_distribution.index, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightcoral', 'lightgreen', 'lightblue'])
        plt.title('Distribuição de Avaliações de Usuários')
        st.pyplot(plt)
