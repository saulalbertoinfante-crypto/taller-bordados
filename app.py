"""
Taller de Bordados - Catálogo y Cotizador
==========================================
App Streamlit con:
- Catálogo tipo Masonry Grid (diseños digitales/físicos)
- Carrito de cotización persistente vía st.session_state
- Generación de PDF de la cotización
- Generación de mensaje de pedido para WhatsApp (Pago Móvil / Zelle)
- Tema personalizado "azul cielo"

Cómo ejecutar localmente:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
from streamlit_option_menu import option_menu
from fpdf import FPDF
from datetime import datetime
import io
import urllib.parse

# ----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Taller de Bordados",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Datos de contacto de la tienda (edita aquí)
NUMERO_WHATSAPP = "584121234567"  # formato internacional sin '+'
DATOS_PAGO_MOVIL = "0412-1234567 / C.I. 12.345.678 / Banco Ejemplo"
DATOS_ZELLE = "correo@ejemplo.com / Nombre Apellido"

# ----------------------------------------------------------------------------
# CATÁLOGO DE DISEÑOS (edita/expande esta lista con tus productos reales)
# ----------------------------------------------------------------------------
CATALOGO = [
    {
        "id": 1,
        "nombre": "Mariposa Monarca",
        "categoria": "Animales",
        "img": "https://placehold.co/400x500/87CEEB/1a1a2e?text=Mariposa+Monarca",
        "precio_digital": 5.00,
        "precio_fisico": 12.00,
    },
    {
        "id": 2,
        "nombre": "Ramo Floral Vintage",
        "categoria": "Floral",
        "img": "https://placehold.co/400x650/87CEEB/1a1a2e?text=Ramo+Floral",
        "precio_digital": 6.50,
        "precio_fisico": 15.00,
    },
    {
        "id": 3,
        "nombre": "Iniciales Personalizadas",
        "categoria": "Nombres",
        "img": "https://placehold.co/400x400/87CEEB/1a1a2e?text=Iniciales",
        "precio_digital": 4.00,
        "precio_fisico": 10.00,
    },
    {
        "id": 4,
        "nombre": "Cactus Boho",
        "categoria": "Plantas",
        "img": "https://placehold.co/400x550/87CEEB/1a1a2e?text=Cactus+Boho",
        "precio_digital": 4.50,
        "precio_fisico": 11.00,
    },
    {
        "id": 5,
        "nombre": "Frase Motivacional",
        "categoria": "Letras",
        "img": "https://placehold.co/400x350/87CEEB/1a1a2e?text=Frase",
        "precio_digital": 3.50,
        "precio_fisico": 9.00,
    },
    {
        "id": 6,
        "nombre": "Mandala Circular",
        "categoria": "Geométrico",
        "img": "https://placehold.co/400x600/87CEEB/1a1a2e?text=Mandala",
        "precio_digital": 7.00,
        "precio_fisico": 18.00,
    },
]

# ----------------------------------------------------------------------------
# ESTILOS: TEMA "AZUL CIELO" + MASONRY GRID (CSS personalizado)
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F9FF;
    }
    [data-testid="stSidebar"] {
        background-color: #E0F4FF;
    }
    h1, h2, h3 {
        color: #0B5394;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .masonry {
        column-count: 3;
        column-gap: 1rem;
    }
    @media (max-width: 900px) {
        .masonry { column-count: 2; }
    }
    @media (max-width: 600px) {
        .masonry { column-count: 1; }
    }
    .masonry-item {
        display: inline-block;
        width: 100%;
        margin-bottom: 1rem;
        break-inside: avoid;
        background: white;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(11, 83, 148, 0.15);
        border: 1px solid #BEE3F8;
    }
    .masonry-item img {
        width: 100%;
        display: block;
    }
    .masonry-caption {
        padding: 0.6rem 0.8rem 0.2rem 0.8rem;
        font-weight: 600;
        color: #0B5394;
    }
    .masonry-price {
        padding: 0 0.8rem 0.6rem 0.8rem;
        color: #333;
        font-size: 0.9rem;
    }
    div.stButton > button {
        background-color: #4FA8DA;
        color: white;
        border-radius: 10px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #0B5394;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# ESTADO DE SESIÓN: CARRITO
# ----------------------------------------------------------------------------
if "carrito" not in st.session_state:
    # carrito: dict {id_diseño: {"nombre", "tipo", "cantidad", "precio_unit"}}
    st.session_state.carrito = {}


def agregar_al_carrito(diseno, tipo, cantidad):
    clave = f"{diseno['id']}_{tipo}"
    precio_unit = diseno["precio_digital"] if tipo == "Digital" else diseno["precio_fisico"]
    if clave in st.session_state.carrito:
        st.session_state.carrito[clave]["cantidad"] += cantidad
    else:
        st.session_state.carrito[clave] = {
            "nombre": diseno["nombre"],
            "tipo": tipo,
            "cantidad": cantidad,
            "precio_unit": precio_unit,
        }


def eliminar_del_carrito(clave):
    if clave in st.session_state.carrito:
        del st.session_state.carrito[clave]


def total_carrito():
    return sum(item["cantidad"] * item["precio_unit"] for item in st.session_state.carrito.values())


# ----------------------------------------------------------------------------
# GENERACIÓN DE PDF DE COTIZACIÓN
# ----------------------------------------------------------------------------
def generar_pdf_cotizacion():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(11, 83, 148)
    pdf.cell(0, 12, "Taller de Bordados - Cotizacion", ln=True, align="C")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 8, f"Fecha: {fecha}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(90, 8, "Diseno", border=1)
    pdf.cell(30, 8, "Tipo", border=1)
    pdf.cell(20, 8, "Cant.", border=1)
    pdf.cell(25, 8, "Subtotal", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)
    for item in st.session_state.carrito.values():
        subtotal = item["cantidad"] * item["precio_unit"]
        pdf.cell(90, 8, item["nombre"], border=1)
        pdf.cell(30, 8, item["tipo"], border=1)
        pdf.cell(20, 8, str(item["cantidad"]), border=1)
        pdf.cell(25, 8, f"${subtotal:.2f}", border=1, ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, f"TOTAL A PAGAR: ${total_carrito():.2f}", ln=True, align="R")

    # fpdf2 puede devolver bytearray; lo normalizamos a bytes
    return bytes(pdf.output(dest="S"))


# ----------------------------------------------------------------------------
# MENSAJE DE PEDIDO PARA WHATSAPP
# ----------------------------------------------------------------------------
def construir_mensaje_whatsapp(metodo_pago):
    fecha = datetime.now().strftime("%d/%m/%Y")
    lineas = [f"Fecha: {fecha}", "Detalle del Pedido:"]
    for item in st.session_state.carrito.values():
        subtotal = item["cantidad"] * item["precio_unit"]
        lineas.append(f"- {item['cantidad']}x {item['nombre']} ({item['tipo']}) -> ${subtotal:.2f}")
    lineas.append("-" * 30)
    lineas.append(f"TOTAL A PAGAR: ${total_carrito():.2f}")
    lineas.append(f"Metodo de Pago Seleccionado: {metodo_pago}")
    lineas.append("")
    lineas.append("Adjunto mi comprobante para agilizar la entrega.")
    return "\n".join(lineas)


# ----------------------------------------------------------------------------
# NAVEGACIÓN
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧵 Taller de Bordados")
    pagina = option_menu(
        menu_title=None,
        options=["Catálogo", "Mi Cotización", "Contacto"],
        icons=["grid-3x3-gap", "cart3", "whatsapp"],
        default_index=0,
        styles={
            "container": {"background-color": "#E0F4FF"},
            "nav-link-selected": {"background-color": "#4FA8DA"},
        },
    )
    n_items = sum(i["cantidad"] for i in st.session_state.carrito.values())
    st.markdown(f"**Artículos en cotización:** {n_items}")

# ----------------------------------------------------------------------------
# PÁGINA: CATÁLOGO (Masonry Grid)
# ----------------------------------------------------------------------------
if pagina == "Catálogo":
    st.title("Catálogo de Diseños")
    st.caption("Elige un diseño, el formato y la cantidad, y agrégalo a tu cotización.")

    categorias = ["Todas"] + sorted({d["categoria"] for d in CATALOGO})
    filtro = st.selectbox("Filtrar por categoría", categorias)

    diseños_mostrados = CATALOGO if filtro == "Todas" else [d for d in CATALOGO if d["categoria"] == filtro]

    columnas = st.columns(3)
    for idx, diseno in enumerate(diseños_mostrados):
        col = columnas[idx % 3]
        with col:
            st.markdown(
                f"""
                <div class="masonry-item">
                    <img src="{diseno['img']}" />
                    <div class="masonry-caption">{diseno['nombre']}</div>
                    <div class="masonry-price">Digital: ${diseno['precio_digital']:.2f} · Físico: ${diseno['precio_fisico']:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            tipo = st.radio(
                "Formato", ["Digital", "Físico"], key=f"tipo_{diseno['id']}", horizontal=True
            )
            cantidad = st.number_input(
                "Cantidad", min_value=1, max_value=50, value=1, step=1, key=f"cant_{diseno['id']}"
            )
            if st.button("Agregar a mi cotización", key=f"btn_{diseno['id']}"):
                agregar_al_carrito(diseno, "Digital" if tipo == "Digital" else "Físico", cantidad)
                st.success(f"'{diseno['nombre']}' agregado.")

# ----------------------------------------------------------------------------
# PÁGINA: MI COTIZACIÓN (Carrito)
# ----------------------------------------------------------------------------
elif pagina == "Mi Cotización":
    st.title("Mi Cotización")

    if not st.session_state.carrito:
        st.info("Tu cotización está vacía. Ve al Catálogo para agregar diseños.")
    else:
        for clave, item in list(st.session_state.carrito.items()):
            subtotal = item["cantidad"] * item["precio_unit"]
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 2, 1])
            c1.write(item["nombre"])
            c2.write(item["tipo"])
            c3.write(f"x{item['cantidad']}")
            c4.write(f"${subtotal:.2f}")
            if c5.button("🗑️", key=f"del_{clave}"):
                eliminar_del_carrito(clave)
                st.rerun()

        st.divider()
        st.subheader(f"TOTAL A PAGAR: ${total_carrito():.2f}")

        metodo_pago = st.radio("Método de Pago", ["Pago Móvil", "Zelle"], horizontal=True)
        if metodo_pago == "Pago Móvil":
            st.info(f"Datos Pago Móvil: {DATOS_PAGO_MOVIL}")
        else:
            st.info(f"Datos Zelle: {DATOS_ZELLE}")

        st.file_uploader("Adjunta tu comprobante de pago (opcional, solo referencia)", type=["png", "jpg", "jpeg", "pdf"])

        col_a, col_b = st.columns(2)
        with col_a:
            pdf_bytes = generar_pdf_cotizacion()
            st.download_button(
                "📄 Descargar cotización en PDF",
                data=pdf_bytes,
                file_name=f"cotizacion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
            )
        with col_b:
            mensaje = construir_mensaje_whatsapp(metodo_pago)
            enlace_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(mensaje)}"
            st.link_button("📲 Enviar pedido por WhatsApp", enlace_wa)

        with st.expander("Vista previa del mensaje de WhatsApp"):
            st.code(mensaje, language=None)

        if st.button("Vaciar cotización"):
            st.session_state.carrito = {}
            st.rerun()

# ----------------------------------------------------------------------------
# PÁGINA: CONTACTO
# ----------------------------------------------------------------------------
else:
    st.title("Contacto")
    st.write("¿Tienes dudas sobre un diseño o quieres un bordado personalizado?")
    st.markdown(f"📲 Escríbenos por WhatsApp: **+{NUMERO_WHATSAPP}**")
    st.markdown("📸 Síguenos en Instagram para ver nuestros trabajos más recientes.")
