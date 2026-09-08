import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de la interfaz
st.set_page_config(
    page_title="SAO Cardinal Core // Stats",
    page_icon="⚔️",
    layout="wide"
)

# 2. Inyección de CSS personalizado para emular la UI de Sword Art Online
st.markdown("""
<style>
    /* Estilo para las tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: rgba(10, 16, 26, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-left: 4px solid #00f0ff;
        padding: 10px 15px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 240, 255, 0.2);
        border-color: #00f0ff;
    }
    /* Estilo para el nombre de la métrica (Fuerza, Velocidad, etc.) */
    div[data-testid="metric-container"] label {
        color: #00f0ff !important;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    /* Título principal con resplandor */
    h1 {
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 3. Datos del lore y estadísticas canónicas
combatientes = {
    "Kirito": {
        "tier": "Tier S+ (God / Anomaly)",
        "score": 98.4,
        "role": "Dual Blades Wielder",
        "stats": {"Fuerza": 96, "Velocidad": 99, "Voluntad": 98, "Rango": 72, "Técnica": 97, "Durabilidad": 92},
        "desc": "El héroe de Aincrad. Su control del Incarnation System en Underworld desafía los límites del universo virtual."
    },
    "Asuna": {
        "tier": "Tier S (Goddess Stacia)",
        "score": 94.2,
        "role": "Líder de Asalto",
        "stats": {"Fuerza": 88, "Velocidad": 98, "Voluntad": 94, "Rango": 80, "Técnica": 96, "Durabilidad": 90},
        "desc": "Conocida como el Destello Veloz. Como la Diosa Stacia, posee la autoridad del sistema para alterar el terreno geográfico a voluntad."
    },
    "Sinon": {
        "tier": "Tier S- (Goddess Solus)",
        "score": 89.8,
        "role": "Sniper Élite",
        "stats": {"Fuerza": 82, "Velocidad": 91, "Voluntad": 91, "Rango": 100, "Técnica": 95, "Durabilidad": 84},
        "desc": "Tiradora suprema. La cuenta de la Diosa Solus le otorga vuelo táctico y poder de bombardeo orbital masivo."
    },
    "Eugeo": {
        "tier": "Tier A+ (High Knight)",
        "score": 87.5,
        "role": "Caballero de Underworld",
        "stats": {"Fuerza": 87, "Velocidad": 86, "Voluntad": 93, "Rango": 85, "Técnica": 88, "Durabilidad": 89},
        "desc": "Discípulo del estilo Aincrad. Su afinidad con la Blue Rose Sword le permite congelar áreas enteras y detener ejércitos."
    }
}

# 4. Cabecera del Dashboard
st.title("⚔️ Cardinal System // Base de Datos")
st.caption("Terminal de evaluación táctica y rendimiento de avatares")

# Selector principal de personaje
char_select = st.selectbox("🎯 SELECCIONAR COMBATIENTE PARA ANÁLISIS:", list(combatientes.keys()))
char_data = combatientes[char_select]

# Ficha de resumen del personaje seleccionado
st.markdown(f"### Perfil: **{char_select}**")
st.markdown(f"**Clasificación:** `{char_data['tier']}` &nbsp;&nbsp; | &nbsp;&nbsp; **Rol:** `{char_data['role']}`")
st.write(char_data['desc'])

# Desglose de Stats en Tarjetas Estilo HUD
st.markdown("#### Atributos de Combate")
cols = st.columns(6)
stats_keys = list(char_data['stats'].keys())

for i, col in enumerate(cols):
    with col:
        st.metric(label=stats_keys[i].upper(), value=char_data['stats'][stats_keys[i]])

st.divider()

# 5. Sección de Gráficos (Comparativa y Radar lado a lado)
col_bar, col_radar = st.columns([1.2, 1])

with col_bar:
    st.subheader("📊 Comparativa Global (Rating)")
    df_power = pd.DataFrame([
        {"Avatar": k, "Rating": v["score"], "Tier": v["tier"]} 
        for k, v in combatientes.items()
    ]).sort_values(by="Rating", ascending=True)

    fig_bar = px.bar(
        df_power,
        x="Rating",
        y="Avatar",
        orientation="h",
        color="Rating",
        color_continuous_scale="Tealgrn",
        text="Tier",
        range_x=[70, 100]
    )
    fig_bar.update_layout(
        template="plotly_dark", 
        height=380, 
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_radar:
    st.subheader(f"⚙️ Escáner Táctico: {char_select}")
    
    # Radar personalizado con Graph Objects (Mucho más bonito visualmente)
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(char_data['stats'].values()),
        theta=list(char_data['stats'].keys()),
        fill='toself',
        fillcolor='rgba(0, 240, 255, 0.25)',
        line=dict(color='#00f0ff', width=2.5),
        marker=dict(color='#00f0ff', size=6),
        name=char_select
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[60, 100],
                gridcolor="rgba(255, 255, 255, 0.1)",
                linecolor="rgba(255, 255, 255, 0.1)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.1)",
                linecolor="rgba(255, 255, 255, 0.1)"
            )
        ),
        showlegend=False,
        template="plotly_dark",
        height=380,
        margin=dict(l=40, r=40, t=30, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)