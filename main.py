import streamlit as st
import pandas as pd
import pages.tabelas.general as page_geral
import pages.tabelas.semi_detailed as page_semi_detailed
import pages.tabelas.detailed as page_detailed
from matplotlib import pyplot as plt

# Função para carregar dados
@st.cache_data
def load_data():
    with st.spinner('Carregando dados...'):
        df = pd.read_csv('video_games.csv')
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['month'] = df['release_date'].dt.month
        df['year'] = df['release_date'].dt.year
    return df

# Função para a página inicial com informações gerais
def show_main_page():

    # Seção de Descrição e Informações sobre o Base de Dados
    st.write(
        """
        ## Descrição da Base de Dados:

        Este conjunto de dados oferece uma visão geral detalhada de videogames em várias plataformas. Abrange uma ampla gama de informações, tornando-se um recurso valioso para a compreensão da evolução, popularidade e diversidade temática dos videogames. Ideal para análise de tendências de jogos, preferências de jogadores e dinâmicas específicas de plataforma, este conjunto de dados é uma ferramenta fundamental para pesquisadores, desenvolvedores de jogos e analistas de mercado.

        ## Colunas da Base de Dados:

        - **nome:** O título do videogame.
        - **plataforma:** A plataforma de jogos na qual o jogo está disponível (por exemplo, PlayStation, Xbox).
        - **release_date:** A data em que o jogo foi lançado.
        - **resumo:** Uma breve descrição ou resumo do enredo do jogo ou dos principais recursos.
        - **user_review:** Avaliação da avaliação do usuário, indicando a recepção e popularidade do jogo.

        ## Tamanho da Base de Dados:
        
        - 5 MB

        ## Link para Baixar o Base de Dados:
        
        [Download da Base de Dados](https://www.kaggle.com/datasets/maso0dahmed/video-games-data)
        """
    )

# Função para a página de filtros
def show_filter_page(df, pages):
    st.markdown("### Análise de Dados de Jogos em diferentes PLATAFORMAS!")
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

# Carregar dados
df = load_data()

# Lógica de roteamento
main_page = st.sidebar.radio('Páginas', ['Página Inicial', 'Página de Filtros'])

if main_page == 'Página Inicial':
    show_main_page()
else:
    show_filter_page(df, main_page)