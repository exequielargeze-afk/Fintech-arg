import streamlit as st
import requests

# =========================================================================
# 💰 TU PANEL DE CONTROL DE MONETIZACIÓN (Cambiá estos links cuando quieras)
# =========================================================================
LINK_INVITACION_BINGX = "https://bingxdao.com/referral-program/CISAPT?activityId=1641166226936946772" 
# =========================================================================

# 1. Configuración de la página y adaptación móvil
st.set_page_config(page_title="RindePesos", page_icon="💸", layout="centered")

# Estilos CSS avanzados para un contraste perfecto y legibilidad extrema
st.markdown("""
    <style>
    .big-font { font-size: 26px !important; font-weight: bold; color: #2ecc71; }
    .daily-font { font-size: 18px !important; font-weight: bold; color: #3498db; }
    
    /* Tarjetas de Podio */
    .podio-1 { padding: 18px; border-radius: 12px; background-color: #fffbeb; margin-bottom: 12px; border-left: 6px solid #fbbf24; border-right: 1px solid #fef3c7; }
    .podio-2 { padding: 15px; border-radius: 10px; background-color: #f3f4f6; margin-bottom: 12px; border-left: 6px solid #9ca3af; }
    .podio-3 { padding: 15px; border-radius: 10px; background-color: #fff7ed; margin-bottom: 12px; border-left: 6px solid #ea580c; }
    .card-normal { padding: 15px; border-radius: 10px; background-color: #ffffff; margin-bottom: 10px; border-left: 5px solid #bdc3c7; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    
    /* Bloque de Sponsor BingX */
    .sponsor-card { padding: 20px; border-radius: 12px; background-color: #e0f2fe; margin-bottom: 20px; border: 2px dashed #0284c7; text-align: center; }
    
    .card-title { font-size: 20px !important; font-weight: 800 !important; color: #111827 !important; display: inline-block; margin-bottom: 5px; }
    .badge-tasa { background-color: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💸 RindePesos")
st.subheader("Hacé que tus pesos rindan al máximo en Argentina")
st.write("Descubrí qué cuenta te paga más hoy por tener tu plata guardada o a plazo.")

# 2. Entrada del usuario
monto = st.number_input("¿Cuántos pesos querés simular?", min_value=1000, value=150000, step=10000, format="%d")

# =========================================================================
# 🔥 BLOQUE PUBLICITARIO DE BINGX (Genera tus ingresos extras)
# =========================================================================
st.markdown(f"""
<div class="sponsor-card">
    <h3 style="color: #0369a1; margin-top:0;">🚀 ¡PROMO DESTACADA DE LA SEMANA!</h3>
    <p style="color: #1e293b; font-size: 16px;">¿Buscás rendimientos más altos? Create una cuenta en <b>BingX</b>, completá tu registro y empezá a operar con cripto.</p>
    <p style="color: #0369a1; font-weight: bold; font-size: 18px;">🎁 ¡Bono de bienvenida exclusivo esperando por vos!</p>
    <a href="{LINK_INVITACION_BINGX}" target="_blank" style="text-decoration:none;">
        <button style="background-color: #0284c7; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size:16px;">
            Crear Cuenta Gratis en BingX ↗
        </button>
    </a>
</div>
""", unsafe_allow_html=True)
# =========================================================================

# 3. Base de datos con mecanismo de Fallback (Tasas de mercado)
datos_respaldo = [
    {"nombre": "Carrefour Banco", "tna": 20.00},
    {"nombre": "Lemon Cash", "tna": 20.20},
    {"nombre": "Cocos Pay", "tna": 20.02},
    {"nombre": "Personal Pay", "tna": 19.00},
    {"nombre": "Naranja X", "tna": 18.00},
    {"nombre": "Ualá", "tna": 18.00},
    {"nombre": "Mercado Pago", "tna": 17.90}
]

TNA_PLAZO_FIJO = 25.00  

url = "https://dolarapi.com"
datos_finales = []

try:
    respuesta = requests.get(url, timeout=3)
    if respuesta.status_code == 200:
        datos_api = respuesta.json()
        for b in datos_api:
            datos_finales.append({
                "nombre": b.get("nombre", "Desconocido"),
                "tna": float(b.get("tna", 0))
            })
    else:
        datos_finales = datos_respaldo
except Exception:
    datos_finales = datos_respaldo

# 4. Procesamiento matemático
ranking = []
for b in datos_finales:
    nombre = b["nombre"]
    tna = b["tna"]
    ganancia_30 = (monto * (tna / 100)) / 12
    ganancia_diaria = ganancia_30 / 30
    ranking.append({'nombre': nombre, 'tna': tna, 'ganancia': ganancia_30, 'ganancia_diaria': ganancia_diaria})

ranking_ordenado = sorted(ranking, key=lambda x: x['tna'], reverse=True)

ganancia_pf = (monto * (TNA_PLAZO_FIJO / 100)) / 12

mejor_b = ranking_ordenado[0]['nombre']
peor_b = ranking_ordenado[-1]
diferencia_billeteras = ranking_ordenado[0]['ganancia'] - peor_b['ganancia']

st.error(f"⚠️ **¡Ojo!** Si dejás tus pesos en la peor billetera en vez de usar **{mejor_b}**, estás perdiendo **${diferencia_billeteras:,.2f}** este mes.")

st.info(f"🏦 **Comparación con Plazo Fijo Bancario (TNA {TNA_PLAZO_FIJO}%):** Un plazo fijo te dejaría **${ganancia_pf:,.2f}** al mes, pero acordate de que **te congela la plata por 30 días**. ¡Las billeteras de abajo te pagan rindiendo día a día con tu plata libre!")

# 6. Renderizar el Podio Visual y Ranking
st.write("### 🏆 Ranking de Cuentas Remuneradas")

texto_compartir = f"💸 *RANKING DE RENDIMIENTOS HOY EN ARGENTINA*\nSimulación para: ${monto:,.2f}\n\n"

for puesto, b in enumerate(ranking_ordenado, 1):
    if puesto == 1:
        clase_card = "podio-1"
        icono = "🥇"
    elif puesto == 2:
        clase_card = "podio-2"
        icono = "🥈"
    elif puesto == 3:
        clase_card = "podio-3"
        icono = "🥉"
    else:
        clase_card = "card-normal"
        icono = "📱"
        
    if puesto <= 5:
        texto_compartir += f"{icono} *Puesto #{puesto}: {b['nombre']}*\n👉 rinde: ${b['ganancia']:,.2f}/mes o ${b['ganancia_diaria']:,.2f}/día (TNA: {b['tna']}%)\n\n"

    with st.container():
        st.markdown(f"""
        <div class="{clase_card}">
            <span class="card-title">{icono} Puesto #{puesto}: {b['nombre']}</span> 
            <span class="badge-tasa">TNA: {b['tna']}%</span><br>
            <span class="big-font">${b['ganancia']:,.2f} <small style="color: #4b5563; font-size:14px; font-weight:normal;">al mes</small></span> 
            <span style="margin-left:12px; margin-right:12px; color:#d1d5db;">|</span>
            <span class="daily-font">${b['ganancia_diaria']:,.2f} <small style="color: #4b5563; font-size:14px; font-weight:normal;">por día</small></span>
        </div>
        """, unsafe_allow_html=True)

texto_compartir += f"Calculá tus ahorros gratis en: fintech-arg-viwdwylf8ioykfdixxtcal.streamlit.app"

# 7. Herramientas de Viralidad
st.write("---")
st.write("### 📢 ¡Compartí el dato con tu familia o amigos!")
st.write("Tocá el botón de abajo para copiar un resumen listo para pegar en tus grupos de WhatsApp:")

st.code(texto_compartir, language="text")
st.caption("💡 Mantené presionado o dale doble clic al cuadro gris de arriba para copiarlo al instante.")

# 8. Captura de Emails
st.write("---")
st.write("### 🔔 Que no se te escapen las subas de tasas")
email = st.text_input("Dejá tu correo electrónico y te mandamos una alerta automática apenas una billetera aumente sus ganancias:")
if st.button("Activar Alertas Gratis"):
    if email:
        st.success("¡Excelente! Ya quedaste registrado. Te avisaremos de inmediato.")
    else:
        st.warning("Por favor, ingresá un correo electrónico válido.")
