
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Message', layout='wide')

# Estilo visual
st.markdown("""
    <style>
        body { background-color: #fafafa; font-family: 'Segoe UI', sans-serif; }
        .block-container { padding-top: 2rem; }
        h1, h2, h3 { color: #0A4C95; }
        .stMetric { border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px; background-color: #ffffff; }
        .stButton > button { background-color: #0A4C95; color: white; border-radius: 6px; padding: 0.4rem 1rem; }
        .stDataFrame { border: 1px solid #ddd; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# LOGO
st.image("message_logotipo.png", width=160)
st.title("📊 Dashboard de Performance - Message")

@st.cache_data
def load_data():
    return pd.read_csv("base_dashboard_message.csv", parse_dates=["Data"])

df = load_data()

# CLIENTES TOP 20% FATURAMENTO (baseado no total enviado)
st.header("🏆 Top Clientes - Representam 20% do Total de Envio")
df_total = df.groupby("NC")["Enviado"].sum().reset_index().sort_values(by="Enviado", ascending=False)
df_total["Perc_Acumulado"] = df_total["Enviado"].cumsum() / df_total["Enviado"].sum()
top_20 = df_total[df_total["Perc_Acumulado"] <= 0.2]
st.dataframe(top_20, use_container_width=True)

# FILTRO MULTI-CLIENTE
st.header("🎯 Filtro por Cliente(s)")
clientes_disponiveis = sorted(df["NC"].dropna().unique())
clientes_selecionados = st.multiselect("Selecione os clientes", options=clientes_disponiveis, default=clientes_disponiveis)

df_filtrado = df[df["NC"].isin(clientes_selecionados)]

# KPIs
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

st.markdown("---")
st.info(f"📌 Clientes selecionados: **{', '.join(clientes_selecionados[:5])}{'...' if len(clientes_selecionados) > 5 else ''}**")

# GRÁFICOS
st.subheader("📈 Evolução das Métricas (Clientes)")
fig = px.line(df_filtrado, x="Data", y=["Enviado", "Entregue", "Aberto"], markers=True, color='NC')
fig.update_layout(legend_title_text='Métrica por Cliente', template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Taxas de Entrega e Abertura (%)")
fig2 = px.bar(df_filtrado, x="Data", y=["PercEntregueXEnviado", "PercAbertoXEntregue"], barmode="group", color='NC')
fig2.update_layout(template='plotly_white')
st.plotly_chart(fig2, use_container_width=True)

# TABELA E DOWNLOAD
st.subheader("📄 Tabela Filtrada por Cliente")
st.dataframe(df_filtrado, use_container_width=True)

csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar dados filtrados (.csv)", csv, "dados_filtrados_clientes.csv", "text/csv")
