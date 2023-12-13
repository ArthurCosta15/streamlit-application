import streamlit as st


def show_general(df_filtered):
    st.subheader('Tabela de Nível Geral')
    st.table(df_filtered[['name', 'release_date', 'user_review', 'month', 'year']])
