# ─────── IMPORTAÇÕES E CONFIGURAÇÕES ───────
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

st.set_page_config(page_title="Painel MEI", layout="wide", page_icon="📊")

# ─────── FUNÇÕES AUXILIARES ───────
def baixar_serie_bacen(codigo_serie, nome_serie):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json'
    resposta = requests.get(url)
    dados = resposta.json()
    df = pd.DataFrame(dados)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'].str.replace(',', '.'), errors='coerce')
    df = df.rename(columns={'data': 'Date', 'valor': nome_serie})
    return df

def load_data():
    selic_df = baixar_serie_bacen(4390, 'SELIC')
    ipca_df = baixar_serie_bacen(433, 'IPCA')
    inad_df = baixar_serie_bacen(15885, 'Inadimplencia')
    df = selic_df.merge(ipca_df, on='Date').merge(inad_df, on='Date').dropna()
    df['Ano'] = df['Date'].dt.year
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    df['Mês'] = df['Date'].dt.month.map(meses)
    return df

def save_excel(df):
    relatorio = 'relatorio_mei.xlsx'
    if os.path.exists(relatorio):
        os.remove(relatorio)
    df.to_excel(relatorio, index=False)

# ─────── INTERFACE PRINCIPAL ───────
pagina = st.sidebar.radio("Menu", options=["Home", "Contabilidade"])

if pagina == "Home":
    st.title("📈 Painel Econômico Interativo para MEI")

    if st.button("🔄 Atualizar relatório agora"):
        df = load_data()
        save_excel(df)
        st.success("Relatório atualizado com sucesso!")
    else:
        df = load_data()

    ano_min, ano_max = st.slider("Selecione o período:", 2004, 2025, (2020, 2025))
    df = df[(df['Ano'] >= ano_min) & (df['Ano'] <= ano_max)]

    indicadores_disponiveis = ["SELIC", "IPCA", "Inadimplencia"]
    indicadores_selecionados = st.multiselect("Escolha os indicadores:", indicadores_disponiveis, default=indicadores_disponiveis)

    abas = st.tabs(["📊 Evolução", "📉 Comparação Anual", "📌 Correlação", "📆 Sazonalidade", "📊 Barras Combinadas", "🔮 Projeções Futuras"])

    with abas[0]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""💡 **Como interpretar?**
            - SELIC: Se acima de 10%, crédito é caro. Ideal para MEI: evite empréstimos.
            - IPCA: Acima de 5%? Reajuste preços mensalmente.
            - Inadimplência: Acima de 5%? Ofereça descontos para pagamento à vista.

            🔍 **Dica para MEI:** 
            Monitore meses em que a SELIC e o IPCA sobem juntos. São períodos críticos para ajustar estratégias de preço e estoque.""")
        for indicador in indicadores_selecionados:
            fig = px.line(df, x="Date", y=indicador, title=f"Evolução de {indicador}")
            st.plotly_chart(fig, use_container_width=True)

    with abas[1]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""💡 **O que analisar?**
            - Anos com IPCA alto: Custos operacionais aumentaram.
            - SELIC baixa: Boa hora para investir.
            - Inadimplência em alta: Exija entradas maiores.""")
        for indicador in indicadores_selecionados:
            media_anual = df.groupby("Ano")[indicador].mean().reset_index()
            fig = px.bar(media_anual, x="Ano", y=indicador, title=f"Média Anual de {indicador}")
            st.plotly_chart(fig, use_container_width=True)

    with abas[2]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("Mostra a relação entre dois indicadores. Correlações ajudam o MEI a entender como um indicador pode influenciar o outro.")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Eixo X", indicadores_disponiveis)
        with col2:
            y_axis = st.selectbox("Eixo Y", [i for i in indicadores_disponiveis if i != x_axis])
        fig = px.scatter(df, x=x_axis, y=y_axis, trendline="ols", title=f"Correlação entre {x_axis} e {y_axis}")
        st.plotly_chart(fig, use_container_width=True)

        correlacao = df[x_axis].corr(df[y_axis])
        st.markdown(f"📌 **Coeficiente de correlação**: `{correlacao:.2f}`")
        if correlacao > 0.7:
            nivel = "forte"
        elif correlacao > 0.4:
            nivel = "moderada"
        elif correlacao > 0.2:
            nivel = "fraca"
        else:
            nivel = "muito fraca"
        direcao = "direta" if correlacao > 0 else "inversa"
        st.info(f"A correlação entre {x_axis} e {y_axis} é **{nivel}** e **{direcao}**.")

    with abas[3]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("Comportamento médio mensal. Útil para planejamento de sazonalidade.")
        for indicador in indicadores_selecionados:
            sazonalidade = df.groupby("Mês")[indicador].mean().reindex([
                'Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
            ])
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=sazonalidade.values, theta=sazonalidade.index, fill='toself', name=indicador))
            fig.update_layout(title=f"Sazonalidade de {indicador}", polar=dict(radialaxis=dict(visible=True)))
            st.plotly_chart(fig, use_container_width=True)

    with abas[4]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("Visualize todos os indicadores juntos mês a mês.")
        df_barra = df[['Date'] + indicadores_disponiveis].copy()
        df_barra['AnoMes'] = df_barra['Date'].dt.to_period('M').astype(str)
        df_melt = df_barra.melt(id_vars="AnoMes", value_vars=indicadores_disponiveis, var_name="Indicador", value_name="Valor")
        fig = px.bar(df_melt, x="AnoMes", y="Valor", color="Indicador", title="Indicadores Combinados por Mês")
        st.plotly_chart(fig, use_container_width=True)

    with abas[5]:
        with st.expander("ℹ️ Projeção baseada no Relatório Focus"):
            st.markdown("""
        ### 📈 SELIC:
        - 2025: 12,50%
        - 2026: 10,50%
        - 2027–2028: 10,00%

        ### 💸 IPCA:
        - Queda gradual até 3,80% em 2028

        ### 📉 Inadimplência:
        - Pode continuar alta. Risco de exclusão do Simples Nacional se não regularizar.

        > 🧾 **Recomendação para MEI**: mantenha controle de fluxo de caixa e reavalie preços e formas de pagamento.
        """)

elif pagina == "Contabilidade":
    import streamlit_app
    streamlit_app.app() 