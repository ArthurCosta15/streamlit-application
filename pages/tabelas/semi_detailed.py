import streamlit as st

def show_semi_detailed(df_filtered):
    st.subheader('Tabela de Nível Semi-Detalhado')
    df_semi_detailed = df_filtered[['name', 'platform', 'release_date', 'user_review', 'month', 'year']].drop_duplicates()
    st.table(df_semi_detailed)