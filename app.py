import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# 1. Configuración de la interfaz
st.set_page_config(
    page_title="SAO Cardinal Core // AI Tactical Analyzer",
    page_icon="⚔️",
    layout="wide"
)

# 2. Carga en caché del modelo Seq2Seq y Tokenizador explícito
@st.cache_resource
def cargar_modelo_ia():
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("summarization", model=model, tokenizer=tokenizer)

# 3. Datos del lore y estadísticas canónicas
combatientes = {
    "Kirito": {
        "tier": "Tier S+ (God / Anomaly)",
        "score": 98.4,
        "stats": {"Fuerza": 96, "Velocidad": 99, "Voluntad / Hax": 98, "Rango": 72, "Técnica": 97, "Durabilidad": 92},
        "lore_data": (
            "Kazuto Kirigaya, known as Kirito the Black Swordsman, completed the death game of Aincrad by dual-wielding Elucidator and Dark Repulser. "
            "In Project Alicization and the Underworld war, Kirito mastered the Incarnation System to an unprecedented level, transforming mental willpower into absolute reality distortion. "
            "He defeated the Administrator and Gabriel Miller by absorbing the sacred energy of the Night Sky Sword, projecting cosmic-scale blades and temporarily achieving supreme godly authority in the virtual universe."
        )
    },
    "Asuna": {
        "tier": "Tier S (Goddess Stacia)",
        "score": 94.2,
        "stats": {"Fuerza": 88, "Velocidad": 98, "Voluntad / Hax": 94, "Rango": 80, "Técnica": 96, "Durabilidad": 90},
        "lore_data": (
            "Asuna Yuuki served as the sub-leader of the Knights of the Blood Oath, earning the title The Flash for her blistering rapier thrusts using Lambent Light. "
            "During the Underworld foreign invasion, she logged into the super-account of Creation Goddess Stacia, wielding the divine power to manipulate geographical terrain, split tectonic plates, and command virtual armies while retaining infinite hit points."
        )
    },
    "Sinon": {
        "tier": "Tier S- (Goddess Solus)",
        "score": 89.8,
        "stats": {"Fuerza": 82, "Velocidad": 91, "Voluntad / Hax": 91, "Rango": 100, "Técnica": 95, "Durabilidad": 84},
        "lore_data": (
            "Shino Asada is the elite sniper of Gun Gale Online utilizing the heavy antimaterial sniper rifle PGM Ultima Ratio Hecate II. "
            "In Underworld, she claimed the account of Sun Goddess Solus, giving her continuous supersonic flight and the unique ability to convert unlimited solar thermal radiation into devastating long-range orbital energy bombardments."
        )
    },
    "Eugeo": {
        "tier": "Tier A+ (High Knight)",
        "score": 87.5,
        "stats": {"Fuerza": 87, "Velocidad": 86, "Voluntad / Hax": 93, "Rango": 85, "Técnica": 88, "Durabilidad": 89},
        "lore_data": (
            "Eugeo was an Integrity Knight apprentice and Kirito's sworn brother who mastered the Aincrad sword style in Norlangarth. "
            "Empowering the legendary Blue Rose Sword, Eugeo can unleash wide-area cryokinetic sacred arts that freeze battalions of enemies solid and transmute their vitality into blooming frost roses before his blade fusion."
        )
    }
}

st.title("⚔️ Cardinal System // Análisis Táctico & Escala de Poder")
st.caption("Módulo de Evaluación de Combate impulsado por Modelos Transformers")

# 4. Métricas y Gráficos Interactivos
col_bar, col_radar = st.columns([1.1, 1])

with col_bar:
    st.subheader("Índice Global de Combate (Rating)")
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
        color_continuous_scale="Darkmint",
        text="Tier",
        range_x=[70, 100]
    )
    fig_bar.update_layout(template="plotly_dark", height=280, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_radar:
    st.subheader("Radar de Atributos Tácticos")
    char_select = st.selectbox("Seleccionar combatiente:", list(combatientes.keys()))
    stats_dict = combatientes[char_select]["stats"]
    
    df_radar = pd.DataFrame(dict(r=list(stats_dict.values()), theta=list(stats_dict.keys())))
    fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
    fig_radar.update_traces(fill='toself', line_color='#00f0ff')
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[60, 100])),
        template="plotly_dark",
        height=260,
        margin=dict(l=30, r=30, t=10, b=10)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# 5. Módulo de Resumen con IA
st.subheader("🤖 Generación de Resumen Táctico (IA)")
st.write("El modelo transformer sintetiza el historial y capacidades de combate registradas en el Cardinal System.")

c1, c2 = st.columns([1.5, 2.5])

with c1:
    personaje_ia = st.selectbox("Personaje a analizar con IA:", list(combatientes.keys()), key="select_ia")
    max_words = st.slider("Longitud máxima (palabras):", 30, 90, 50)
    min_words = st.slider("Longitud mínima (palabras):", 15, 30, 20)
    ejecutar = st.button("Generar Resumen con IA", type="primary")

with c2:
    if ejecutar:
        with st.spinner(f"Cargando modelo y sintetizando capacidades de {personaje_ia}..."):
            resumidor = cargar_modelo_ia()
            lore_text = combatientes[personaje_ia]["lore_data"]
            salida = resumidor(lore_text, max_length=max_words, min_length=min_words, do_sample=False)
            resumen_final = salida[0]['summary_text']
        
        st.success(f"Evaluación completada: {personaje_ia} [{combatientes[personaje_ia]['tier']}]")
        st.markdown("**Veredicto del Sistema:**")
        st.info(f'"{resumen_final}"')
    else:
        st.info("Presiona el botón para procesar los datos a través del pipeline de Hugging Face.")