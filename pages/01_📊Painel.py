import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os
import streamlit.components.v1 as components
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Painel Econômico Interativo para MEI",
    layout="wide",
    page_icon="📊",
    menu_items={}  # Desativa o menu automático
)

# Cores dos indicadores
CORES = {
    "SELIC": "#2980B9",
    "IPCA": "#27AE60",
    "Inadimplencia": "#E74C3C"
}

# Função para configurar a sidebar

with st.sidebar:
        # Espaço vazio para empurrar o logo para baixo
        st.title("🔗 Mais Informações para MEI")
        st.markdown("""
            <p style="font-size:15px; margin-top:15px;">
                <a href="https://sebrae.com.br/sites/PortalSebrae/mei" target="_blank" style="color:#4169E1; text-decoration:none;">
                    👉 Acesse agora o Portal Sebrae MEI
                </a>
            </p>

            <p style="font-size:16px; margin-top:20px;">Lá você encontra orientações sobre:</p>
            <ul style="font-size:16px; color:#FFFFFF;">
                <li>📝 Regularização</li>
                <li>💰 Tributação</li>
                <li>🧾 Emissão de nota</li>
                <li>🎁 Benefícios</li>
                <li>🔍 E mais!</li>
            </ul>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
        """
        <span style='color: #FFFFFF; font-weight: bold;'>Help MEI</span><br>
        <span style='color: #FF5F15; font-style: italic;'>Visualize hoje. Cresça amanhã.</span>
        """, 
        unsafe_allow_html=True
    )

# Funções de dados 
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
    df = selic_df.merge(ipca_df, on='Date').merge(inad_df, on='Date').dropna()
    df['Ano'] = df['Date'].dt.year
    df['Mês'] = df['Date'].dt.month
    return df

def save_excel(df):
    relatorio = 'relatorio_mei.xlsx'
    if os.path.exists(relatorio):
        os.remove(relatorio)
    df.to_excel(relatorio, index=False)

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


# Partículas de fundo
particles_background = """
<style>
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        top: 0;
        left: 0;
    }
</style>
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
    "particles": {
        "number": {
            "value": 80,
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": "#ffffff"
        },
        "shape": {
            "type": "circle"
        },
        "opacity": {
            "value": 0.5,
            "random": false
        },
        "size": {
            "value": 3,
            "random": true
        },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 1,
            "width": 1
        },
        "move": {
            "enable": true,
            "speed": 1,
            "direction": "none",
            "out_mode": "out"
        }
    },
    "interactivity": {
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"
            },
            "onclick": {
                "enable": true,
                "mode": "push"
            }
        },
        "modes": {
            "repulse": {
                "distance": 100
            },
            "push": {
                "particles_nb": 4
            }
        }
    },
    "retina_detect": true
});
</script>
"""

components.html(particles_background, height=150, width=2000, scrolling=False)


# Conteúdo principal
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

# Gráficos (mantidos do seu código original)
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

with abas[3]:
    with st.expander("ℹ️ Sobre este gráfico"):
        st.markdown("""
    💡 **Evolução Anual dos Indicadores:**
    - Cada linha representa um indicador econômico.
    - Valores médios calculados por ano.
                

    📌 **Dica MEI:** Compare tendências de longo prazo para planejamento estratégico.
        """)
        st.caption("Fonte: Banco Central do Brasil (BACEN)")

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

    fig.update_xaxes(tickvals=df_anual["Ano"].unique(), tickangle=45)
    fig.update_yaxes(tickformat=".1f%")
    fig.update_traces(line_width=2.5)
    
    st.plotly_chart(fig, use_container_width=True)

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

# Rodapé no final da página
st.markdown("""
<style>
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
    }
</style>
<div class="footer">
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        <img alt="Licença Creative Commons" style="border-width:0" 
             src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
    </a>
    <br />
    Este trabalho está licenciado sob uma 
    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
        Licença Creative Commons Atribuição 4.0 Internacional
    </a>.
</div>
""", unsafe_allow_html=True)