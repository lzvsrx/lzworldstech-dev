import streamlit as st
from streamlit_option_menu import option_menu
import base64
import os
import textwrap
from deep_translator import GoogleTranslator
import re
import streamlit.components.v1 as components

# --- STABILITY UTILS ---
def safe_read_file(path, binary=False):
    """Safely read a file and return its content or an empty string/bytes."""
    try:
        if os.path.exists(path):
            mode = "rb" if binary else "r"
            with open(path, mode) as f:
                return f.read()
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {path}")
    return b"" if binary else ""

def get_base64_resource(path):
    """Convert resource to base64 safely."""
    data = safe_read_file(path, binary=True)
    if data:
        return base64.b64encode(data).decode()
    return ""

# Page Config
st.set_page_config(page_title="Luiz Otavio Valenzi Sousa - Portfolio", page_icon="💻", layout="wide", initial_sidebar_state="expanded")

# --- TRANSLATION SYSTEM ---
@st.cache_data(show_spinner=False)
def translate_text(text, target_lang='pt'):
    if target_lang == 'pt' or not text:
        return text
    try:
        # Strip HTML for translation to avoid breaking tags
        clean_text = re.sub(r'<[^>]+>', '', str(text))
        if not clean_text.strip():
            return text
        
        translated = GoogleTranslator(source='auto', target=target_lang).translate(clean_text)
        
        # If the original was HTML, we try to preserve structure (basic)
        if '<' in str(text) and '>' in str(text):
            # This is a simplified approach, for complex HTML we'd need a parser
            return text.replace(clean_text, translated)
        return translated
    except Exception:
        return text

def get_base64_font(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def text_to_braille(text):
    braille_dict = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵', ' ': ' ', '.': '⠲', ',': '⠂', '!': '⠖',
        '0': '⠴', '1': '⠂', '2': '⠆', '3': '⠒', '4': '⠲', '5': '⠢', '6': '⠖', '7': '⠶', '8': '⠦', '9': '⠔',
        '?': '⠦', ':': '⠒', ';': '⠆', '(': '⠦', ')': '⠴', '-': '⠤', '/': '⠌', '@': '⠈', '+': '⠖', '=': '⠶',
        'á': '⠷', 'é': '⠿', 'í': '⠌', 'ó': '⠬', 'ú': '⠾', 'â': '⠟', 'ê': '⠮', 'î': '⠩', 'ô': '⠹', 'û': '⠱',
        'ã': '⠯', 'õ': '⠵', 'ç': '⠯'
    }
    return "".join(braille_dict.get(c.lower(), c) for c in str(text))

def write_braille(text, is_markdown=False, is_sidebar=False):
    container = st.sidebar if is_sidebar else st
    
    # --- AUTOMATIC TRANSLATION ---
    target_lang = st.session_state.get('target_lang', 'pt')
    display_text = text
    if target_lang != 'pt':
        display_text = translate_text(text, target_lang)

    if is_markdown:
        container.markdown(display_text, unsafe_allow_html=True)
    else:
        container.write(display_text)
    
    if st.session_state.get('braille_mode', False):
        import re
        # Remove markdown/html symbols for braille translation
        clean_text = re.sub(r'<[^>]+>', '', str(display_text)) # remove HTML tags
        clean_text = clean_text.replace("**", "").replace("*", "").replace("#", "").replace("---", "")
        container.markdown(f'<p class="braille-text">{text_to_braille(clean_text)}</p>', unsafe_allow_html=True)

# Define the technological/animated style
font_base64 = get_base64_font("assets/fonts/DonGraffiti.ttf")
custom_style = f"""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
    /* Import Don Graffiti */
    @font-face {{
        font-family: 'Don Graffiti';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    body {{
        background-color: #050a15;
        color: #e0f7fa;
        font-family: 'Share Tech Mono', monospace;
    }}

    /* Apply Don Graffiti only to headers and specific text to avoid breaking UI icons */
    h1, h2, h3, h4, h5, h6, .graffiti-text, .stButton button, .stLinkButton a, [data-testid="stExpander"] summary p {{
        font-family: 'Don Graffiti', cursive !important;
        color: #00ffcc;
        text-shadow: 2px 2px 5px #000, 0 0 10px rgba(0, 255, 204, 0.7);
        letter-spacing: 2px;
    }}

    .stApp {{
        background: radial-gradient(circle at center, #0a192f 0%, #050a15 100%);
    }}

    /* Moving Profile Image Animation */
    @keyframes float {{
        0% {{ transform: translatey(0px) rotate(0deg); box-shadow: 0 0 20px #00ffcc; }}
        50% {{ transform: translatey(-20px) rotate(5deg); box-shadow: 0 0 40px #00ff00; }}
        100% {{ transform: translatey(0px) rotate(0deg); box-shadow: 0 0 20px #00ffcc; }}
    }}

    .profile-pic {{
        border-radius: 50%;
        border: 4px solid #00ffcc;
        animation: float 4s ease-in-out infinite;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 250px;
        height: 250px;
        object-fit: cover;
    }}

    /* Modern Technological Card Style (Glassmorphism) */
    .tech-card {{
        background: rgba(10, 25, 47, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .tech-card:hover {{
        transform: translateY(-5px);
        border-color: #00ffcc;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
        background: rgba(10, 25, 47, 0.9);
    }}

    /* Animated Background Lines */
    .bg-lines {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-image: 
            linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px);
        background-size: 60px 60px;
        animation: grid-move 30s linear infinite;
    }}

    @keyframes grid-move {{
        from {{ background-position: 0 0; }}
        to {{ background-position: 0 1000px; }}
    }}

    /* Footer Style */
    .footer {{
        text-align: center;
        padding: 30px;
        font-size: 14px;
        color: #00ffcc;
        border-top: 1px solid rgba(0, 255, 204, 0.2);
        margin-top: 60px;
        background: rgba(5, 10, 21, 0.8);
    }}
    /* Fix expander layout and icons */
    .stExpander {{
        background: rgba(10, 25, 47, 0.5) !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        border-radius: 12px !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
    }}
    
    .stExpander:hover {{
        border-color: #00ffcc !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }}

    /* Target only the title text inside expander */
    .stExpander summary {{
        color: #00ffcc !important;
    }}
    
    .stExpander summary p {{
        font-size: 1.1rem !important;
        margin: 0 !important;
        padding: 12px 0 !important;
        color: #00ffcc !important;
    }}

    /* Accessibility: High Contrast and Focus */
    :focus {{
        outline: 3px solid #00ffcc !important;
        outline-offset: 2px !important;
    }}

    .sr-only {{
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        border: 0;
    }}
</style>
<div class="bg-lines"></div>
"""

# Inject custom CSS and Google Translate scripts
st.markdown(custom_style, unsafe_allow_html=True)

# Cookie Consent Banner (Simplified for Legal Compliance)
if 'cookies_accepted' not in st.session_state:
    with st.container():
        col_c1, col_c2 = st.columns([4, 1])
        with col_c1:
            st.caption("🍪 Este site utiliza cookies básicos para melhorar sua experiência e garantir a segurança legal da navegação.")
        with col_c2:
            if st.button("Aceitar"):
                st.session_state.cookies_accepted = True
                st.rerun()

# Sidebar Navigation
with st.sidebar:
    write_braille("### 🌍 Idioma & Tradução", is_markdown=True, is_sidebar=True)
    
    # New Native Translation System
    languages = {
        "Português": "pt",
        "English": "en",
        "Español": "es",
        "Français": "fr",
        "日本語": "ja",
        "中文": "zh-CN",
        "Deutsch": "de",
        "Italiano": "it",
        "Русский": "ru"
    }
    
    selected_lang_name = st.selectbox("Escolha o Idioma:", list(languages.keys()), index=0)
    st.session_state['target_lang'] = languages[selected_lang_name]
    
    if st.session_state['target_lang'] != 'pt':
        st.info(f"Tradução automática para {selected_lang_name} ativada.")
    
    st.markdown("---")
    
    # Personal Info Section in Sidebar
    write_braille("### 👤 Quem é Luiz Otavio?", is_markdown=True, is_sidebar=True)
    sidebar_html = """
    <div class="tech-card" style="padding: 15px; font-size: 0.9rem; border-color: rgba(0, 255, 204, 0.2);">
        <p style="margin: 0 0 8px 0; color: #e0f7fa;"><strong>Identidade:</strong> Luiz Otavio Valenzi Sousa</p>
        <p style="margin: 0 0 8px 0; color: #e0f7fa;"><strong>Status:</strong> Profissional Autônomo</p>
        <p style="margin: 0 0 8px 0; color: #e0f7fa;"><strong>Local:</strong> Pouso Alegre Minas Gerais Brasil</p>
        <p style="margin: 0 0 8px 0; color: #e0f7fa;"><strong>Foco:</strong> Software & Hardware</p>
        <p style="margin: 0; color: #e0f7fa;"><strong>Objetivo:</strong> Inovação Digital</p>
    </div>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)
    
    # Legal Verification Badge
    st.markdown("""
    <div style="background: rgba(0, 255, 204, 0.1); border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; margin-top: 10px; text-align: center;">
        <span style="color: #00ffcc; font-size: 0.8rem; font-weight: bold;">✅ IDENTIDADE VERIFICADA</span><br>
        <span style="color: #e0f7fa; font-size: 0.7rem;">Portfólio Oficial LZ TECH</span>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get('braille_mode', False):
        st.sidebar.markdown(f'<p class="braille-text" style="font-size: 1rem !important;">{text_to_braille("Luiz Otavio: 23 anos, Pouso Alegre Minas Gerais Brasil, Software e Hardware")}</p>', unsafe_allow_html=True)

    st.markdown("---")
    write_braille("### ♿ Acessibilidade", is_markdown=True, is_sidebar=True)
    contrast_mode = st.toggle("Modo Alto Contraste")
    large_font = st.toggle("Fonte Ampliada")
    
    if contrast_mode:
        st.markdown("""
        <style>
            .stApp { background: #000 !important; }
            .tech-card { background: #000 !important; border: 2px solid #fff !important; color: #fff !important; }
            p, h1, h2, h3, span, label { color: #fff !important; text-shadow: none !important; }
            .bg-lines { display: none !important; }
        </style>
        """, unsafe_allow_html=True)
    
    if large_font:
        st.markdown("""
        <style>
            html, body, p, span, label { font-size: 1.25rem !important; }
            h1 { font-size: 3rem !important; }
            h2 { font-size: 2.5rem !important; }
            h3 { font-size: 2rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # Braille and Audio Reader
    write_braille("---", is_markdown=True, is_sidebar=True)
    write_braille("### 🔊 Acessibilidade Completa", is_markdown=True, is_sidebar=True)
    
    # Audio Reader
    if st.button("🔊 Ler Todos os Textos (Voz)"):
        # Build comprehensive text to read
        content_to_read = f"""
        Nome: Luiz Otavio Valenzi Sousa. 
        Bio: Amo tecnologia, informática e programação desde pequeno. 
        Formação: Técnico em Informática e Graduando em Engenharia de Software. 
        Habilidades: Python, HTML, CSS, JavaScript, Django, React e mais. 
        Projetos principais: Cores e Fragrâncias, Unis Estágios e NTB System.
        """
        # Improved JavaScript using components.html to ensure execution
        components.html(f"""
            <script>
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{content_to_read}');
                msg.lang = 'pt-BR';
                msg.rate = 1.0;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
        st.success("Lendo conteúdo...")

    # Braille Text Translator
    braille_mode = st.toggle("⠃ Exibir Letras em Braille", key='braille_mode')
    if braille_mode:
        write_braille("Tradução automática para caracteres Braille Unicode ativada.", is_sidebar=True)
        st.markdown("""
        <style>
            .braille-text { font-family: 'Share Tech Mono', monospace; font-size: 1.5rem !important; color: #fff !important; }
        </style>
        """, unsafe_allow_html=True)

    write_braille("---", is_markdown=True, is_sidebar=True)
    selected = option_menu(
        menu_title="LZ TECH NAV",
        options=["Home", "Perfil", "Habilidades", "Carreira", "Projetos", "LZ Chatbot", "Contato"],
        icons=["terminal-fill", "fingerprint", "activity", "award-fill", "boxes", "gpu-card", "headset"],
        menu_icon="motherboard-fill",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#0a192f"},
            "icon": {"color": "#00ffcc", "font-size": "25px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#112240", "color": "#00ffcc", "font-family": "'Share Tech Mono', monospace", "text-transform": "uppercase", "letter-spacing": "1px"},
            "nav-link-selected": {"background-color": "#112240", "font-family": "'Share Tech Mono', monospace", "font-weight": "bold", "border-left": "4px solid #00ffcc"},
        }
    )

# --- HOME SECTION ---
if selected == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        write_braille('<h1 class="graffiti-text">Luiz Otavio Valenzi Sousa</h1>', is_markdown=True)
        write_braille("### 💻 Desenvolvedor Full-Stack & Futuro Engenheiro de Software", is_markdown=True)
        write_braille("✨ Bem-vindo ao meu universo tecnológico. Transformando sonhos em código. 🌌")
        write_braille("📍 Localizado em Pouso Alegre Minas Gerais Brasil")
        
    with col2:
        # Check if profile picture exists, else use placeholder
        profile_b64 = get_base64_resource("assets/profile.jpg")
        if profile_b64:
            st.markdown(f'<img src="data:image/jpeg;base64,{profile_b64}" class="profile-pic" alt="Foto de Perfil de Luiz Otavio">', unsafe_allow_html=True)
        else:
            write_braille("Adicione sua foto em assets/profile.jpg para vê-la aqui com animação!")
            st.markdown('<img src="https://via.placeholder.com/250" class="profile-pic" alt="Placeholder de Perfil">', unsafe_allow_html=True)

# --- PERFIL SECTION ---
elif selected == "Perfil":
    write_braille('<h2 class="graffiti-text">Sobre Mim</h2>', is_markdown=True)
    
    col_perfil1, col_perfil2 = st.columns([1.2, 1])
    
    with col_perfil1:
        # Perfil Text - Fixed indentation to avoid Markdown interpreting as a code block
        perfil_html = """
<div class="tech-card">
<h3 style="color: #00ffcc; font-size: 1.2rem; margin-bottom: 15px;">👤 Identidade Digital</h3>
<ul style="list-style-type: none; padding-left: 0; color: #e0f7fa;">
<li style="margin-bottom: 8px;"><strong>Nome:</strong> Luiz Otavio Valenzi Sousa</li>
<li style="margin-bottom: 8px;"><strong>Idade:</strong> 23 anos</li>
<li style="margin-bottom: 8px;"><strong>Localização:</strong> Pouso Alegre Minas Gerais Brasil</li>
<li style="margin-bottom: 8px;"><strong>Status:</strong> Desenvolvedor & Futuro Engenheiro de Software</li>
</ul>

<h3 style="color: #00ffcc; font-size: 1.2rem; margin-top: 25px; margin-bottom: 15px;">🚀 Minha Jornada</h3>
<p style="color: #e0f7fa; line-height: 1.6; margin-bottom: 15px;">
Desde os primeiros cliques, a tecnologia foi meu playground. Comecei desmontando e montando hardwares e hoje construo sistemas complexos. 
Minha paixão é a intersecção entre o <strong>Código Eficiente</strong> e a <strong>Acessibilidade Universal</strong>.
</p>

<h3 style="color: #00ffcc; font-size: 1.2rem; margin-top: 25px; margin-bottom: 15px;">💡 Missão e Valores</h3>
<p style="color: #e0f7fa; line-height: 1.6; margin-bottom: 15px;">
Acredito que a tecnologia deve ser democrática. Por isso, foco em desenvolver soluções que incluam todos (como meu sistema de leitura em Braille e áudio). 
Meus valores são: <strong>Inovação constante, Integridade técnica e Curiosidade sem limites.</strong>
</p>

<h3 style="color: #00ffcc; font-size: 1.2rem; margin-top: 25px; margin-bottom: 15px;">🎯 Visão de Futuro</h3>
<p style="color: #e0f7fa; line-height: 1.6;">
Meu objetivo é fundar a <strong>LZ Tech</strong>, uma empresa focada em transformar a vida das pessoas através de softwares inteligentes e hardware de alta performance.
</p>

<h3 style="color: #00ffcc; font-size: 1.2rem; margin-top: 25px; margin-bottom: 15px;">⚖️ Segurança e Verificação Legal</h3>
<p style="color: #e0f7fa; line-height: 1.6;">
Este site opera como um <strong>Portfólio Profissional Autônomo</strong>. Todas as atividades aqui descritas estão em conformidade com a legislação brasileira vigente, incluindo a <strong>LGPD (Lei 13.709/2018)</strong> e a <strong>LBI (Lei 13.146/2015)</strong>. Os dados coletados via formulário são criptografados pelo provedor de serviço e utilizados estritamente para fins de orçamento e contato comercial direto.
</p>
</div>
"""
        write_braille(perfil_html, is_markdown=True)
        
    with col_perfil2:
        write_braille("### ⚡ Estatísticas LZ", is_markdown=True)
        stats = [
            ("💻", "Anos de Código", "5+"),
            ("🛠️", "Reparos de PC", "6"),
            ("📁", "Projetos GitHub", "15+"),
            ("📚", "Certificações", "20")
        ]
        
        for icon, label, val in stats:
            st.markdown(f"""<div class="tech-card" style="margin-bottom: 10px; padding: 15px; display: flex; align-items: center; justify-content: space-between;">
<span style="font-size: 1.5rem;">{icon}</span>
<span style="color: #e0f7fa; font-family: 'Share Tech Mono'; flex-grow: 1; margin-left: 15px;">{label}</span>
<span style="color: #00ffcc; font-weight: bold; font-size: 1.2rem;">{val}</span>
</div>""", unsafe_allow_html=True)
            if st.session_state.get('braille_mode', False):
                st.markdown(f'<p class="braille-text">{text_to_braille(f"{label}: {val}")}</p>', unsafe_allow_html=True)

    write_braille("---", is_markdown=True)
    write_braille("### 📜 Linha do Tempo Profissional", is_markdown=True)
    
    timeline = [
        ("2020", "Início do Curso Técnico no IFSULDEMINAS - Onde a paixão virou profissão."),
        ("2022", "Primeiros Projetos Freelance em Manutenção e Redes."),
        ("2023", "Ingresso na Engenharia de Software - Foco total em desenvolvimento."),
        ("2024", "Criação do sistema Cores & Fragrâncias e foco em acessibilidade."),
        ("2025+", "Expansão da LZ Tech e novos horizontes em IA e Mobile.")
    ]
    
    for year, event in timeline:
        st.markdown(f"""
        <div style="border-left: 3px solid #00ffcc; padding-left: 20px; margin-left: 10px; margin-bottom: 20px;">
            <h4 style="color: #00ffcc; margin: 0;">{year}</h4>
            <p style="color: #e0f7fa; margin: 5px 0;">{event}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.get('braille_mode', False):
            st.markdown(f'<p class="braille-text">{text_to_braille(f"{year}: {event}")}</p>', unsafe_allow_html=True)

# --- HABILIDADES SECTION ---
elif selected == "Habilidades":
    write_braille('<h2 class="graffiti-text">Habilidades</h2>', is_markdown=True)
    
    skills = {
        "Python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "HTML5": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
        "CSS3": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
        "JavaScript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "PHP": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg",
        "Django": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg",
        "Pacote Office": "https://img.icons8.com/?size=100&id=OxTy4VlCaZQH&format=png&color=00FF00",
        "Microsoft Word": "https://img.icons8.com/?size=100&id=11571&format=png&color=00FF00",
        "Microsoft Excel": "https://img.icons8.com/?size=100&id=11566&format=png&color=00FF00",
        "Microsoft PowerPoint": "https://img.icons8.com/?size=100&id=12416&format=png&color=00FF00",
        "Linux": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
        "Windows": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/windows8/windows8-original.svg",
        "Java": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "TypeScript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
        "React.js": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
        "MySQL": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        "SQL": "https://www.svgrepo.com/show/331760/sql-database-generic.svg",
        "Mobile": "https://img.icons8.com/?size=100&id=12580&format=png&color=00FF00",
        "Inteligência Artificial": "https://img.icons8.com/?size=100&id=61864&format=png&color=000000",
        "Montagem de Computador": "https://img.icons8.com/nolan/64/computer.png",
        "Formatação de Computador": "https://img.icons8.com/?size=100&id=12908&format=png&color=000000",
        "Reparo de Computador": "https://img.icons8.com/nolan/64/maintenance.png",
    }
    
    cols = st.columns(4)
    for idx, (name, icon) in enumerate(skills.items()):
        with cols[idx % 4]:
            write_braille(f"""
            <div class="tech-card" style="text-align: center; margin-bottom: 20px; padding: 15px;">
                <img src="{icon}" width="70" style="filter: drop-shadow(0 0 10px #00ffcc); transition: transform 0.3s;">
                <p style="color: #00ffcc; margin-top: 15px; font-size: 1.1em; font-weight: bold;">{name}</p>
            </div>
            """, is_markdown=True)

# --- CARREIRA SECTION ---
elif selected == "Carreira":
    write_braille('<h2 class="graffiti-text">Formação & Cursos</h2>', is_markdown=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        write_braille("### 🎓 Graduação", is_markdown=True)
        grad_text = "- Bacharelado em Engenharia de Software - Anhanguera (2023 - 2026)\n- Técnico em Informática - Instituto Federal do Sul de Minas (2020 - 2023)"
        write_braille(grad_text)
        
        with st.expander("Ver Diploma Técnico em Informática"):
            pdf_path = "assets/certs/tecnico-de-informatica.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf">'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                write_braille("⚠️ Diploma não encontrado em assets/certs/tecnico-de-informatica.pdf")
        
    with col2:
        write_braille("### 📜 Cursos & Certificados", is_markdown=True)
        courses = {
            "Imersão Front-End - Alura (2024)": ("alura.pdf", "🎨"),
            "Direito Eletrônico - Anhanguera (2023)": ("direito-eletronico.pdf", "⚖️"),
            "Tecnologias da Informação Aplicadas ao Direito - Anhanguera (2023)": ("TECNOLOGIAS DE INFORMAÇÃO APLICADAS AO DIREITO.pdf", "⚖️"),
            "Tecnologia, Direito Digital e Propriedade Intelectual - Anhanguera (2023)": ("TECNOLOGIA, DIREITO DIGITAL E PROPRIEDADE INTELECTUAL.pdf", "⚖️"),
            "Novos Desenvolvimentos em IoT - Anhanguera (2023)": ("NOVOS DESENVOLVIMENTOS EM IOT.pdf", "🌐"),
            "Redes de Computadores e IoT - Anhanguera (2023)": ("REDES DE COMPUTADORES E A INTERNET DAS COISAS.pdf", "🌐"),
            "Sensores, Microcontroladores e Programação IoT - Anhanguera (2023)": ("SENSORES, MICROCONTROLADORES E PROGRAMAÇÃO EM INTERNET DAS COISAS.pdf", "🌐"),
            "IoT e Programação de Sensores - Anhanguera (2023)": ("IOT e Programação de Sensores.pdf", "🌐"),
            "Empreendedorismo e Inovação - Anhanguera (2023)": ("EMPREENDEDORISMO E INOVAÇÃO.pdf", "💡"),
            "Processo da Criatividade - Anhanguera (2023)": ("PROCESSO DA CRIATIVIDADE.pdf", "💡"),
            "Estruturas de Dados em Python - Anhanguera (2023)": ("ESTRUTURAS DE DADOS EM PYTHON.pdf", "🐍"),
            "Introdução à Análise de Dados com Python - Anhanguera (2023)": ("INTRODUÇÃO À ANÁLISE DE DADOS COM PYTHON.pdf", "🐍"),
            "Introdução à Linguagem Python - Anhanguera (2023)": ("INTRODUÇÃO À LINGUAGEM PYTHON.pdf", "🐍"),
            "Análise de Dados com Python - Anhanguera (2023)": ("analise de dados com python.pdf", "🐍"),
            "Django Web Framework + DRF - Udemy (2026)": ("django.pdf", "🎯"),
            "Frontend HTML CSS JS + Projetos - Udemy (2026)": ("html-css-js.pdf", "💻"),
            "Python 3 do Básico ao Avançado - Udemy (2023)": ("python.pdf", "🐍")
        }
        
        for course_name, (pdf_filename, icon) in courses.items():
            with st.expander(f"{icon} {course_name}"):
                write_braille("Visualizar certificado")
                write_braille(course_name)
                
                # Try multiple paths for PDFs
                pdf_paths = [f"assets/certs/{pdf_filename}", f"assets/fonts/{pdf_filename}"]
                base64_pdf = ""
                for p in pdf_paths:
                    base64_pdf = get_base64_resource(p)
                    if base64_pdf: break
                
                if base64_pdf:
                    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf">'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    write_braille(f"⚠️ Certificado {pdf_filename} não encontrado.")

# --- PROJETOS SECTION ---
elif selected == "Projetos":
    write_braille('<h2 class="graffiti-text">Meus Projetos</h2>', is_markdown=True)
    
    projects = [
        {
            "title": "🌸 Cores & Fragrâncias by Berenice",
            "desc": "Site com sistema de controle de estoque de produtos cosméticos.",
            "status": "📅 Feito em 2025 | 🔄 Atualizado Diariamente",
            "link": "https://coresefragranciasbyberenice-3.streamlit.app/",
            "main_img": "assets/projects/coresefragrancias1.png",
            "other_imgs": ["assets/projects/coresefragrancias2.png", "assets/projects/coresefragrancias3.png"]
        },
        {
            "title": "🎓 Unis Estágios e Serviços",
            "desc": "Página para procura de estágios e empregos com a faculdade Unis de Varginha-MG.",
            "status": "📅 Feito em 2025 | ✅ Terminado em 2026",
            "link": "https://unis-estagios-e-servicos.streamlit.app/",
            "main_img": "assets/projects/unis1.png",
            "other_imgs": [f"assets/projects/unis{i}.png" for i in range(2, 18)]
        },
        {
            "title": "📱 NTB - Sistema de Certificação Técnica",
            "desc": "Aplicativo Android para laudos técnicos de engenharia e engenharia hospitalar.",
            "status": "📅 Feito em 2025 | 🛑 Manutenção Parada",
            "link": "#",
            "main_img": "assets/projects/ntb1.png",
            "other_imgs": ["assets/projects/ntb2.png", "assets/projects/ntb3.png", "assets/projects/ntb4.png"]
        }
    ]
    
    for project in projects:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                if os.path.exists(project["main_img"]):
                    st.image(project["main_img"], use_container_width=True)
                else:
                    write_braille(f"Imagem {project['main_img']} não encontrada")
                
                # Exibir outras imagens se existirem
                if project["other_imgs"]:
                    with st.expander("Ver mais imagens"):
                        cols = st.columns(2)
                        for idx, img_path in enumerate(project["other_imgs"]):
                            if os.path.exists(img_path):
                                with cols[idx % 2]:
                                    st.image(img_path, use_container_width=True)
            with col2:
                write_braille(f"### {project['title']}", is_markdown=True)
                write_braille(f"*{project['status']}*", is_markdown=True)
                write_braille(project["desc"])
                if project["link"] != "#":
                    st.link_button("Ver Projeto", project["link"])
            write_braille("---", is_markdown=True)

# --- CHATBOT SECTION ---
elif selected == "LZ Chatbot":
    write_braille('<h2 class="graffiti-text">Assistente Virtual LZ Tech</h2>', is_markdown=True)
    
    # Base de conhecimento do Chatbot
    knowledge_base = {
        "projetos": "Luiz desenvolveu projetos incríveis: 🌸 'Cores & Fragrâncias' (Controle de estoque, 2025, atualizado diariamente), 🎓 'Unis Estágios' (Busca de empregos, 2025-2026) e 📱 'NTB System' (Laudos técnicos Android, 2025).",
        "habilidades": "As habilidades técnicas incluem: Python, HTML, CSS, JavaScript, PHP, Django, Pacote Office (Word, Excel, PowerPoint), Linux, Windows, Java, TypeScript, React.js, MySQL, SQL, Mobile e Inteligência Artificial. Além de Montagem, Formatação e Reparo de Computadores.",
        "formação": "Luiz é Técnico em Informática pelo IF Sul de Minas (2020-2023) e está cursando Bacharelado em Engenharia de Software na Anhanguera (2023-2026).",
        "cursos": "Possui diversos certificados: Imersão Front-End (Alura), Direito Eletrônico, IoT, Estrutura de Dados, Django Web Framework (Udemy) e muitos outros.",
        "contato": "Você pode entrar em contato pelo e-mail: valenzisousaluizotavio@gmail.com ou WhatsApp: +55 35 99921-5995.",
        "sobre": "Luiz Otavio tem 23 anos, é apaixonado por tecnologia desde pequeno e sonha em ter sua própria empresa inovadora."
    }

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            write_braille(message["content"])

    # Input do usuário
    if prompt := st.chat_input("Pergunte sobre meus projetos, habilidades ou formação..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            write_braille(prompt)

        # Resposta lógica simples
        response = "Desculpe, ainda estou aprendendo! Tente perguntar sobre 'projetos', 'habilidades', 'formação' ou 'contato'."
        p_low = prompt.lower()
        
        if "projeto" in p_low: response = knowledge_base["projetos"]
        elif "habilidade" in p_low or "tecnologia" in p_low or "sabe" in p_low: response = knowledge_base["habilidades"]
        elif "formação" in p_low or "estudo" in p_low or "faculdade" in p_low: response = knowledge_base["formação"]
        elif "curso" in p_low or "certificado" in p_low: response = knowledge_base["cursos"]
        elif "contato" in p_low or "email" in p_low or "whatsapp" in p_low: response = knowledge_base["contato"]
        elif "quem" in p_low or "sobre" in p_low: response = knowledge_base["sobre"]

        with st.chat_message("assistant"):
            write_braille(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- CONTATO SECTION ---
elif selected == "Contato":
    write_braille('<h2 class="graffiti-text">Contato & Redes</h2>', is_markdown=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        write_braille("### Me mande uma mensagem!", is_markdown=True)
        # Jotform Iframe Integration
        jotform_iframe = """<iframe 
title="Envio de Projetos de Site" 
src="https://form.jotform.com/260857281730056" 
width="100%" 
height="800" 
frameborder="0" 
style="border:none; border-radius:15px; background: rgba(10, 25, 47, 0.7); backdrop-filter: blur(10px);" 
allowfullscreen> 
</iframe>"""
        st.markdown(jotform_iframe, unsafe_allow_html=True)
        
        # LGPD Notice for Compliance
        st.markdown("""
        <div style="font-size: 0.75rem; color: #e0f7fa; background: rgba(0, 255, 204, 0.05); padding: 10px; border-radius: 8px; margin-top: 10px;">
            ⚖️ <strong>Aviso LGPD:</strong> Seus dados são usados apenas para retorno de contato profissional e não são compartilhados. Ao enviar o formulário, você concorda com o processamento dos dados fornecidos para este fim exclusivo.
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📄 Termos de Uso e Privacidade Detalhados"):
            st.markdown("""
            <div style="font-size: 0.85rem; color: #e0f7fa; line-height: 1.4;">
                <strong>1. Coleta de Dados:</strong> Apenas os dados informados voluntariamente no formulário acima são coletados.<br><br>
                <strong>2. Finalidade:</strong> O uso é estritamente profissional para responder a solicitações de orçamento ou dúvidas técnicas.<br><br>
                <strong>3. Segurança:</strong> Utilizamos integração com o Jotform, que aplica protocolos de criptografia SSL e conformidade internacional de segurança.<br><br>
                <strong>4. Direitos:</strong> Você pode solicitar a exclusão de seus dados a qualquer momento enviando um e-mail para o endereço listado ao lado.<br><br>
                <strong>5. Verificação:</strong> Este portfólio é mantido por Luiz Otavio Valenzi Sousa, residente em Pouso Alegre - MG, Brasil.
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.get('braille_mode', False):
            st.markdown(f'<p class="braille-text">{text_to_braille("Formulário de Contato Jotform: Envio de Projetos de Site")}</p>', unsafe_allow_html=True)
        
    with col2:
        write_braille("### Conecte-se comigo", is_markdown=True)
        links_html = """<div class="tech-card">
<p><img src="https://img.icons8.com/?size=100&id=0tREDFkScvsm&format=png&color=000000" width="25"> <a href="https://github.com/lzvsrx" style="color: #00ffcc; text-decoration: none;">GitHub</a></p>
<p><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="25"> <a href="https://www.linkedin.com/in/luiz-otavio-valenzi-sousa-1180bb360/" style="color: #00ffcc; text-decoration: none;">LinkedIn</a></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" width="25"> <a href="https://www.instagram.com/lzworldstech/" style="color: #00ffcc; text-decoration: none;">Instagram</a></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25"> <a href="https://wa.me/5535999215995" style="color: #00ffcc; text-decoration: none;">WhatsApp: +55 35 99921-5995</a></p>
<p>📧 valenzisousaluizotavio@gmail.com</p>
</div>"""
        st.markdown(links_html, unsafe_allow_html=True)
        
        st.markdown("---")
        write_braille("### 💬 Feedbacks & Reconhecimento", is_markdown=True)
        testimonials = [
            ("⭐", "Excelente profissional! O sistema Cores & Fragrâncias superou as expectativas.", "Berenice - Cliente"),
            ("🚀", "Destaque técnico na faculdade, sempre focado em soluções acessíveis.", "Coordenação - Engenharia de Software"),
            ("🛠️", "Confiança total na manutenção de nossos computadores há anos.", "Clientes de Manutenção")
        ]
        
        for icon, text, author in testimonials:
            st.markdown(f"""
            <div class="tech-card" style="margin-bottom: 10px; padding: 15px; border-left: 3px solid #00ffcc;">
                <p style="font-style: italic; color: #e0f7fa; font-size: 0.9rem;">"{text}"</p>
                <p style="color: #00ffcc; font-weight: bold; margin: 0; font-size: 0.8rem;">{icon} {author}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.session_state.get('braille_mode', False):
                st.markdown(f'<p class="braille-text">{text_to_braille(f"{author}: {text}")}</p>', unsafe_allow_html=True)
        if st.session_state.get('braille_mode', False):
            st.markdown(f'<p class="braille-text">{text_to_braille("Redes Sociais: GitHub, LinkedIn, Instagram e WhatsApp")}</p>', unsafe_allow_html=True)

# Footer
footer_html = """
<div class="footer">
    <p style="margin: 0;">Desenvolvido por <strong>Luiz Otavio Valenzi Sousa</strong> | LZ TECH</p>
    <p style="font-size: 0.7rem; margin-top: 5px; opacity: 0.7;">
        Portfólio Profissional de Desenvolvedor Autônomo | Pouso Alegre - MG - Brasil<br>
        Em conformidade com a LGPD e Acessibilidade Web (LBI).
    </p>
</div>
"""
write_braille(footer_html, is_markdown=True)
