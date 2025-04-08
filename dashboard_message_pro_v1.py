
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Message', layout='wide')

# LOGO
st.image("message_logotipo.png", width=160)
st.title("📊 Dashboard de Performance - Message")
st.markdown("Este painel mostra os principais indicadores de envios, entregas e aberturas das campanhas de comunicação.")

# Carregamento de dados
@st.cache_data
def load_data():
    return pd.read_csv("base_dashboard_message.csv", parse_dates=["Data"])

df = load_data()

# Filtro de múltiplos meses
meses_disponiveis = sorted(df['Mês'].unique())
meses_selecionados = st.multiselect("📅 Selecione os meses", options=meses_disponiveis, default=meses_disponiveis)

df_filtrado = df[df['Mês'].isin(meses_selecionados)]

# KPIs e insights
total_enviado = df_filtrado['Enviado'].sum()
total_entregue = df_filtrado['Entregue'].sum()
total_aberto = df_filtrado['Aberto'].sum()
taxa_entrega = (total_entregue / total_enviado) * 100 if total_enviado > 0 else 0
taxa_abertura = (total_aberto / total_entregue) * 100 if total_entregue > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("✉️ Total Enviado", f"{int(total_enviado):,}".replace(',', '.'))
col2.metric("📬 Total Entregue", f"{int(total_entregue):,}".replace(',', '.'))
col3.metric("📖 Total Aberto", f"{int(total_aberto):,}".replace(',', '.'))
col4.metric("📈 % Entrega", f"{taxa_entrega:.2f}%")
col5.metric("📊 % Abertura", f"{taxa_abertura:.2f}%")

# Insights automáticos
st.info(f"📌 Taxa média de entrega: **{taxa_entrega:.2f}%** | Taxa média de abertura: **{taxa_abertura:.2f}%**")

# Gráficos
st.subheader("📈 Evolução das Métricas")
fig = px.line(df_filtrado, x="Data", y=["Enviado", "Entregue", "Aberto"], markers=True)
fig.update_layout(legend_title_text='Métrica')
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Taxas de Entrega e Abertura (%)")
fig2 = px.bar(df_filtrado, x="Data", y=["PercEntregueXEnviado", "PercAbertoXEntregue"], barmode="group",
              labels={"value": "%", "variable": "Indicador"})
st.plotly_chart(fig2, use_container_width=True)

# Tabela + Download
st.subheader("📄 Tabela Detalhada")
st.dataframe(df_filtrado, use_container_width=True)

csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar dados filtrados (.csv)", csv, "dados_filtrados.csv", "text/csv")
