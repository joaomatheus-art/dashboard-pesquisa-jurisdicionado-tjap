import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path
from PIL import Image

# ─── Configuração da página ───────────────────────────────────────────────────
_BASE = Path(__file__).parent
_logo_icon = _BASE / "logo_tjap_clean.png"
_icon = Image.open(_logo_icon) if _logo_icon.exists() else "⚖️"

st.set_page_config(
    page_title="Pesquisa Jurisdicionado",
    page_icon=_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Paleta TJAP ─────────────────────────────────────────────────────────────
TJAP_BLUE    = "#1A3A8F"
TJAP_GREEN   = "#1A8C3E"
TJAP_YELLOW  = "#F5C518"
TJAP_LIGHT   = "#E8EFFF"
TJAP_GRAY    = "#6B7280"
COLOR_NAO    = "#D94F3D"
COLOR_NEUTRO = "#F5A623"

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:wght@400;600&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans', sans-serif; }}
    .stApp {{ background-color: #F4F7FB; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(175deg, {TJAP_BLUE} 0%, #0B2060 100%);
    }}
    [data-testid="stSidebar"] * {{
        font-family: 'IBM Plex Sans', sans-serif !important;
    }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div.stMarkdown {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {{
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] *,
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] * {{
        color: #1E293B !important;
        background-color: white !important;
    }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{
        color: rgba(255,255,255,0.5) !important;
    }}

    /* FIX 1: logo com fundo branco limpo */
    .logo-box {{
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.18);
    }}

    /* KPI cards */
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.07);
        border-left: 5px solid {TJAP_BLUE};
        margin-bottom: 8px;
    }}
    .kpi-card.green  {{ border-left-color: {TJAP_GREEN}; }}
    .kpi-card.yellow {{ border-left-color: {TJAP_YELLOW}; }}
    .kpi-card.red    {{ border-left-color: #D94F3D; }}
    .kpi-title {{
        font-size: 0.68rem; color: {TJAP_GRAY}; text-transform: uppercase;
        letter-spacing: .09em; margin-bottom: 5px; font-weight: 600;
    }}
    .kpi-value {{
        font-size: 1.9rem; font-weight: 700; color: {TJAP_BLUE}; line-height: 1;
        font-family: 'IBM Plex Serif', serif;
    }}
    .kpi-value.green {{ color: {TJAP_GREEN}; }}
    .kpi-value.red   {{ color: #D94F3D; }}
    .kpi-sub {{ font-size: 0.72rem; color: {TJAP_GRAY}; margin-top: 5px; }}

    /* Cabeçalho de seção */
    .section-header {{
        font-size: 0.78rem; font-weight: 700; color: {TJAP_BLUE};
        text-transform: uppercase; letter-spacing: 0.09em;
        border-bottom: 2px solid {TJAP_GREEN};
        padding-bottom: 5px; margin: 24px 0 14px 0;
    }}

    /* FIX 3+7: Tabs – negrito, borda grossa e cor amarela TJAP na aba ativa */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 2px solid #E2E8F0;
        gap: 0px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.84rem;
        font-weight: 700;
        color: #64748B;
        padding: 12px 20px 12px;
        letter-spacing: 0.02em;
        border-bottom: 4px solid transparent;
        transition: color 0.2s, border-color 0.2s;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: {TJAP_YELLOW} !important;
        background: rgba(245,197,24,0.06) !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {TJAP_YELLOW} !important;
        border-bottom: 4px solid {TJAP_YELLOW} !important;
        background: rgba(245,197,24,0.06) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {TJAP_YELLOW} !important;
        height: 4px !important;
    }}
    .stTabs [data-baseweb="tab-border"] {{
        background-color: #E2E8F0 !important;
        height: 2px !important;
    }}

    /* FIX 6: Tooltip profissional (hoverlabel global via CSS) */
    .js-plotly-plot .plotly .hoverlabel {{
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 13px !important;
        border-radius: 8px !important;
    }}

    /* FIX 2: Remover tooltip do botão de colapso da sidebar */
    [data-testid="collapsedControl"] {{
        pointer-events: none;
    }}
    button[title="keyboard_double_arrow_right"],
    button[title="keyboard_double_arrow_left"] {{
        display: none !important;
    }}
    [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ─── Logo ─────────────────────────────────────────────────────────────────────
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE       = Path(__file__).parent
logo_clean = BASE / "logo_tjap_clean.png"
logo_orig  = BASE / "logo_tjap.png"
logo_path  = logo_clean if logo_clean.exists() else logo_orig

# ─── Carrega dados ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel(BASE / "pesquisa.xlsx")
    df["Carimbo de data/hora"] = pd.to_datetime(df["Carimbo de data/hora"])
    df["Ano"] = df["Carimbo de data/hora"].dt.year
    df["Mês"] = df["Carimbo de data/hora"].dt.month

    df = df.rename(columns={
        "Carimbo de data/hora": "timestamp",
        "Gênero do entrevistado:": "genero",
        "Faixa etária:": "faixa_etaria",
        "Grau de instrução:": "instrucao",
        "Renda familiar em Salários-Mínimos:": "renda",
        "Você se enquadra em qual dos perfis abaixo?": "perfil",
        "Responde de qual Comarca/Município?": "comarca",
        "De que forma você buscou atendimento ou utilizou os serviços do Tribunal?": "canal",
        "SE O ATENDIMENTO FOI PRESENCIAL: \n\nO tempo de espera e a informação prestada foram adequados?": "presencial_ok",
        "SE O ATENDIMENTO FOI POR BALCÃO VIRTUAL (ZOOM), WHATSAPP, E-MAIL OU CELULAR:\nFoi fácil acessar e utilizar o canal e ser atendido?": "virtual_ok",
        "SE ACESSOU O PORTAL/SITE:\nVocê encontrou o que precisava com facilidade e clareza nas informações? ": "portal_ok",
        "Você acompanha as informações dos serviços oferecidos pela Justiça do Amapá, por meio das redes sociais do TJAP (Instagram, Facebook, YouTube, WebRádio, X, BlueSky e Flickr)? ": "acompanha_redes",
        "Você está satisfeito com os conteúdos e informações dos serviços oferecidos pela Justiça do Amapá, por meio das redes sociais do TJAP (Instagram, Facebook, YouTube, WebRádio, X, BlueSky e Flickr)? ": "satisfeito_redes",
        "Você acha que o TJAP implementa adaptações dos espaços físicos que permitam a acessibilidade e a livre movimentação, com independência e segurança, da pessoa com deficiência? ": "acessibilidade_fisica",
        "O Portal do TJAP garante às pessoas com deficiência o pleno acesso às informações disponíveis?": "acessibilidade_portal",
        "Você está satisfeito(a) com o atendimento oferecido pela Justiça do Amapá?": "satisfeito_atendimento",
        "Você confia na Justiça do Amapá?": "confianca",
    })

    # FIX 5: Macapá e Bailique eram coletadas juntas no formulário;
    # exibimos com asterisco e nota explicativa.
    df["comarca"] = df["comarca"].str.replace(
        "Macapá/Bailique", "Macapá / Bailique (*)", regex=False
    )
    return df

df_all = load_data()
anos_disponiveis = sorted([int(a) for a in df_all["Ano"].unique()])

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    if logo_path.exists():
        st.markdown(
            f'<div class="logo-box"><img src="data:image/png;base64,{img_to_b64(logo_path)}" width="150"/></div>',
            unsafe_allow_html=True,
        )
    st.markdown("### Filtro")
    ano_sel = st.multiselect("Ano", anos_disponiveis, default=anos_disponiveis,
                             format_func=lambda x: str(x))
    st.markdown("---")
    st.caption("Desenvolvido pela Secretaria de Planejamento\nTribunal de Justiça do Estado do Amapá")

# ─── Filtra por ano ──────────────────────────────────────────────────────────
df = df_all[df_all["Ano"].isin(ano_sel)].copy()

total    = len(df)
color_map = {"Sim": TJAP_GREEN, "Não": COLOR_NAO, "Não sei responder": COLOR_NEUTRO}

def pct(col, val="Sim"):
    if total == 0: return 0
    return round(df[col].eq(val).sum() / total * 100, 1)

def cell_color(val):
    """FIX 3 & 4: colore células sem usar matplotlib."""
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        return ""
    bg = "#dcfce7" if val >= 80 else "#fef9c3" if val >= 60 else "#fee2e2"
    return f"background-color:{bg}; font-weight:600; color:#1E293B"

FONT_CFG  = dict(family="IBM Plex Sans")
HOVER_CFG = dict(
    bgcolor="#FFFFFF",
    bordercolor=TJAP_BLUE,
    font=dict(family="IBM Plex Sans", size=13, color="#1E293B"),
    namelength=-1,
)

def add_meta_line(fig, orientation="v"):
    """FIX 2: linha de meta azul escuro, destaque e anotação visível."""
    kw = dict(
        line_dash="dash", line_color=TJAP_BLUE, line_width=2,
        annotation_text="<b>Meta: 80%</b>",
        annotation_font=dict(color=TJAP_BLUE, size=13, family="IBM Plex Sans"),
        annotation_bgcolor="rgba(232,240,255,0.92)",
        annotation_bordercolor=TJAP_BLUE,
        annotation_borderwidth=1,
        annotation_position="top right",
    )
    if orientation == "v":
        fig.add_hline(y=80, **kw)
    else:
        fig.add_vline(x=80, **kw)

# ─── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(90deg,{TJAP_BLUE},{TJAP_GREEN});
     border-radius:12px; padding:20px 28px; margin-bottom:18px; color:white;">
  <div style="font-size:1.4rem; font-weight:700; font-family:'IBM Plex Serif',serif;">
    Dashboard de Satisfação do Jurisdicionado
  </div>
  <div style="font-size:0.85rem; opacity:.85; margin-top:4px;">
    Tribunal de Justiça do Estado do Amapá &nbsp;|&nbsp; Pesquisa Institucional
  </div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ────────────────────────────────────────────────────────────────────
p_satisf    = pct("satisfeito_atendimento")
p_confianca = pct("confianca")

# Cálculo correto: canal contém X AND coluna de adequação específica = Sim / total
def pct_canal(canal_str, col_ok):
    """% de satisfação ENTRE os usuários do canal (denominador = usuários do canal)."""
    mask_canal = df["canal"].str.contains(canal_str, na=False)
    denom = mask_canal.sum()
    if denom == 0: return 0
    numer = (mask_canal & df[col_ok].eq("Sim")).sum()
    return round(numer / denom * 100, 1)

p_pres    = pct_canal("Presencial",  "presencial_ok")
p_virtual = pct_canal("Virtual",            "virtual_ok")  # "Virtual" é o valor na col I
p_portal  = pct_canal("Portal/site", "portal_ok")

def kpi(col, title, value, sub, color=""):
    with col:
        st.markdown(f"""<div class="kpi-card {color}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value {color}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi(k1, "Total de Respostas",   f"{total:,}".replace(",","."), "respondentes", "")
kpi(k2, "Satisfação Geral",     f"{p_satisf}%",    "satisfeitos com o atendimento",   "green")
kpi(k3, "Índice de Confiança",  f"{p_confianca}%", "confiam na Justiça do AP",        "green")
kpi(k4, "Atend. Presencial",    f"{p_pres}%",      "entre usuários do canal",    "" if p_pres>=70 else "red")
kpi(k5, "Balcão Virtual",       f"{p_virtual}%",   "entre usuários do canal",    "" if p_virtual>=70 else "red")
kpi(k6, "Portal / Site",        f"{p_portal}%",    "entre usuários do canal",    "" if p_portal>=70 else "red")

st.markdown("---")

# ─── Abas ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visão Geral", "Perfil dos Respondentes",
    "Canais de Atendimento", "Comparativo Anual", "Conclusão",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Visão Geral
# ══════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">Satisfação com o Atendimento</div>', unsafe_allow_html=True)
        vc = df["satisfeito_atendimento"].value_counts().reset_index()
        vc.columns = ["Resposta","Qtd"]
        fig = px.pie(vc, names="Resposta", values="Qtd", hole=0.55,
                     color="Resposta", color_discrete_map=color_map)
        fig.update_traces(textposition="outside", textinfo="percent+label", textfont=FONT_CFG)
        fig.update_layout(margin=dict(t=20,b=20,l=0,r=0), showlegend=True,
                          legend=dict(orientation="h", yanchor="bottom", y=-0.18, font=FONT_CFG),
                          font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_1")

    with c2:
        st.markdown('<div class="section-header">Confia na Justiça do Amapá?</div>', unsafe_allow_html=True)
        vc2 = df["confianca"].value_counts().reset_index()
        vc2.columns = ["Resposta","Qtd"]
        fig2 = px.pie(vc2, names="Resposta", values="Qtd", hole=0.55,
                      color="Resposta", color_discrete_map=color_map)
        fig2.update_traces(textposition="outside", textinfo="percent+label", textfont=FONT_CFG)
        fig2.update_layout(margin=dict(t=20,b=20,l=0,r=0), showlegend=True,
                           legend=dict(orientation="h", yanchor="bottom", y=-0.18, font=FONT_CFG),
                           font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig2, use_container_width=True, key="chart_2")

    # FIX 2: Indicadores Estratégicos com linha de meta visível
    st.markdown('<div class="section-header">Indicadores Estratégicos vs. Meta de 80%</div>', unsafe_allow_html=True)
    indicadores = {
        "Satisfação com Atendimento":     pct("satisfeito_atendimento"),
        "Confiança na Justiça AP":        pct("confianca"),
        "Acompanha Redes Sociais":        pct("acompanha_redes"),
        "Satisfeito com Redes Sociais":   pct("satisfeito_redes"),
        "Acessibilidade Física":          pct("acessibilidade_fisica"),
        "Acessibilidade Portal Web":      pct("acessibilidade_portal"),
        "Atend. Presencial — Satisfação": p_pres,      # 92.7%
        "Balcão Virtual — Satisfação":    p_virtual,   # 85.7%
        "Portal / Site — Satisfação":     p_portal,    # 88.1%
    }
    ind_df = pd.DataFrame(list(indicadores.items()), columns=["Indicador","% Sim"])
    ind_df = ind_df.sort_values("% Sim")
    bar_colors = [TJAP_GREEN if v>=80 else TJAP_YELLOW if v>=60 else COLOR_NAO for v in ind_df["% Sim"]]

    fig3 = go.Figure(go.Bar(
        x=ind_df["% Sim"], y=ind_df["Indicador"],
        orientation="h",
        marker_color=bar_colors,
        text=[f"{v}%" for v in ind_df["% Sim"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Sans", size=13, color="#1A3A8F", weight=700),
    ))
    add_meta_line(fig3, orientation="h")   # linha azul escuro destacada
    fig3.update_layout(
        xaxis=dict(range=[0,118], title=dict(text="% de respostas positivas (Sim)", font=FONT_CFG)),
        yaxis=dict(title="", tickfont=dict(family="IBM Plex Sans", size=12)),
        margin=dict(l=10, r=20, t=20, b=20),
        height=390,
        plot_bgcolor="white", paper_bgcolor="white",
        font=FONT_CFG, hoverlabel=HOVER_CFG,
    )
    st.plotly_chart(fig3, use_container_width=True, key="chart_3")

    st.markdown('<div class="section-header">Evolução de Respostas no Período</div>', unsafe_allow_html=True)
    df_time = df.groupby(df["timestamp"].dt.date).size().reset_index(name="Respostas")
    df_time.columns = ["Data","Respostas"]
    fig4 = px.area(df_time, x="Data", y="Respostas", color_discrete_sequence=[TJAP_BLUE])
    fig4.update_traces(fill="tozeroy", line_color=TJAP_BLUE, fillcolor="rgba(26,58,143,0.14)")
    fig4.update_layout(margin=dict(t=10,b=20,l=0,r=0),
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis=dict(title=""), yaxis=dict(title="Qtd. de Respostas"),
                       font=FONT_CFG, hoverlabel=HOVER_CFG)
    st.plotly_chart(fig4, use_container_width=True, key="chart_4")

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Perfil dos Respondentes
# ══════════════════════════════════════════════════════════════════════
with tab2:
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown('<div class="section-header">Gênero</div>', unsafe_allow_html=True)
        g = df["genero"].value_counts().reset_index(); g.columns = ["Gênero","Qtd"]
        fig = px.bar(g, x="Gênero", y="Qtd", color="Gênero", text="Qtd",
                     color_discrete_sequence=[TJAP_BLUE, TJAP_GREEN, TJAP_YELLOW, TJAP_GRAY])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=0,r=0),
                          plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_5")

    with r1c2:
        st.markdown('<div class="section-header">Faixa Etária</div>', unsafe_allow_html=True)
        fe = df["faixa_etaria"].value_counts().reset_index(); fe.columns = ["Faixa","Qtd"]
        order = ["18 a 24 anos","25 a 34 anos","35 a 44 anos","45 a 59 anos","60 anos ou +"]
        fe["Faixa"] = pd.Categorical(fe["Faixa"], categories=order, ordered=True)
        fe = fe.sort_values("Faixa")
        fig = px.bar(fe, x="Faixa", y="Qtd", text="Qtd",
                     color_discrete_sequence=[TJAP_GREEN])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=0,r=0),
                          plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_6")

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown('<div class="section-header">Grau de Instrução</div>', unsafe_allow_html=True)
        gi = df["instrucao"].value_counts().reset_index(); gi.columns = ["Instrução","Qtd"]
        fig = px.pie(gi, names="Instrução", values="Qtd",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=10,b=10,l=0,r=0), showlegend=False, font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_7")

    with r2c2:
        st.markdown('<div class="section-header">Renda Familiar (Salários Mínimos)</div>', unsafe_allow_html=True)
        ri = df["renda"].value_counts().reset_index(); ri.columns = ["Renda","Qtd"]
        order_r = ["Até 2 SM","Entre 2 a 4 SM","Entre 4 a 10 SM",
                   "Entre 10 a 20 SM","Acima de 20 SM","Não quer responder"]
        ri["Renda"] = pd.Categorical(ri["Renda"], categories=order_r, ordered=True)
        ri = ri.sort_values("Renda")
        fig = px.bar(ri, x="Qtd", y="Renda", orientation="h", text="Qtd",
                     color_discrete_sequence=[TJAP_BLUE])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=0,r=0),
                          plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_8")

    st.markdown('<div class="section-header">Perfil dos Respondentes</div>', unsafe_allow_html=True)
    pr = df["perfil"].value_counts().reset_index(); pr.columns = ["Perfil","Qtd"]
    pr["Pct"] = (pr["Qtd"] / pr["Qtd"].sum() * 100).round(1)
    fig = px.bar(pr, x="Qtd", y="Perfil", orientation="h",
                 color="Qtd", color_continuous_scale=[[0,TJAP_LIGHT],[1,TJAP_BLUE]],
                 text=pr["Pct"].apply(lambda v: f"{v}%"))
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      margin=dict(t=10,b=10,l=0,r=0),
                      plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG)
    st.plotly_chart(fig, use_container_width=True, key="chart_9")

    st.markdown('<div class="section-header">Satisfação por Gênero</div>', unsafe_allow_html=True)
    cross = df.groupby("genero")["satisfeito_atendimento"].value_counts(normalize=True).mul(100).round(1).reset_index()
    cross.columns = ["Gênero","Resposta","Pct"]
    fig = px.bar(cross, x="Gênero", y="Pct", color="Resposta",
                 color_discrete_map=color_map, barmode="group",
                 text=cross["Pct"].apply(lambda v: f"{v}%"))
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_title="% de Respondentes",
                      margin=dict(t=10,b=10,l=0,r=0),
                      plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG)
    st.plotly_chart(fig, use_container_width=True, key="chart_10")

    # FIX 4: Tabela sem matplotlib
    st.markdown('<div class="section-header">Resumo por Grau de Instrução</div>', unsafe_allow_html=True)
    resumo = (
        df.groupby("instrucao").agg(
            Respondentes=("genero","count"),
            Satisfacao=("satisfeito_atendimento", lambda s: round((s=="Sim").sum()/len(s)*100,1)),
            Confianca  =("confianca",              lambda s: round((s=="Sim").sum()/len(s)*100,1)),
        ).reset_index()
        .rename(columns={"instrucao":"Grau de Instrução","Satisfacao":"Satisfação (%)","Confianca":"Confiança (%)"})
        .sort_values("Respondentes", ascending=False)
    )
    st.dataframe(
        resumo.style
            .map(cell_color, subset=["Satisfação (%)","Confiança (%)"])
            .format({"Satisfação (%)":"{:.1f}%","Confiança (%)":"{:.1f}%"}),
        use_container_width=True, hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Canais de Atendimento
# ══════════════════════════════════════════════════════════════════════
with tab3:

    # ── Análise por Teoria dos Conjuntos ──────────────────────────────────
    st.markdown('<div class="section-header">Análise de Canais — Teoria dos Conjuntos</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0F4FF;border-left:4px solid #1A3A8F;border-radius:8px;
                padding:12px 18px;margin-bottom:16px;font-size:0.82rem;color:#1E293B;line-height:1.6;">
      <b>Nota metodológica:</b> Respondentes que marcaram combinações de canais (ex.: "Presencial, Virtual")
      utilizaram <b>ambos os canais</b> — não representam um grupo separado. A análise abaixo aplica
      a teoria dos conjuntos para contabilizar o alcance real de cada canal, incluindo os usos combinados.
    </div>
    """, unsafe_allow_html=True)

    # Calcular conjuntos
    def _parse_canal(v):
        if pd.isna(v): return []
        return [c.strip() for c in str(v).split(",")]

    _cp  = df["canal"].apply(_parse_canal)
    _P   = _cp.apply(lambda x: "Presencial"  in x)
    _V   = _cp.apply(lambda x: "Virtual"            in x)
    _S   = _cp.apply(lambda x: "Portal/site" in x)
    _n   = max(len(df), 1)

    _only_P   = (_P & ~_V & ~_S).sum()
    _only_V   = (~_P & _V & ~_S).sum()
    _only_S   = (~_P & ~_V & _S).sum()
    _PV       = (_P & _V & ~_S).sum()
    _PS       = (_P & ~_V & _S).sum()
    _VS       = (~_P & _V & _S).sum()
    _PVS      = (_P & _V & _S).sum()
    _tot_P    = _P.sum()
    _tot_V    = _V.sum()
    _tot_S    = _S.sum()

    # KPIs de alcance
    ka, kb, kc, kd = st.columns(4)
    def _kstat(col, label, val, sub, color=""):
        with col:
            st.markdown(f"""<div class="kpi-card {color}">
                <div class="kpi-title">{label}</div>
                <div class="kpi-value {color}">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)
    _kstat(ka, "Usaram Presencial",  f"{_tot_P} ({_tot_P/_n*100:.1f}%)", "incluindo combinações", "")
    _kstat(kb, "Usaram Balcão Virtual",     f"{_tot_V} ({_tot_V/_n*100:.1f}%)", "incluindo combinações", "")
    _kstat(kc, "Usaram Portal/site", f"{_tot_S} ({_tot_S/_n*100:.1f}%)", "incluindo combinações", "")
    _kstat(kd, "Usaram 2+ Canais",   f"{_PV+_PS+_VS+_PVS} ({(_PV+_PS+_VS+_PVS)/_n*100:.1f}%)", "multicanal", "green")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Gráfico 1: Alcance total por canal (barras empilhadas: exclusivo + compartilhado)
    ca_left, ca_right = st.columns(2)
    with ca_left:
        st.markdown('<div class="section-header">Alcance por Canal (com sobreposições)</div>', unsafe_allow_html=True)
        canais_nomes = ["Presencial", "Balcão Virtual", "Portal/site"]
        excl  = [_only_P, _only_V, _only_S]
        combi = [_tot_P - _only_P, _tot_V - _only_V, _tot_S - _only_S]

        fig_conj = go.Figure()
        fig_conj.add_trace(go.Bar(
            name="Uso exclusivo", x=canais_nomes, y=excl,
            marker_color=TJAP_BLUE, text=excl,
            textposition="inside", textfont=dict(color="white", family="IBM Plex Sans", size=12),
            hovertemplate="<b>%{x}</b> — Uso exclusivo<br>Respondentes: <b>%{y}</b><extra></extra>",
        ))
        fig_conj.add_trace(go.Bar(
            name="Uso combinado", x=canais_nomes, y=combi,
            marker_color=TJAP_YELLOW, text=combi,
            textposition="inside", textfont=dict(color="#1E293B", family="IBM Plex Sans", size=12),
            hovertemplate="<b>%{x}</b> — Uso combinado<br>Respondentes: <b>%{y}</b><extra></extra>",
        ))
        fig_conj.update_layout(
            barmode="stack", plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(t=10,b=10,l=0,r=0), height=300,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=FONT_CFG),
            font=FONT_CFG, hoverlabel=HOVER_CFG,
            yaxis=dict(title="Respondentes", gridcolor="#F1F5F9"),
            xaxis=dict(title=""),
        )
        st.plotly_chart(fig_conj, use_container_width=True, key="chart_conjuntos_alcance")

    with ca_right:
        st.markdown('<div class="section-header">Distribuição das Combinações</div>', unsafe_allow_html=True)
        combos_labels = [
            "Somente Presencial", "Somente Balcão Virtual", "Somente Portal/site",
            "Presencial + Balcão Virtual", "Presencial + Portal", "Virtual + Portal",
            "Presencial + Balcão Virtual + Portal",
        ]
        combos_vals = [_only_P, _only_V, _only_S, _PV, _PS, _VS, _PVS]
        combos_pct  = [round(v/_n*100,1) for v in combos_vals]
        combos_colors = [TJAP_BLUE, "#4A90D9", "#7CB9E8",
                         TJAP_GREEN, "#2ECC71", TJAP_YELLOW, COLOR_NAO]

        fig_combos = go.Figure(go.Bar(
            x=combos_vals, y=combos_labels, orientation="h",
            marker_color=combos_colors,
            text=[f"{v} ({p}%)" for v,p in zip(combos_vals, combos_pct)],
            textposition="outside",
            textfont=dict(family="IBM Plex Sans", size=11, color="#1E293B"),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Respondentes: <b>%{x}</b><br>"
                "Percentual: <b>%{customdata}%</b><extra></extra>"
            ),
            customdata=combos_pct,
        ))
        fig_combos.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(t=10,b=10,l=0,r=0), height=300,
            font=FONT_CFG, hoverlabel=HOVER_CFG,
            xaxis=dict(title="Respondentes", gridcolor="#F1F5F9"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig_combos, use_container_width=True, key="chart_conjuntos_combos")

    # Tabela-resumo de teoria dos conjuntos

    st.markdown('<div class="section-header">Satisfação por Canal — Três Conjuntos Base</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0F4FF;border-left:4px solid #1A3A8F;border-radius:8px;
                padding:10px 16px;margin-bottom:14px;font-size:0.8rem;color:#1E293B;">
      Cada respondente que utilizou determinado canal — isoladamente ou em combinação —
      é contabilizado no respectivo conjunto. Um mesmo respondente pode aparecer em
      mais de um canal.
    </div>
    """, unsafe_allow_html=True)

    # Satisfação por canal — usando coluna específica de cada canal (metodologia correta)
    _canal_cols = {
        "Presencial":    ("presencial_ok", _P),
        "Balcão Virtual": ("virtual_ok",   _V),
        "Portal/site":   ("portal_ok",     _S),
    }
    _registros = []
    for _canal_base, (_col_ok, _flag) in _canal_cols.items():
        _sub = df[_flag]
        _sub_ok = _sub[_col_ok].dropna()
        _n_base = len(_sub_ok)
        for _resp in ["Sim", "Não", "Não sei responder"]:
            _qtd = (_sub_ok == _resp).sum()
            if _qtd > 0:
                _registros.append({
                    "Canal": _canal_base,
                    "Resposta": _resp,
                    "Pct": round(_qtd / _n_base * 100, 1),
                    "Qtd": _qtd,
                })
    cross_base = pd.DataFrame(_registros)

    fig_sat_canal = px.bar(
        cross_base, x="Canal", y="Pct", color="Resposta",
        color_discrete_map=color_map, barmode="stack",
        text=cross_base["Pct"].apply(lambda v: f"{v}%"),
        custom_data=["Qtd"],
    )
    fig_sat_canal.update_traces(
        textposition="inside",
        hovertemplate=(
            "<b>%{x}</b> — %{fullData.name}<br>"
            "Percentual: <b>%{y}%</b><br>"
            "Respondentes: <b>%{customdata[0]}</b><extra></extra>"
        ),
    )
    fig_sat_canal.update_layout(
        yaxis=dict(title="% de Respondentes", range=[0,105], gridcolor="#F1F5F9"),
        xaxis=dict(title=""),
        margin=dict(t=10,b=10,l=0,r=0),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=FONT_CFG),
        font=FONT_CFG, hoverlabel=HOVER_CFG,
    )
    st.plotly_chart(fig_sat_canal, use_container_width=True, key="chart_satisf_canal_base")

    st.markdown('<div class="section-header">Redes Sociais do TJAP</div>', unsafe_allow_html=True)
    rs1, rs2 = st.columns(2)
    with rs1:
        st.markdown("**Acompanha as Redes Sociais?**")
        vc = df["acompanha_redes"].value_counts().reset_index(); vc.columns = ["Resp","Qtd"]
        fig = px.pie(vc, names="Resp", values="Qtd", hole=0.5,
                     color="Resp", color_discrete_map=color_map)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=10,b=10,l=0,r=0), showlegend=False, font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_17")
    with rs2:
        st.markdown("**Satisfeito com o Conteúdo das Redes?**")
        st.caption("Base: apenas quem acompanha as redes sociais do TJAP")
        _df_acomp = df[df["acompanha_redes"] == "Sim"]
        vc2 = _df_acomp["satisfeito_redes"].value_counts().reset_index(); vc2.columns = ["Resp","Qtd"]
        fig2 = px.pie(vc2, names="Resp", values="Qtd", hole=0.5,
                      color="Resp", color_discrete_map=color_map)
        fig2.update_traces(
            textposition="outside", textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Respondentes: <b>%{value}</b> de {}<br>%{percent}<extra></extra>".format(len(_df_acomp)),
        )
        fig2.update_layout(margin=dict(t=10,b=10,l=0,r=0), showlegend=False, font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig2, use_container_width=True, key="chart_18")

    st.markdown('<div class="section-header">Acessibilidade</div>', unsafe_allow_html=True)
    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown("**Adaptações nos espaços físicos?**")
        vaf = df["acessibilidade_fisica"].value_counts().reset_index(); vaf.columns = ["Resp","Qtd"]
        fig = px.pie(vaf, names="Resp", values="Qtd", hole=0.5,
                     color="Resp", color_discrete_map=color_map)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=10,b=10,l=0,r=0), showlegend=False, font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig, use_container_width=True, key="chart_19")
    with ac2:
        st.markdown("**Acessibilidade no Portal para PCD?**")
        vaw = df["acessibilidade_portal"].value_counts().reset_index(); vaw.columns = ["Resp","Qtd"]
        fig2 = px.pie(vaw, names="Resp", values="Qtd", hole=0.5,
                      color="Resp", color_discrete_map=color_map)
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(margin=dict(t=10,b=10,l=0,r=0), showlegend=False, font=FONT_CFG, hoverlabel=HOVER_CFG)
        st.plotly_chart(fig2, use_container_width=True, key="chart_20")

# ══════════════════════════════════════════════════════════════════════
# TAB 5 — Comparativo Anual
# ══════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Comparativo Anual de Indicadores Estratégicos</div>', unsafe_allow_html=True)

    metricas_anuais = {}
    for ano in sorted(df_all["Ano"].unique()):
        d = df_all[df_all["Ano"] == ano]; n = len(d)
        metricas_anuais[ano] = {
            "Respostas":                   int(n),
            "Satisfação Atendimento (%)":  round((d["satisfeito_atendimento"]=="Sim").sum()/n*100,1) if n else 0,
            "Confiança (%)":               round((d["confianca"]=="Sim").sum()/n*100,1) if n else 0,
            "Presencial OK (%)":           round((d["presencial_ok"]=="Sim").sum()/n*100,1) if n else 0,
            "Balcão Virtual OK (%)":              round((d["virtual_ok"]=="Sim").sum()/n*100,1) if n else 0,
            "Portal OK (%)":               round((d["portal_ok"]=="Sim").sum()/n*100,1) if n else 0,
            "Acompanha Redes (%)":         round((d["acompanha_redes"]=="Sim").sum()/n*100,1) if n else 0,
            "Acessibilidade Física (%)":   round((d["acessibilidade_fisica"]=="Sim").sum()/n*100,1) if n else 0,
        }

    df_anual = pd.DataFrame(metricas_anuais).T.reset_index().rename(columns={"index":"Ano"})
    df_anual["Ano"] = df_anual["Ano"].astype(str)
    cols_metricas = [c for c in df_anual.columns if c not in ("Ano","Respostas")]

    if len(df_anual) == 1:
        st.info(
            f"Os dados disponíveis abrangem apenas o ano {df_anual['Ano'].iloc[0]}. "
            "Ao incluir registros de anos anteriores na planilha, todos os gráficos comparativos "
            "serão gerados automaticamente.",
            icon="ℹ️"
        )

    # FIX 3: Tabela colorida sem matplotlib
    st.markdown("**Tabela Resumo por Ano**")
    st.dataframe(
        df_anual.style
            .map(cell_color, subset=cols_metricas)
            .format({c:"{:.1f}%" for c in cols_metricas} | {"Respostas":"{:.0f}"}),
        use_container_width=True, hide_index=True,
    )

    fig_vol = px.bar(df_anual, x="Ano", y="Respostas",
                     color_discrete_sequence=[TJAP_BLUE], text="Respostas")
    fig_vol.update_traces(textposition="outside")
    fig_vol.update_layout(
        title=dict(text="Volume de Respostas por Ano", font=dict(family="IBM Plex Sans")),
        margin=dict(t=40,b=10,l=0,r=0),
        plot_bgcolor="white", paper_bgcolor="white", font=FONT_CFG, hoverlabel=HOVER_CFG,
    )
    st.plotly_chart(fig_vol, use_container_width=True, key="chart_21")

    st.markdown('<div class="section-header">Radar de Indicadores por Ano</div>', unsafe_allow_html=True)
    radar_cols   = ["Satisfação Atendimento (%)","Confiança (%)","Presencial OK (%)",
                    "Balcão Virtual OK (%)","Portal OK (%)","Acompanha Redes (%)","Acessibilidade Física (%)"]
    radar_labels = ["Satisfação","Confiança","Presencial","Balcão Virtual","Portal","Redes","Acessib."]
    palette_r    = [TJAP_BLUE, TJAP_GREEN, TJAP_YELLOW, COLOR_NAO, "#9B59B6"]

    fig_radar = go.Figure()
    for i, row in df_anual.iterrows():
        vals = [row[c] for c in radar_cols]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=radar_labels+[radar_labels[0]],
            fill="toself", name=str(row["Ano"]),
            line_color=palette_r[i % len(palette_r)],
            fillcolor=palette_r[i % len(palette_r)],
            opacity=0.28,
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        showlegend=True, margin=dict(t=20,b=20,l=20,r=20),
        height=430, font=FONT_CFG, hoverlabel=HOVER_CFG,
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="chart_22")

    st.markdown('<div class="section-header">Evolução dos Indicadores</div>', unsafe_allow_html=True)
    df_long = df_anual.melt(id_vars="Ano", value_vars=radar_cols,
                             var_name="Indicador", value_name="Valor (%)")
    fig_line = px.line(df_long, x="Ano", y="Valor (%)", color="Indicador",
                       markers=True,
                       color_discrete_sequence=[TJAP_BLUE,TJAP_GREEN,TJAP_YELLOW,
                                                COLOR_NAO,"#9B59B6","#F39C12","#1ABC9C"])
    add_meta_line(fig_line, orientation="v")
    fig_line.update_layout(
        yaxis=dict(range=[0,110]),
        margin=dict(t=10,b=10,l=0,r=0),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="top", y=-0.2),
        font=FONT_CFG, hoverlabel=HOVER_CFG,
    )
    st.plotly_chart(fig_line, use_container_width=True, key="chart_23")


# ══════════════════════════════════════════════════════════════════════
# TAB 6 — Conclusão
# ══════════════════════════════════════════════════════════════════════
with tab5:

    # ── Nível de Confiança ──────────────────────────────────────────────
    st.markdown('<div class="section-header">Parâmetros e Nível de Confiança da Pesquisa</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    def kpi_stat(col, label, value, sub):
        with col:
            st.markdown(f"""<div class="kpi-card green">
                <div class="kpi-title">{label}</div>
                <div class="kpi-value green">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    kpi_stat(c1, "Nível de Confiança", "95%", "intervalo de confiança adotado")
    kpi_stat(c2, "Margem de Erro",     "5%",  "erro amostral máximo tolerado")
    kpi_stat(c3, "Amostra Coletada",   "1.743","respondentes efetivos")
    kpi_stat(c4, "Amostra Calculada",  "1.100","tamanho amostral mínimo")

    st.markdown("""
    <div style="background:#F0F4FF;border-left:4px solid #1A3A8F;border-radius:8px;
                padding:16px 20px;margin:16px 0;font-size:0.85rem;color:#1E293B;line-height:1.7;">
      <b>Metodologia:</b> Amostragem estratificada proporcional (alocação de Neyman) com estratos por comarca.
      Universo: 117.951 processos pendentes no estado. P = Q = 0,5 (máxima variância).
      Z = 1,96 (95% de confiança). Margem de erro adotada: <b>5%</b>. Erro amostral apurado: <b>2,96%</b> — muito abaixo da margem estabelecida, reforçando a precisão da pesquisa.
      A amostra coletada (1.743) supera em 58% o mínimo calculado (1.100), reforçando a robustez estatística dos resultados.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Matriz de Prioridades — Pontos de Ação Identificados</div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .matriz-table { width:100%; border-collapse:collapse; font-family:'IBM Plex Sans',sans-serif; font-size:0.82rem; }
    .matriz-table th { background:#1A3A8F; color:white; padding:10px 14px; text-align:left;
                       font-size:0.72rem; text-transform:uppercase; letter-spacing:0.07em; }
    .matriz-table td { padding:9px 14px; border-bottom:1px solid #F1F5F9; vertical-align:middle; }
    .matriz-table tr:hover td { background:#F8FAFC; }
    .badge-critica  { background:#fee2e2; color:#7F1D1D; border-radius:99px; padding:3px 10px; font-weight:700; font-size:0.72rem; white-space:nowrap; }
    .badge-alta     { background:#dbeafe; color:#1E3A8A; border-radius:99px; padding:3px 10px; font-weight:700; font-size:0.72rem; white-space:nowrap; }
    .badge-media    { background:#fef9c3; color:#78350F; border-radius:99px; padding:3px 10px; font-weight:700; font-size:0.72rem; white-space:nowrap; }
    .badge-baixa    { background:#dcfce7; color:#14532D; border-radius:99px; padding:3px 10px; font-weight:700; font-size:0.72rem; white-space:nowrap; }
    .desemp-red     { color:#991B1B; font-weight:700; }
    .desemp-yellow  { color:#92400E; font-weight:700; }
    .desemp-green   { color:#166534; font-weight:700; }
    </style>
    <table class="matriz-table">
      <thead><tr>
        <th>#</th>
        <th>Indicador / Área de Atenção</th>
        <th>Desempenho</th>
        <th>Prioridade</th>
        <th>Ação Recomendada</th>
      </tr></thead>
      <tbody>
        <tr>
          <td><b>1</b></td>
          <td><b>Acessibilidade do Portal (PCD)</b></td>
          <td><span class="desemp-red">69,8%</span></td>
          <td><span class="badge-alta">Alta</span></td>
          <td>Auditoria WCAG 2.1 AA + integração Rybená + testes com público vulnerável</td>
        </tr>
        <tr>
          <td><b>2</b></td>
          <td><b>Engajamento nas Redes Sociais</b></td>
          <td><span class="desemp-red">74,0%</span></td>
          <td><span class="badge-alta">Alta</span></td>
          <td>Campanha de comunicação para público não digitalizado, com ênfase em rádio e canais comunitários</td>
        </tr>
        <tr>
          <td><b>3</b></td>
          <td><b>Acessibilidade Física dos Espaços</b></td>
          <td><span class="desemp-red">78,8%</span></td>
          <td><span class="badge-media">Média</span></td>
          <td>Incorporação às obras do Plano de Obras (ABNT NBR 9050 / Lei 13.146/2015), conforme disponibilidade orçamentária</td>
        </tr>
        <tr>
          <td><b>4</b></td>
          <td><b>Satisfação dos Advogados</b></td>
          <td><span class="desemp-red">78,9%</span></td>
          <td><span class="badge-media">Média</span></td>
          <td>Grupo de trabalho com OAB-AP para mapeamento de gargalos processuais e de sistemas</td>
        </tr>
        <tr>
          <td><b>5</b></td>
          <td><b>Balcão Virtual (Zoom/WhatsApp/E-mail)</b></td>
          <td><span class="desemp-yellow">85,7%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Revisão dos fluxos de atendimento virtual e padronização de SLA; ampliação da capacitação dos servidores</td>
        </tr>
        <tr>
          <td><b>6</b></td>
          <td><b>Comarcas Remotas — Oiapoque e Calçoene</b></td>
          <td><span class="desemp-yellow">~83%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Diagnóstico qualitativo in loco e plano de melhoria específico para comarcas de fronteira</td>
        </tr>
        <tr>
          <td><b>7</b></td>
          <td><b>Portal / Site — Satisfação</b></td>
          <td><span class="desemp-yellow">88,1%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Ampliação do Projeto 60+, integração Rybená e testes de usabilidade com grupos de baixa escolaridade e 45+ anos</td>
        </tr>
        <tr>
          <td><b>8</b></td>
          <td><b>Confiança Institucional</b></td>
          <td><span class="desemp-green">88,0%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Ampliar presença digital e comunicação institucional para os 24,4% que não acompanham redes</td>
        </tr>
        <tr>
          <td><b>9</b></td>
          <td><b>Satisfação Geral com Atendimento</b></td>
          <td><span class="desemp-green">90,1%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Manter padrão de atendimento presencial; monitorar nos próximos ciclos</td>
        </tr>
        <tr>
          <td><b>10</b></td>
          <td><b>Atend. Presencial — Satisfação</b></td>
          <td><span class="desemp-green">92,7%</span></td>
          <td><span class="badge-baixa">Manutenção</span></td>
          <td>Manter e replicar as boas práticas do atendimento presencial nos demais canais</td>
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color:{TJAP_GRAY}; font-size:0.78rem; font-family:'IBM Plex Sans',sans-serif; line-height:1.8;">
  Tribunal de Justiça do Estado do Amapá &nbsp;|&nbsp;
  Pesquisa de Satisfação do Jurisdicionado &nbsp;|&nbsp;
  Dashboard Estratégico &nbsp;&middot;&nbsp; {pd.Timestamp.now().year}<br/>
  <span style="font-size:0.72rem; color:#94A3B8;">
    Desenvolvido pela Secretaria de Planejamento do TJAP
  </span>
</div>
""", unsafe_allow_html=True)
