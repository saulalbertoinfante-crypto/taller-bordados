"""
Taller de Bordados - Catálogo y Cotizador
==========================================
App Streamlit con:
- Catálogo con tarjetas: precio único, controles -/+ que recalculan el precio
  en vivo y flecha "›" para agregar a la cotización.
- Cotización tipo lista (nombre, precio unitario, precio total).
- Botón "Agregar mi cotización" que abre un checkout en 2 pasos:
    Paso 1: datos del cliente (nombre, apellido, dirección, tipo de cliente)
    Paso 2: método de pago (Pago Móvil / Zelle / USDT Binance) + comprobante
- Generación de PDF de la cotización y mensaje final para WhatsApp.
- Tema personalizado "azul cielo".

Cómo ejecutar localmente:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
from streamlit_option_menu import option_menu
from fpdf import FPDF
from datetime import datetime
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

# Datos de contacto / pago de la tienda (edita aquí)
NUMERO_WHATSAPP = "584121234567"  # formato internacional sin '+'
DATOS_PAGO_MOVIL = "0412-1234567 / C.I. 12.345.678 / Banco Ejemplo"
DATOS_ZELLE = "correo@ejemplo.com / Nombre Apellido"
DATOS_USDT_BINANCE = "ID Binance Pay: 123456789 (o dirección USDT-TRC20: T...)"

# ----------------------------------------------------------------------------
# CATÁLOGO DE DISEÑOS (edita/expande esta lista con tus productos reales)
# ----------------------------------------------------------------------------
CATALOGO = [
    {
        "id": 1,
        "nombre": "Mariposa Monarca",
        "categoria": "Animales",
        "img": "https://placehold.co/400x500/87CEEB/1a1a2e?text=Mariposa+Monarca",
        "precio": 5.00,
    },
    {
        "id": 2,
        "nombre": "Ramo Floral Vintage",
        "categoria": "Floral",
        "img": "https://placehold.co/400x650/87CEEB/1a1a2e?text=Ramo+Floral",
        "precio": 6.50,
    },
    {
        "id": 3,
        "nombre": "Iniciales Personalizadas",
        "categoria": "Nombres",
        "img": "https://placehold.co/400x400/87CEEB/1a1a2e?text=Iniciales",
        "precio": 4.00,
    },
    {
        "id": 4,
        "nombre": "Cactus Boho",
        "categoria": "Plantas",
        "img": "https://placehold.co/400x550/87CEEB/1a1a2e?text=Cactus+Boho",
        "precio": 4.50,
    },
    {
        "id": 5,
        "nombre": "Frase Motivacional",
        "categoria": "Letras",
        "img": "https://placehold.co/400x350/87CEEB/1a1a2e?text=Frase",
        "precio": 3.50,
    },
    {
        "id": 6,
        "nombre": "Mandala Circular",
        "categoria": "Geométrico",
        "img": "https://placehold.co/400x600/87CEEB/1a1a2e?text=Mandala",
        "precio": 7.00,
    },
]
CATALOGO_POR_ID = {d["id"]: d for d in CATALOGO}

# ----------------------------------------------------------------------------
# ESTILOS: TEMA "AZUL CIELO"
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #F0F9FF; }
    [data-testid="stSidebar"] { background-color: #E0F4FF; }
    h1, h2, h3 { color: #0B5394; font-family: 'Trebuchet MS', sans-serif; }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-radius: 14px !important;
        border: 1px solid #BEE3F8 !important;
        box-shadow: 0 2px 8px rgba(11, 83, 148, 0.12);
    }
    .tarjeta-precio {
        font-weight: 700;
        color: #0B5394;
        font-size: 1.05rem;
        padding: 0.3rem 0 0.2rem 0;
    }
    div.stButton > button {
        background-color: #4FA8DA;
        color: white;
        border-radius: 10px;
        border: none;
    }
    div.stButton > button:hover { background-color: #0B5394; color: white; }

    /* Botones pequeños -, + y › dentro de la tarjeta */
    div[data-testid="column"] div.stButton > button {
        padding: 0.1rem 0.6rem;
        font-weight: 700;
    }
    .chevron-btn button {
        background-color: transparent !important;
        color: #7FB3D5 !important;
        font-size: 1.3rem !important;
        border: none !important;
        box-shadow: none !important;
    }
    .chevron-btn button:hover { color: #0B5394 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# ESTADO DE SESIÓN
# ----------------------------------------------------------------------------
if "carrito" not in st.session_state:
    # carrito confirmado: {id_diseño: {"nombre", "cantidad", "precio_unit"}}
    st.session_state.carrito = {}
if "cantidades" not in st.session_state:
    # cantidad seleccionada actualmente en cada tarjeta (antes de agregar)
    st.session_state.cantidades = {d["id"]: 1 for d in CATALOGO}
if "nav_page" not in st.session_state:
    st.session_state.nav_page = None
if "mostrar_checkout" not in st.session_state:
    st.session_state.mostrar_checkout = False
if "checkout_paso" not in st.session_state:
    st.session_state.checkout_paso = 1
if "pedido_enviado" not in st.session_state:
    st.session_state.pedido_enviado = False


def total_carrito():
    return sum(i["cantidad"] * i["precio_unit"] for i in st.session_state.carrito.values())


def eliminar_del_carrito(id_diseno):
    if id_diseno in st.session_state.carrito:
        del st.session_state.carrito[id_diseno]


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
    pdf.cell(100, 8, "Diseno", border=1)
    pdf.cell(30, 8, "P. Unit.", border=1)
    pdf.cell(20, 8, "Cant.", border=1)
    pdf.cell(30, 8, "Subtotal", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)
    for item in st.session_state.carrito.values():
        subtotal = item["cantidad"] * item["precio_unit"]
        pdf.cell(100, 8, item["nombre"], border=1)
        pdf.cell(30, 8, f"${item['precio_unit']:.2f}", border=1)
        pdf.cell(20, 8, str(item["cantidad"]), border=1)
        pdf.cell(30, 8, f"${subtotal:.2f}", border=1, ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, f"TOTAL A PAGAR: ${total_carrito():.2f}", ln=True, align="R")

    return bytes(pdf.output(dest="S"))


# ----------------------------------------------------------------------------
# MENSAJE DE PEDIDO PARA WHATSAPP
# ----------------------------------------------------------------------------
def construir_mensaje_whatsapp(cliente, metodo_pago):
    fecha = datetime.now().strftime("%d/%m/%Y")
    lineas = [
        f"Fecha: {fecha}",
        f"Cliente: {cliente['nombre']} {cliente['apellido']} ({cliente['tipo_cliente']})",
        f"Dirección: {cliente['direccion']}",
        "Detalle del Pedido:",
    ]
    for item in st.session_state.carrito.values():
        subtotal = item["cantidad"] * item["precio_unit"]
        lineas.append(f"- {item['cantidad']}x {item['nombre']} -> ${subtotal:.2f}")
    lineas.append("-" * 30)
    lineas.append(f"TOTAL A PAGAR: ${total_carrito():.2f}")
    lineas.append(f"Método de Pago Seleccionado: {metodo_pago}")
    lineas.append("")
    lineas.append("Adjunto mi comprobante para agilizar la entrega.")
    return "\n".join(lineas)


# ----------------------------------------------------------------------------
# MODAL DE CHECKOUT (2 PASOS)
# ----------------------------------------------------------------------------
@st.dialog("Finalizar cotización")
def modal_checkout():
    if st.session_state.checkout_paso == 1:
        st.subheader("Paso 1 de 2 · Datos del cliente")
        nombre = st.text_input("Nombre", value=st.session_state.get("c_nombre", ""))
        apellido = st.text_input("Apellido", value=st.session_state.get("c_apellido", ""))
        direccion = st.text_input("Dirección", value=st.session_state.get("c_direccion", ""))
        tipo_cliente = st.radio(
            "Tipo de cliente", ["Natural", "Empresa"],
            horizontal=True,
            index=0 if st.session_state.get("c_tipo", "Natural") == "Natural" else 1,
        )

        col1, col2 = st.columns(2)
        if col1.button("Cancelar", use_container_width=True):
            st.session_state.mostrar_checkout = False
            st.rerun()
        if col2.button("Siguiente →", use_container_width=True):
            if nombre.strip() and apellido.strip() and direccion.strip():
                st.session_state.c_nombre = nombre.strip()
                st.session_state.c_apellido = apellido.strip()
                st.session_state.c_direccion = direccion.strip()
                st.session_state.c_tipo = tipo_cliente
                st.session_state.checkout_paso = 2
                st.rerun()
            else:
                st.warning("Completa nombre, apellido y dirección para continuar.")

    else:
        st.subheader("Paso 2 de 2 · Método de pago")
        metodo = st.radio(
            "Selecciona tu método de pago",
            ["Pago Móvil", "Zelle", "USDT Binance"],
            index=["Pago Móvil", "Zelle", "USDT Binance"].index(
                st.session_state.get("c_metodo", "Pago Móvil")
            ),
        )
        if metodo == "Pago Móvil":
            st.info(f"Datos Pago Móvil: {DATOS_PAGO_MOVIL}")
        elif metodo == "Zelle":
            st.info(f"Datos Zelle: {DATOS_ZELLE}")
        else:
            st.info(f"Datos USDT Binance: {DATOS_USDT_BINANCE}")

        comprobante = st.file_uploader(
            "Sube la captura de tu comprobante de pago",
            type=["png", "jpg", "jpeg", "pdf"],
        )

        col1, col2 = st.columns(2)
        if col1.button("← Atrás", use_container_width=True):
            st.session_state.checkout_paso = 1
            st.rerun()
        if col2.button("Enviar pedido", use_container_width=True):
            if comprobante is None:
                st.warning("Adjunta la captura del comprobante antes de enviar.")
            else:
                st.session_state.c_metodo = metodo
                st.session_state.pedido_enviado = True
                st.session_state.mostrar_checkout = False
                st.session_state.checkout_paso = 1
                st.rerun()


# ----------------------------------------------------------------------------
# NAVEGACIÓN
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧵 Taller de Bordados")

    opciones = ["Catálogo", "Mi Cotización", "Contacto"]
    manual_idx = opciones.index(st.session_state.nav_page) if st.session_state.nav_page else None

    pagina = option_menu(
        menu_title=None,
        options=opciones,
        icons=["grid-3x3-gap", "cart3", "whatsapp"],
        default_index=0,
        manual_select=manual_idx,
        key="menu_principal",
        styles={
            "container": {"background-color": "#E0F4FF"},
            "nav-link-selected": {"background-color": "#4FA8DA"},
        },
    )
    st.session_state.nav_page = None  # se resetea tras aplicarse

    n_items = sum(i["cantidad"] for i in st.session_state.carrito.values())
    st.markdown(f"**Artículos en cotización:** {n_items}")

# ----------------------------------------------------------------------------
# PÁGINA: CATÁLOGO
# ----------------------------------------------------------------------------
if pagina == "Catálogo":
    st.title("Catálogo de Diseños")
    st.caption("Ajusta la cantidad con − / + y toca › para agregarlo a tu cotización.")

    categorias = ["Todas"] + sorted({d["categoria"] for d in CATALOGO})
    filtro = st.selectbox("Filtrar por categoría", categorias)
    diseños_mostrados = CATALOGO if filtro == "Todas" else [d for d in CATALOGO if d["categoria"] == filtro]

    columnas = st.columns(3)
    for idx, diseno in enumerate(diseños_mostrados):
        did = diseno["id"]
        col = columnas[idx % 3]
        with col:
            with st.container(border=True):
                st.image(diseno["img"], use_container_width=True)

                cant = st.session_state.cantidades.get(did, 1)
                precio_mostrado = diseno["precio"] * cant
                st.markdown(
                    f'<div class="tarjeta-precio">{diseno["nombre"]}: {precio_mostrado:.2f}$</div>',
                    unsafe_allow_html=True,
                )

                c_menos, c_cant, c_mas, c_espacio, c_flecha = st.columns([1, 1, 1, 3, 1])
                with c_menos:
                    if st.button("−", key=f"menos_{did}"):
                        st.session_state.cantidades[did] = max(1, cant - 1)
                        st.rerun()
                with c_cant:
                    st.markdown(
                        f'<div style="text-align:center;padding-top:6px;">{cant}</div>',
                        unsafe_allow_html=True,
                    )
                with c_mas:
                    if st.button("+", key=f"mas_{did}"):
                        st.session_state.cantidades[did] = cant + 1
                        st.rerun()
                with c_espacio:
                    st.write("")
                with c_flecha:
                    st.markdown('<div class="chevron-btn">', unsafe_allow_html=True)
                    if st.button("›", key=f"chevron_{did}"):
                        st.session_state.carrito[did] = {
                            "nombre": diseno["nombre"],
                            "cantidad": cant,
                            "precio_unit": diseno["precio"],
                        }
                        st.session_state.nav_page = "Mi Cotización"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PÁGINA: MI COTIZACIÓN
# ----------------------------------------------------------------------------
elif pagina == "Mi Cotización":
    st.title("Mi Cotización")

    if st.session_state.pedido_enviado:
        st.success("¡Pedido enviado! Revisa el mensaje de WhatsApp abajo para completarlo.")
        mensaje = construir_mensaje_whatsapp(
            {
                "nombre": st.session_state.get("c_nombre", ""),
                "apellido": st.session_state.get("c_apellido", ""),
                "direccion": st.session_state.get("c_direccion", ""),
                "tipo_cliente": st.session_state.get("c_tipo", ""),
            },
            st.session_state.get("c_metodo", ""),
        )
        enlace_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(mensaje)}"
        st.link_button("📲 Abrir WhatsApp y adjuntar mi comprobante", enlace_wa)
        with st.expander("Vista previa del mensaje"):
            st.code(mensaje, language=None)
        if st.button("Hacer un nuevo pedido"):
            st.session_state.carrito = {}
            st.session_state.pedido_enviado = False
            st.rerun()

    elif not st.session_state.carrito:
        st.info("Tu cotización está vacía. Ve al Catálogo para agregar diseños.")

    else:
        for did, item in list(st.session_state.carrito.items()):
            subtotal = item["cantidad"] * item["precio_unit"]
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 2, 1])
            c1.write(item["nombre"])
            c2.write(f"P. unit.: ${item['precio_unit']:.2f}")
            c3.write(f"x{item['cantidad']}")
            c4.write(f"${subtotal:.2f}")
            if c5.button("🗑️", key=f"del_{did}"):
                eliminar_del_carrito(did)
                st.rerun()

        st.divider()
        st.subheader(f"TOTAL A PAGAR: ${total_carrito():.2f}")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            pdf_bytes = generar_pdf_cotizacion()
            st.download_button(
                "📄 Descargar PDF",
                data=pdf_bytes,
                file_name=f"cotizacion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
            )
        with col_b:
            if st.button("🧾 Agregar mi cotización", use_container_width=True):
                st.session_state.mostrar_checkout = True
                st.session_state.checkout_paso = 1
                st.rerun()
        with col_c:
            if st.button("Vaciar cotización", use_container_width=True):
                st.session_state.carrito = {}
                st.rerun()

if st.session_state.mostrar_checkout:
    modal_checkout()

# ----------------------------------------------------------------------------
# PÁGINA: CONTACTO
# ----------------------------------------------------------------------------
if pagina == "Contacto":
    st.title("Contacto")
    st.write("¿Tienes dudas sobre un diseño o quieres un bordado personalizado?")
    st.markdown(f"📲 Escríbenos por WhatsApp: **+{NUMERO_WHATSAPP}**")
    st.markdown("📸 Síguenos en Instagram para ver nuestros trabajos más recientes.")
