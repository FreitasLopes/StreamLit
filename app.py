import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

st.set_page_config(page_title="Painel MEI", layout="wide", page_icon="HELPMEI (1).png")

CORES = {
    "SELIC": "#2980B9",   
    "IPCA": "#27AE60",     
    "Inadimplencia": "#E74C3C" 
}


#fazer a requisição para conseguir trazer os dados
def baixar_serie_bacen(codigo_serie, nome_serie):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json'
    resposta = requests.get(url)
    dados = resposta.json()
    df = pd.DataFrame(dados)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.rename(columns={'data': 'Date', 'valor': nome_serie})

    return df



def load_data():
    selic_df = baixar_serie_bacen(4189, 'SELIC') 
    ipca_df = baixar_serie_bacen(13522, 'IPCA')   
    inad_df = baixar_serie_bacen(15885, 'Inadimplencia')
    
    #juntar os dados
    df = selic_df.merge(ipca_df, on='Date').merge(inad_df, on='Date').dropna()    
    df['Ano'] = df['Date'].dt.year
    df['Mês'] = df['Date'].dt.month
    
    return df

def save_excel(df):
    relatorio = 'relatorio_mei.xlsx'
    if os.path.exists(relatorio):
        os.remove(relatorio)
    df.to_excel(relatorio, index=False)


#dados sobre esta baixo, estavel ou alto foram tirados do bacen
def classificar_indicador(nome, valor):
    if nome == "IPCA":
        if valor <= 1.5: 
            return "Muito Baixo"
        elif valor <= 4.5: 
            return "Estável"
        elif valor <= 6: 
            return "Alto"
        else: 
            return "Muito Alto"
    elif nome == "SELIC":  
        if valor <= 8: 
            return "Baixa"
        elif valor <= 12: 
            return "Moderada"
        elif valor <= 15: 
            return "Alta"
        else: 
            return "Muito Alta"
    elif nome == "Inadimplencia":
        if valor <= 3: 
            return "Baixa"
        elif valor <= 5: 
            return "Moderada"
        else: 
            return "Alta"
    return "Indefinido"

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

    abas = st.tabs(["📊 Evolução Mensal", "📉 Comparação Anual", "📌 Correlação", "📆 Evolução Anual ", "🔮 Projeções Futuras"])

    #grafico 1, sobre a evolução mensal 
    with abas[0]:
        with st.expander("ℹ️ Sobre este gráfico"):
                    st.markdown(""" 💡 **Este gráfico mostra a evolução mensal dos indicadores ao longo do tempo.**
    - **SELIC**: Alta significa crédito mais caro.
    - **IPCA**: Indica aumento de preços.
    - **Inadimplência**: Mostra atrasos nos pagamentos dos Microempreendedores.
                                

            📌 **Dica para o MEI:** Planeje o caixa nos períodos de alta e observe tendências para antecipar estratégias.""")
                    st.caption("Fonte dos dados: Banco Central do Brasil (BACEN)")

        for indicador in indicadores_selecionados:
            col1, col2 = st.columns([4, 1])
            with col1:
                fig = px.line(df, x="Date", y=indicador, title=f"Evolução de {indicador}", color_discrete_sequence=[CORES[indicador]])
                
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                valor_medio = df[df["Ano"] == ano_max][indicador].mean()
                st.metric(
                    label=f"{indicador} médio ({ano_max})",
                    value=f"{valor_medio:.2f}%",
                    delta=classificar_indicador(indicador, valor_medio)
                   )
    #grafico de media anual 
    with abas[1]:
        with st.expander("ℹ️ Sobre este gráfico"):
                    st.markdown(""" 💡 **Este gráfico mostra a média anual de cada indicador.**
    - Veja anos em que os indicadores dispararam ou caíram.
                                

    📌 **MEI:** Use isso para entender períodos mais favoráveis a crédito, investimentos ou reajuste de preços.""")
                    st.caption("Fonte dos dados: Banco Central do Brasil (BACEN)")

        for indicador in indicadores_selecionados:
            col1, col2 = st.columns([4, 1])
            with col1:
                media_anual = df.groupby("Ano")[indicador].mean().reset_index()
                fig = px.bar(media_anual, x="Ano", y=indicador, title=f"Média Anual de {indicador}",color_discrete_sequence=[CORES[indicador]])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                valor_medio = df[df["Ano"] == ano_max][indicador].mean()
                st.metric(
                    label=f"{indicador} médio ({ano_max})",
                    value=f"{valor_medio:.2f}%",
                    delta=classificar_indicador(indicador, valor_medio)
                )
    #correlção
    with abas[2]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("Este gráfico mostra a correlação entre dois indicadores.")
            st.markdown("📌 **MEI:** Correlações ajudam a prever impactos de um indicador sobre o outro.")
            st.caption("Fonte dos dados: Banco Central do Brasil (BACEN)")

        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Eixo X", indicadores_disponiveis)
        with col2:
            y_axis = st.selectbox("Eixo Y", [i for i in indicadores_disponiveis if i != x_axis])

        fig = px.scatter(df, x=x_axis, y=y_axis, trendline="ols", title=f"Correlação entre {x_axis} e {y_axis}",color_discrete_sequence=[CORES[x_axis]])
        st.plotly_chart(fig, use_container_width=True)

        correlacao = df[x_axis].corr(df[y_axis])
        nivel = (
            "forte" if correlacao > 0.7 else
            "moderada" if correlacao > 0.4 else
            "fraca" if correlacao > 0.2 else
            "muito fraca"
        )
        direcao = "direta" if correlacao > 0 else "inversa"
        st.info(f"📌 Correlação: **{nivel}** e **{direcao}** ({correlacao:.2f})")

    #evoluçao anual
    with abas[3]:
        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""
          💡 **Evolução Anual dos Indicadores:**
        - Cada linha representa um indicador econômico.
        - Valores médios calculados por ano.
                        

        📌 **Dica MEI:** Compare tendências de longo prazo para planejamento estratégico.
            """)
            st.caption("Fonte: Banco Central do Brasil (BACEN)")

        #Agrupa dados por ano e calcula a média
        df_anual = df.groupby("Ano")[indicadores_disponiveis].mean().reset_index()

        fig = px.line(
            df_anual,
            x="Ano",
            y=indicadores_disponiveis,
            color_discrete_map=CORES,  
            markers=True, 
            labels={"value": "Valor (%)", "variable": "Indicador"},
            title="Evolução Anual dos Indicadores (Média)"
        )

        #formatação
        fig.update_xaxes(tickvals=df_anual["Ano"].unique(), tickangle=45)
        fig.update_yaxes(tickformat=".1f%")
        fig.update_traces(line_width=2.5)
        
        st.plotly_chart(fig, use_container_width=True)

    #with abas[4]:
     #   with st.expander("ℹ️ Sobre este gráfico"):
      #      st.markdown("Todos os indicadores juntos, por mês.")
       #     st.markdown("📌 **MEI:** Veja os picos ou quedas gerais no ambiente econômico.")
        #    st.caption("Fonte dos dados: Banco Central do Brasil (BACEN)")

#        df_barra = df[['Date'] + indicadores_disponiveis].copy()
#       df_barra['AnoMes'] = df_barra['Date'].dt.to_period('M').astype(str)
 #       df_melt = df_barra.melt(id_vars="AnoMes", value_vars=indicadores_disponiveis,
  #                              var_name="Indicador", value_name="Valor")
   ##     fig = px.bar(df_melt, x="AnoMes", y="Valor", color="Indicador", title="Indicadores Combinados por Mês",)
     #   st.plotly_chart(fig, use_container_width=True)

    with abas[4]:
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
            st.caption("Fonte: Relatório Focus (BACEN)")
    st.markdown("---")
    st.markdown(
    "📌 **Fonte dos dados**: [Banco Central do Brasil (BACEN)](https://www.bcb.gov.br) &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; 🔗 **Acesse o portal oficial do MEI no Sebrae**: [Sebrae MEI](https://sebrae.com.br/sites/PortalSebrae/mei)",
    unsafe_allow_html=True
)

elif pagina == "Contabilidade":
    import streamlit_app
    streamlit_app.app()

#elif pagina == "Mais Informações":
 #   st.title("🔗 Mais Informações para MEI")
#    st.markdown("""
#    Visite o portal oficial do Sebrae para MEIs:

#    👉 [Acesse agora o Portal Sebrae MEI](https://sebrae.com.br/sites/PortalSebrae/mei)

  #  Lá você encontra orientações sobre:
 #   - Regularização
  #  - Tributação
 #   - Emissão de nota
 #   - Benefícios
 #   - E mais!
 #   """)



