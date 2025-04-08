import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Message', layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('base_dashboard_message.csv', parse_dates=['Data'])
    return df

df = load_data()

# Estilo dark
dark_style = '''
<style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-color: #0e1117;
    }
</style>
'''
st.markdown(dark_style, unsafe_allow_html=True)

st.title('📊 Dashboard de Campanhas - Message (Dark Mode)')
st.markdown('### Visão consolidada de performance mês a mês')

# Filtro de mês
meses_disponiveis = df['Mês'].unique()
mes_selecionado = st.selectbox("📅 Selecione o mês", sorted(meses_disponiveis))

df_mes = df[df['Mês'] == mes_selecionado]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("✉️ Enviado", f"{int(df_mes['Enviado'].sum()):,}".replace(',', '.'))
col2.metric("📬 Entregue", f"{int(df_mes['Entregue'].sum()):,}".replace(',', '.'))
col3.metric("📖 Aberto", f"{int(df_mes['Aberto'].sum()):,}".replace(',', '.'))

# Gráfico de evolução dentro do mês
st.markdown("### 📈 Evolução dentro do mês")
fig = px.bar(df_mes, x="Data", y=["Enviado", "Entregue", "Aberto"], barmode="group", title="Volume por Dia")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Gráfico de taxas
st.markdown("### 📊 Taxas de Entrega e Abertura (%)")
fig2 = px.bar(df_mes, x="Data", y=["PercEntregueXEnviado", "PercAbertoXEntregue"], barmode="group",
              title="Eficiência por Dia", color_discrete_sequence=["#00cc96", "#636efa"])
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Tabela detalhada
st.markdown("### 📄 Detalhes do Mês Selecionado")
st.dataframe(df_mes, use_container_width=True)
