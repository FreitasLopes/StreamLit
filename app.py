import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Econômico", layout="centered")

st.title("📊 Dashboard Econômico")

#lendo os dados do arquivo
df = pd.read_excel("correlacaoIPCA.xlsx")
df["Ano"] = pd.to_datetime(df["Date"]).dt.year

# Ajuste os nomes com base nas colunas reais
indicadores = ["SELIC", "IPCA", "Inadimplencia"]

# ajustar pelas datas ou o tipo de grafico
st.sidebar.header("🎛️ Filtros")

indicador = st.sidebar.selectbox("indicadores", indicadores)
tipo_grafico = st.sidebar.radio("Tipo de gráfico", ["Linha", "Barra"])
ano_range = st.sidebar.slider("Filtrar por intervalo de anos", int(df["Ano"].min()), int(df["Ano"].max()), (2004, 2025))

# filtra pelo ano escolhido
df_filtrado = df[(df["Ano"] >= ano_range[0]) & (df["Ano"] <= ano_range[1])]

# graficp, no caso se quisermos colocar mais dados
st.subheader(f"{indicador} de {ano_range[0]} a {ano_range[1]}")

if tipo_grafico == "Linha":
    fig = px.line(df_filtrado, x="Ano", y=indicador, markers=True,
                  labels={"Ano": "Ano", indicador: indicador},
                  template="plotly_white", color_discrete_sequence=["#3B82F6"])
else:
    fig = px.bar(df_filtrado, x="Ano", y=indicador,
                 labels={"Ano": "Ano", indicador: indicador},
                 template="plotly_white", color_discrete_sequence=["#3B82F6"])

fig.update_layout(
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    font=dict(size=14),
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)
