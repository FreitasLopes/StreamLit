import streamlit as st
import streamlit.components.v1 as components
from PIL import Image


st.set_page_config(
    page_title="Contatos",
    layout="centered",
    page_icon="✉️",
    menu_items={}
)

# Função para criar sidebar personalizado

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

# Particle background
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

# Page content
st.markdown("# ✉️ Contatos")
st.markdown("""
    Entre em contato com nossa equipe para tirar dúvidas, 
    dar sugestões ou reportar problemas.
""")

# Contact form
with st.form("contact_form"):
    st.markdown("### Envie sua mensagem")
    name = st.text_input("Nome")
    email = st.text_input("Email")
    message = st.text_area("Mensagem")
    submitted = st.form_submit_button("Enviar")
    
    if submitted:
        st.success("Mensagem enviada com sucesso! Entraremos em contato em breve.")

# Team information
st.markdown("""
<style>
    .team-header {
        color: #2D89EF;
        font-size: 28px !important;
        font-weight: 700;
        text-align: center;
        margin: 20px 0 10px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #2D89EF;
    }
    
    .team-name {
        font-size: 24px !important;
        font-weight: 600;
        text-align: center;
        margin: 15px 0;
        background: linear-gradient(90deg, #FF4B4B, #FF8C00, #FFD700, #4CAF50, #2D89EF, #6A5ACD);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: rainbow 5s ease infinite;
        background-size: 400% 100%;
    }
    
    @keyframes rainbow {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }
    
    .team-description {
        text-align: center;
        font-size: 16px;
        color: #555;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Team header with enhanced styling
st.markdown('<div class="team-header">EQUIPE HELP MEI SP</div>', unsafe_allow_html=True)
st.markdown('<div class="team-name">Os café com Leite</div>', unsafe_allow_html=True)
st.markdown('<div class="team-description">Grupo de desenvolvimento dedicado a criar soluções para microempreendedores</div>', unsafe_allow_html=True)

# Team members with GitHub links
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="team-card">', unsafe_allow_html=True)
    st.markdown("### Integrantes")
    
    # Team members with GitHub links - REPLACE WITH ACTUAL LINKS
    st.markdown("""
    - [Eduarda Lopes](https://www.linkedin.com/in/mariaeflopes/) <span class="github-icon">🔗</span>
    - [Flávio Santos](https://www.linkedin.com/in/flaviojose-santos/) <span class="github-icon">🔗</span>
    - [Jenifer Barreto](https://www.linkedin.com/in/jenifer-barreto-55022523b/) <span class="github-icon">🔗</span>
    - [Maria Kassandra Alves Gomes](https://www.linkedin.com/in/maria-kassandra-alves-a6b406284/) <span class="github-icon">🔗</span>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-card">', unsafe_allow_html=True)
    st.markdown("### Professores Orientadores")
    st.markdown("""
    - Eduardo Savino Gomes
    - Lucy Mari Tabuti
    - Paula Sanchez Astorino
    - Rodnil da Silva Moreira Lisbôa
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Additional contact info
st.markdown('<div class="section-title">Outras formas de contato</div>', unsafe_allow_html=True)
st.markdown("""
- **Email:** contato@helpmei.com.br
- **Telefone:** (11) 9####-####
- **Endereço:** São Paulo - SP, Brasil
---
""")

# Link back to home
st.page_link("🏠Home.py", label="← Voltar para a página inicial", icon="🏠")

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
