
"""
Taller de Bordados - Catálogo y Cotizador
==========================================
App Streamlit con:
- Catálogo estilo "muro visual" (grid inspirado en Pinterest): imagen con
  badge de precio flotante, overlay con degradado para el nombre, badge
  "Personalizable", controles -/+ redondeados y botón flotante de agregar
  con confirmación tipo toast. Filtro de categorías en píldoras horizontales.
  Paginación "Cargar más diseños" en vez de scroll infinito.
- Vista rápida de cada diseño en modal.
- Cotización tipo lista (nombre, precio unitario, precio total).
- Botón "Agregar mi cotización" que abre un checkout en 2 pasos:
    Paso 1: datos del cliente (nombre, apellido, dirección, tipo de cliente)
    Paso 2: método de pago (Pago Móvil / Zelle / USDT Binance) + comprobante
- Generación de PDF de la cotización y mensaje final para WhatsApp.
- Paleta de azules personalizada.

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

# Paleta de colores (según especificación de diseño)
COLOR_FONDO = "#F5F9FF"
COLOR_AZUL_PRIMARIO = "#1A5F7A"
COLOR_AZUL_SECUNDARIO = "#22A39F"
COLOR_AZUL_TERCIARIO = "#AEE2FF"
COLOR_TEXTO = "#1A2B3C"

DISEÑOS_POR_PAGINA = 6

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
        "personalizable": False,
    },
    {
        "id": 2,
        "nombre": "Ramo Floral Vintage",
        "categoria": "Floral",
        "img": "https://placehold.co/400x650/87CEEB/1a1a2e?text=Ramo+Floral",
        "precio": 6.50,
        "personalizable": False,
    },
    {
        "id": 3,
        "nombre": "Iniciales Personalizadas",
        "categoria": "Nombres",
        "img": "https://placehold.co/400x400/87CEEB/1a1a2e?text=Iniciales",
        "precio": 4.00,
        "personalizable": True,
    },
    {
        "id": 4,
        "nombre": "Cactus Boho",
        "categoria": "Plantas",
        "img": "https://placehold.co/400x550/87CEEB/1a1a2e?text=Cactus+Boho",
        "precio": 4.50,
        "personalizable": False,
    },
    {
        "id": 5,
        "nombre": "Frase Motivacional",
        "categoria": "Letras",
        "img": "https://placehold.co/400x350/87CEEB/1a1a2e?text=Frase",
        "precio": 3.50,
        "personalizable": True,
    },
    {
        "id": 6,
        "nombre": "Mandala Circular",
        "categoria": "Geométrico",
        "img": "https://placehold.co/400x600/87CEEB/1a1a2e?text=Mandala",
        "precio": 7.00,
        "personalizable": False,
    },
]
CATALOGO_POR_ID = {d["id"]: d for d in CATALOGO}

# ----------------------------------------------------------------------------
# ESTILOS
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    .stApp {{ background-color: {COLOR_FONDO}; font-family: 'Poppins', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: white; }}
    h1, h2, h3 {{ color: {COLOR_AZUL_PRIMARIO}; font-family: 'Poppins', sans-serif; font-weight: 300; }}

    /* Tarjeta contenedora */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white;
        border-radius: 18px !important;
        border: none !important;
        box-shadow: 0 3px 14px rgba(26, 43, 60, 0.10);
        overflow: hidden;
    }}

    /* Imagen a sangre + badges + overlay */
    .pin-image-wrap {{
        position: relative;
        margin: -1rem -1rem 0.6rem -1rem;
        overflow: hidden;
        border-radius: 18px 18px 0 0;
    }}
    .pin-image {{
        width: 100%;
        display: block;
        transition: transform 0.35s ease;
    }}
    .pin-image-wrap:hover .pin-image {{ transform: scale(1.05); }}
    .pin-badge-precio {{
        position: absolute;
        top: 10px;
        right: 10px;
        background: white;
        color: {COLOR_AZUL_PRIMARIO};
        font-weight: 700;
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    }}
    .pin-badge-personalizable {{
        position: absolute;
        top: 10px;
        left: 10px;
        background: {COLOR_AZUL_SECUNDARIO};
        color: white;
        font-weight: 600;
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 20px;
    }}
    .pin-overlay {{
        position: absolute;
        left: 0; right: 0; bottom: 0;
        padding: 28px 14px 10px 14px;
        background: linear-gradient(to top, rgba(26,43,60,0.85), rgba(26,43,60,0));
    }}
    .pin-nombre {{ color: white; font-weight: 600; font-size: 1rem; }}

    /* Botones generales */
    div.stButton > button {{
        background-color: {COLOR_AZUL_PRIMARIO};
        color: white;
        border-radius: 10px;
        border: none;
    }}
    div.stButton > button:hover {{ background-color: {COLOR_AZUL_SECUNDARIO}; color: white; }}

    /* Iconos -, + redondeados dentro de la tarjeta */
    div[data-testid="column"] div.stButton > button {{
        border-radius: 50% !important;
        width: 34px; height: 34px;
        padding: 0 !important;
        font-weight: 700;
        background-color: {COLOR_AZUL_TERCIARIO};
        color: {COLOR_AZUL_PRIMARIO};
    }}
    div[data-testid="column"] div.stButton > button:hover {{
        background-color: {COLOR_AZUL_PRIMARIO}; color: white;
    }}
    .cantidad-badge {{
        text-align: center;
        padding-top: 6px;
        font-weight: 600;
        color: {COLOR_AZUL_PRIMARIO};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# ESTADO DE SESIÓN
# ----------------------------------------------------------------------------
if "carrito" not in st.session_state:
    st.session_state.carrito = {}
if "cantidades" not in st.session_state:
    st.session_state.cantidades = {d["id"]: 1 for d in CATALOGO}
if "nav_page" not in st.session_state:
    st.session_state.nav_page = None
if "mostrar_checkout" not in st.session_state:
    st.session_state.mostrar_checkout = False
if "checkout_paso" not in st.session_state:
    st.session_state.checkout_paso = 1
if "pedido_enviado" not in st.session_state:
    st.session_state.pedido_enviado = False
if "mostrar_n" not in st.session_state:
    st.session_state.mostrar_n = DISEÑOS_POR_PAGINA
if "mostrar_detalle" not in st.session_state:
    st.session_state.mostrar_detalle = False
if "detalle_id" not in st.session_state:
    st.session_state.detalle_id = None


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
    pdf.set_text_color(26, 95, 122)
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
# MODAL: VISTA RÁPIDA DE UN DISEÑO
# ----------------------------------------------------------------------------
@st.dialog("Vista rápida")
def modal_detalle(diseno):
    st.image(diseno["img"], use_container_width=True)
    st.markdown(f"### {diseno['nombre']}")
    st.markdown(f"**Precio:** ${diseno['precio']:.2f}")
    if diseno.get("personalizable"):
        st.info("✏️ Este diseño es personalizable — contáctanos para tus iniciales o colores.")
    if st.button("Cerrar", use_container_width=True):
        st.session_state.mostrar_detalle = False
        st.rerun()


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
            "container": {"background-color": "white"},
            "nav-link-selected": {"background-color": COLOR_AZUL_PRIMARIO},
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
    st.caption("Explora, ajusta la cantidad y agrega tus diseños favoritos a la cotización.")

    categorias = ["Todas"] + sorted({d["categoria"] for d in CATALOGO})
    filtro = option_menu(
        menu_title=None,
        options=categorias,
        orientation="horizontal",
        default_index=0,
        key="filtro_categoria",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px 6px 0px 0px",
                "padding": "8px 18px",
                "border-radius": "20px",
                "color": COLOR_TEXTO,
                "background-color": COLOR_AZUL_TERCIARIO,
                "font-weight": "500",
                "white-space": "nowrap",
            },
            "nav-link-selected": {
                "background-color": COLOR_AZUL_SECUNDARIO,
                "color": "white",
                "font-weight": "600",
            },
        },
    )
    diseños_filtrados = CATALOGO if filtro == "Todas" else [d for d in CATALOGO if d["categoria"] == filtro]
    diseños_mostrados = diseños_filtrados[: st.session_state.mostrar_n]

    columnas = st.columns(3)
    for idx, diseno in enumerate(diseños_mostrados):
        did = diseno["id"]
        col = columnas[idx % 3]
        with col:
            with st.container(border=True):
                badge_personalizable = (
                    '<div class="pin-badge-personalizable">✏️ Personalizable</div>'
                    if diseno.get("personalizable") else ""
                )
                st.markdown(
                    f"""
                    <div class="pin-image-wrap">
                        <img src="{diseno['img']}" class="pin-image" />
                        <div class="pin-badge-precio">${diseno['precio']:.2f}</div>
                        {badge_personalizable}
                        <div class="pin-overlay"><span class="pin-nombre">{diseno['nombre']}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                cant = st.session_state.cantidades.get(did, 1)
                c_menos, c_cant, c_mas, c_espacio, c_ver, c_agregar = st.columns([1, 1, 1, 1, 1, 1])
                with c_menos:
                    if st.button("−", key=f"menos_{did}"):
                        st.session_state.cantidades[did] = max(1, cant - 1)
                        st.rerun()
                with c_cant:
                    st.markdown(f'<div class="cantidad-badge">{cant}</div>', unsafe_allow_html=True)
                with c_mas:
                    if st.button("+", key=f"mas_{did}"):
                        st.session_state.cantidades[did] = cant + 1
                        st.rerun()
                with c_espacio:
                    st.write("")
                with c_ver:
                    if st.button("🔍", key=f"ver_{did}", help="Vista rápida"):
                        st.session_state.detalle_id = did
                        st.session_state.mostrar_detalle = True
                        st.rerun()
                with c_agregar:
                    if st.button("＋", key=f"agregar_{did}", help="Agregar a mi cotización"):
                        if did in st.session_state.carrito:
                            st.session_state.carrito[did]["cantidad"] += cant
                        else:
                            st.session_state.carrito[did] = {
                                "nombre": diseno["nombre"],
                                "cantidad": cant,
                                "precio_unit": diseno["precio"],
                            }
                        st.toast(f"🧵 {diseno['nombre']} agregado — Total: ${total_carrito():.2f}")
                        st.rerun()

    if st.session_state.mostrar_n < len(diseños_filtrados):
        st.write("")
        _, col_centro, _ = st.columns([2, 1, 2])
        with col_centro:
            if st.button("Cargar más diseños", use_container_width=True):
                st.session_state.mostrar_n += DISEÑOS_POR_PAGINA
                st.rerun()

if st.session_state.mostrar_detalle and st.session_state.detalle_id is not None:
    modal_detalle(CATALOGO_POR_ID[st.session_state.detalle_id])

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
