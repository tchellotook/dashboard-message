
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Message - Campanhas', layout='wide')

@st.cache_data
def load_data():
    return pd.read_csv('base_dashboard_message.csv', parse_dates=['Data'])

df = load_data()

st.title('📊 Dashboard de Performance de Campanhas - Message')
st.markdown('Este painel mostra os principais indicadores de envio, entrega e abertura de campanhas mês a mês.')

col1, col2, col3 = st.columns(3)
col1.metric("Total Enviado", f"{df['Enviado'].sum():,.0f}")
col2.metric("Total Entregue", f"{df['Entregue'].sum():,.0f}")
col3.metric("Total Aberto", f"{df['Aberto'].sum():,.0f}")

st.subheader("📈 Evolução Mensal das Métricas")
fig = px.line(df, x="Data", y=["Enviado", "Entregue", "Aberto"], markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Taxas de Entrega e Abertura (%)")
fig2 = px.bar(df, x="Data", y=["PercEntregueXEnviado", "PercAbertoXEntregue"], barmode="group")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🧮 Tabela Detalhada")
st.dataframe(df, use_container_width=True)
