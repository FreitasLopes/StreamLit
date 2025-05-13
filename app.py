import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configurações
st.set_page_config(page_title="Análise MEI", layout="wide", page_icon="📊")
st.title("📈 Painel Econômico Simplificado para MEI")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_excel("correlacaoIPCA.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ano'] = df['Date'].dt.year
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    df['Mês'] = df['Date'].dt.month.map(meses)
    return df

df = load_data()

# Filtros Superiores
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
    horizontal=True)

# Filtrar dados
df_filtrado = df[(df['Ano'] >= ano_min) & (df['Ano'] <= ano_max)]

# Layout Principal
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
        variacao = (df_filtrado[indicador].iloc[-1] - df_filtrado[indicador].iloc[0]) / df_filtrado[indicador].iloc[0] * 100
        
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
        pivot = df_filtrado.pivot_table(
            index="Mês",
            columns="Ano",
            values=indicador,
            aggfunc="mean"
        )
        meses_ordem = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        pivot = pivot.reindex(meses_ordem)
        
        fig = px.imshow(
            pivot,
            labels=dict(x="Ano", y="Mês", color=indicador),
            title="Padrão Mensal",
            color_continuous_scale="Blues"
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
