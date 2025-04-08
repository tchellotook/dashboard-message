
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Message (Debug)', layout='wide')

st.title("🔧 Dashboard de Campanhas - Modo Debug")
st.info("Iniciando o carregamento dos dados...")

try:
    df = pd.read_csv('base_dashboard_message.csv', parse_dates=['Data'])
    st.success("✅ Dados carregados com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar o CSV: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ O dataframe está vazio!")
    st.stop()

st.info("Configurando interface...")

meses_disponiveis = df['Mês'].unique()
mes_selecionado = st.selectbox("📅 Selecione o mês", sorted(meses_disponiveis))

df_mes = df[df['Mês'] == mes_selecionado]

col1, col2, col3 = st.columns(3)
col1.metric("✉️ Enviado", f"{int(df_mes['Enviado'].sum()):,}".replace(',', '.'))
col2.metric("📬 Entregue", f"{int(df_mes['Entregue'].sum()):,}".replace(',', '.'))
col3.metric("📖 Aberto", f"{int(df_mes['Aberto'].sum()):,}".replace(',', '.'))

st.subheader("📈 Evolução do Mês")
try:
    fig = px.bar(df_mes, x="Data", y=["Enviado", "Entregue", "Aberto"], barmode="group")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao gerar gráfico de barras: {e}")

st.subheader("📊 Taxas de Entrega e Abertura")
try:
    fig2 = px.bar(df_mes, x="Data", y=["PercEntregueXEnviado", "PercAbertoXEntregue"], barmode="group")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)
except Exception as e:
    st.error(f"Erro ao gerar gráfico de taxas: {e}")

st.subheader("📄 Tabela detalhada")
st.dataframe(df_mes, use_container_width=True)
