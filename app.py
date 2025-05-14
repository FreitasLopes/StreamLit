import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px
import os
import sys
import plotly.graph_objects as go

# titulo de incio
st.set_page_config(page_title="Análise MEI", layout="wide", page_icon="📊")
st.title("📈 Painel Econômico para MEI")

# Função para baixar séries do Bacen
def baixar_serie_bacen(codigo_serie, nome_serie):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json'
    resposta = requests.get(url)
    dados = resposta.json()
    df = pd.DataFrame(dados)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'].str.replace(',', '.'), errors='coerce')
    df = df.rename(columns={'data': 'Date', 'valor': nome_serie})
    return df

# Cache de 1 hora
#@st.cache_data(ttl=3600)
def load_data():
    selic_df = baixar_serie_bacen(4390, 'SELIC')
    ipca_df = baixar_serie_bacen(433, 'IPCA')
    inad_df = baixar_serie_bacen(15885, 'Inadimplencia')
    
    df = selic_df.merge(ipca_df, on='Date', how='inner')
    df = df.merge(inad_df, on='Date', how='inner')
    df = df.dropna()
    df['Ano'] = df['Date'].dt.year
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    df['Mês'] = df['Date'].dt.month.map(meses)
    return df
def clean_file(df, relatorio = 'relatorio.xlsx'):
    if os.path.exists(relatorio):
        os.remove(relatorio)
    df.to_excel(relatorio, index=False)

# Botão para atualizar e salvar Excel
if st.button("🔄 Atualizar dados agora"):
    df_atualizado = load_data()
    df_atualizado.to_excel("relatorio.xlsx", index=False)
    clean_file(df_atualizado)
    st.success("Dados atualizados com sucesso!")

# Carrega os dados
df = load_data()

# Filtros
st.subheader("🔍 Filtros")
ano_min, ano_max = st.slider(
    "Selecione o período:",
    min_value=2004,
    max_value=2025,
    value=(2020, 2025)
)

indicador = st.radio(
    "Indicador principal:",
    ["IPCA", "SELIC", "Inadimplencia"],
    horizontal=True
)

df_filtrado = df[(df['Ano'] >= ano_min) & (df['Ano'] <= ano_max)]

# Layout principal
col1, col2 = st.columns([3, 1])

with col1:
    if not df_filtrado.empty:
        fig = px.area(
            df_filtrado,
            x="Date",
            y=indicador,
            title=f"Comportamento do {indicador} ({ano_min}-{ano_max})",
            labels={"Date": "", indicador: "Valor (%)"},
            color_discrete_sequence=["#4B9AC7"]
        )
        fig.update_layout(
            hovermode="x",
            plot_bgcolor="white",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para o período selecionado")

with col2:
    if not df_filtrado.empty:
        ultimo_valor = df_filtrado[indicador].iloc[-1]
        variacao = (ultimo_valor - df_filtrado[indicador].iloc[0]) / df_filtrado[indicador].iloc[0] * 100
        st.metric(
            label="Valor Atual",
            value=f"{ultimo_valor:.2f}%",
            delta=f"{variacao:.1f}% (variação total)"
        )
        st.markdown("### 📉 Nível de Atenção")
        if (indicador == "IPCA" and ultimo_valor > 0.7) or \
           (indicador == "SELIC" and ultimo_valor > 1.0) or \
           (indicador == "Inadimplencia" and ultimo_valor > 2.0):
            st.error("Alerta - Condição crítica para seu negócio!")
        else:
            st.success("Situação estável")
    else:
        st.warning("Selecione um período válido")

# Gráficos Complementares
if not df_filtrado.empty:
    st.subheader("📌 Entenda as Relações")
    tab1, tab2, tab3 = st.tabs(["IPCA vs Inadimplência", "Sazonalidade", "Comparação Anual"])

    with tab1:
        try:
            fig = px.scatter(
                df_filtrado,
                x="IPCA",
                y="Inadimplencia",
                trendline="lowess",
                title="Como a Inflação Afeta a Inadimplência",
                color_discrete_sequence=["#FF6B6B"]
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {str(e)}")

    with tab2:
        radar_df = df_filtrado.groupby("Mês")[indicador].mean().reset_index()
        radar_df['Mês'] = pd.Categorical(radar_df['Mês'], categories=[
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ], ordered=True)
        radar_df = radar_df.sort_values("Mês")

       

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
    r=radar_df[indicador],
    theta=radar_df["Mês"],
    fill='toself',
    name=indicador,
    line_color='blue',
    hovertemplate='%{theta}<br>%{r:.2f}%<extra></extra>'
))


        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, radar_df[indicador].max() * 1.1])
            ),
            showlegend=False,
            title="Padrão Mensal (Radar Chart)"
        )

        st.plotly_chart(fig, use_container_width=True)



    with tab3:
        fig = px.bar(
            df_filtrado.groupby("Ano")[indicador].mean().reset_index(),
            x="Ano",
            y=indicador,
            title="Média Anual Comparativa",
            color=indicador,
            color_continuous_scale="Tealrose"
        )
        st.plotly_chart(fig, use_container_width=True)

# Dicas Contextuais
if not df_filtrado.empty:
    st.subheader("💡 O Que Fazer?")
    if indicador == "IPCA":
        st.markdown("""
        - **Acima de 0.5%:** Reajuste preços a cada 2 meses  
        - **Abaixo de 0.3%:** Mantenha margens competitivas
        """)
    elif indicador == "SELIC":
        st.markdown("""
        - **Acima de 1%:** Evite novos empréstimos  
        - **Abaixo de 0.8%:** Considere financiar equipamentos
        """)
    else:
        st.markdown("""
        - **Acima de 2%:** Exija entrada de 30%  
        - **Abaixo de 1.5%:** Ofereça condições especiais
        """)

st.caption("Fonte: Banco Central e IBGE | Dados atualizados em " + datetime.now().strftime("%d/%m/%Y"))


