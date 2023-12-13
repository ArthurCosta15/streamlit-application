import streamlit as st

def show_detailed(df_filtered):
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
