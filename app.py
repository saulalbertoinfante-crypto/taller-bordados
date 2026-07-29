import streamlit as st
import json

# =============================================
# DATOS DE PRODUCTOS
# =============================================
PRODUCTOS = [
    {"id": 1, "nombre": "Mariposa Monarca", "categoria": "animales", "precio": 5.00, "imagen": "https://picsum.photos/seed/mariposa/300/450", "personalizable": False},
    {"id": 2, "nombre": "Ramo Floral", "categoria": "floral", "precio": 6.50, "imagen": "https://picsum.photos/seed/ramo/300/320", "personalizable": False},
    {"id": 3, "nombre": "Iniciales", "categoria": "letras", "precio": 4.00, "imagen": "https://picsum.photos/seed/inicial/300/500", "personalizable": True},
    {"id": 4, "nombre": "Águila Real", "categoria": "animales", "precio": 8.00, "imagen": "https://picsum.photos/seed/aguila/300/380", "personalizable": False},
    {"id": 5, "nombre": "Mandala", "categoria": "geometrico", "precio": 7.00, "imagen": "https://picsum.photos/seed/mandala/300/350", "personalizable": False},
    {"id": 6, "nombre": "Nombre Propio", "categoria": "nombres", "precio": 4.00, "imagen": "https://picsum.photos/seed/nombre/300/480", "personalizable": True},
    {"id": 7, "nombre": "Mariposa 2", "categoria": "animales", "precio": 5.50, "imagen": "https://picsum.photos/seed/mariposa2/300/400", "personalizable": False},
    {"id": 8, "nombre": "Ramo 2", "categoria": "floral", "precio": 7.00, "imagen": "https://picsum.photos/seed/ramo2/300/350", "personalizable": False},
    {"id": 9, "nombre": "Letra A", "categoria": "letras", "precio": 3.50, "imagen": "https://picsum.photos/seed/letraA/300/420", "personalizable": True},
    {"id": 10, "nombre": "Águila 2", "categoria": "animales", "precio": 9.00, "imagen": "https://picsum.photos/seed/aguila2/300/390", "personalizable": False},
    {"id": 11, "nombre": "Mandala 2", "categoria": "geometrico", "precio": 7.50, "imagen": "https://picsum.photos/seed/mandala2/300/360", "personalizable": False},
    {"id": 12, "nombre": "Nombre 2", "categoria": "nombres", "precio": 4.50, "imagen": "https://picsum.photos/seed/nombre2/300/470", "personalizable": True},
    {"id": 13, "nombre": "Mariposa 3", "categoria": "animales", "precio": 6.00, "imagen": "https://picsum.photos/seed/mariposa3/300/430", "personalizable": False},
    {"id": 14, "nombre": "Ramo 3", "categoria": "floral", "precio": 8.00, "imagen": "https://picsum.photos/seed/ramo3/300/310", "personalizable": False},
]

# =============================================
# INICIALIZAR ESTADO DE SESIÓN
# =============================================
if "mostrar_hasta" not in st.session_state:
    st.session_state.mostrar_hasta = 9
if "cantidades" not in st.session_state:
    st.session_state.cantidades = {p["id"]: 0 for p in PRODUCTOS}
if "filtro_actual" not in st.session_state:
    st.session_state.filtro_actual = "all"

# =============================================
# FUNCIÓN PARA GENERAR EL HTML
# =============================================
def generar_html():
    # Datos serializados a JSON para inyectar en JavaScript
    productos_json = json.dumps(PRODUCTOS)
    cantidades_json = json.dumps(st.session_state.cantidades)
    filtro = st.session_state.filtro_actual
    mostrar_hasta = st.session_state.mostrar_hasta

    # Determinar si hay más productos para cargar
    productos_filtrados = PRODUCTOS if filtro == "all" else [p for p in PRODUCTOS if p["categoria"] == filtro]
    hay_mas = len(productos_filtrados) > mostrar_hasta

    # Construir el HTML con todas las llaves de JS escapadas con {{ y }}
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Bordados</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; font-family: 'Inter', -apple-system, sans-serif; }}
        body {{
            background: #F8FAFC;
            padding: 20px 20px 0 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2rem;
            color: #1A5F7A;
            font-weight: 600;
        }}
        .header p {{
            color: #64748B;
            font-size: 1.1rem;
        }}
        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 15px;
        }}
        .filter-btn {{
            padding: 8px 20px;
            border-radius: 30px;
            border: 1.5px solid #CBD5E1;
            background: transparent;
            color: #64748B;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-btn:hover {{
            border-color: #1A5F7A;
            color: #1A5F7A;
        }}
        .filter-btn.active {{
            background: #1A5F7A;
            border-color: #1A5F7A;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(26,95,122,0.3);
        }}
        .masonry {{
            column-count: 3;
            column-gap: 20px;
            margin-bottom: 20px;
        }}
        .pin {{
            break-inside: avoid;
            margin-bottom: 20px;
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
        }}
        .pin:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -10px rgba(0,0,0,0.15);
        }}
        .pin img {{
            width: 100%;
            display: block;
            transition: transform 0.4s ease;
        }}
        .pin:hover img {{
            transform: scale(1.03);
        }}
        .pin-image-wrapper {{
            position: relative;
            overflow: hidden;
        }}
        .badge-personalizable {{
            position: absolute;
            top: 12px;
            left: 12px;
            background: #22A39F;
            color: white;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            z-index: 5;
            box-shadow: 0 2px 8px rgba(34,163,159,0.4);
        }}
        .pin-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 30px 15px 15px 15px;
            background: linear-gradient(transparent, rgba(0,0,0,0.7));
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            pointer-events: none;
        }}
        .pin-nombre {{
            color: white;
            font-weight: 600;
            font-size: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .pin-precio {{
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            background: rgba(0,0,0,0.3);
            padding: 2px 12px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
        }}
        .pin-footer {{
            padding: 12px 15px 15px 15px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid #F1F5F9;
        }}
        .subtotal-display {{
            font-weight: 600;
            color: #1A5F7A;
            font-size: 0.95rem;
            background: #EFF6FF;
            padding: 2px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-right: 10px;
        }}
        .quantity-control {{
            display: flex;
            align-items: center;
            gap: 6px;
            background: #F8FAFC;
            padding: 2px 4px;
            border-radius: 30px;
            border: 1px solid #E2E8F0;
        }}
        .quantity-control button {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            font-size: 1.2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: 0.15s;
            background: transparent;
            color: #1A5F7A;
        }}
        .quantity-control button.qty-plus {{
            background: #1A5F7A;
            color: white;
            box-shadow: 0 2px 8px rgba(26,95,122,0.3);
        }}
        .quantity-control button.qty-plus:hover {{
            background: #0f4a5e;
        }}
        .quantity-control button.qty-minus {{
            border: 1px solid #CBD5E1;
        }}
        .quantity-control button.qty-minus:hover {{
            background: #F1F5F9;
        }}
        .qty-number {{
            font-weight: 700;
            color: #1A5F7A;
            min-width: 24px;
            text-align: center;
            font-size: 1rem;
        }}
        .btn-pedir {{
            background: #1A5F7A;
            color: white;
            border: none;
            padding: 6px 18px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 4px 12px rgba(26,95,122,0.3);
        }}
        .btn-pedir:hover {{
            background: #0f4a5e;
            transform: scale(1.02);
        }}
        .btn-cargar-mas {{
            background: #1A5F7A;
            color: white;
            border: none;
            padding: 12px 40px;
            border-radius: 30px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 4px 15px rgba(26,95,122,0.3);
            display: block;
            margin: 0 auto 40px auto;
        }}
        .btn-cargar-mas:hover {{
            background: #0f4a5e;
            transform: scale(1.02);
        }}
        .footer-message {{
            text-align: center;
            color: #94A3B8;
            padding: 20px 0 40px 0;
        }}
        @media (max-width: 768px) {{
            .masonry {{ column-count: 2; column-gap: 12px; }}
            .header h1 {{ font-size: 1.6rem; }}
        }}
        @media (max-width: 480px) {{
            .masonry {{ column-count: 2; column-gap: 8px; }}
            .filter-btn {{ padding: 6px 14px; font-size: 0.8rem; }}
            .pin-footer {{ flex-wrap: wrap; gap: 8px; }}
            .subtotal-display {{ font-size: 0.85rem; margin-right: 0; width: 100%; text-align: center; }}
            .quantity-control {{ flex: 1; justify-content: center; }}
            .btn-pedir {{ flex: 1; text-align: center; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Catálogo de Diseños</h1>
        <p>Explora, ajusta cantidades y haz tu pedido directamente desde cada diseño.</p>
    </div>

    <div class="filters" id="filters">
        <button class="filter-btn active" data-category="all">Todas</button>
        <button class="filter-btn" data-category="animales">Animales</button>
        <button class="filter-btn" data-category="floral">Floral</button>
        <button class="filter-btn" data-category="geometrico">Geométrico</button>
        <button class="filter-btn" data-category="letras">Letras</button>
        <button class="filter-btn" data-category="nombres">Nombres</button>
    </div>

    <div class="masonry" id="masonry"></div>
    <div id="cargar-mas-container"></div>

    <script>
        // Datos desde Python
        const productos = {productos_json};
        const cantidadesIniciales = {cantidades_json};
        let cantidades = {{...cantidadesIniciales}};
        let mostrarHasta = {mostrar_hasta};
        let filtroActual = "{filtro}";
        const hayMas = {str(hay_mas).lower()};

        function enviarMensaje(valor) {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: valor
            }}, '*');
        }}

        function renderizar() {{
            const filtrados = filtroActual === 'all' 
                ? productos 
                : productos.filter(p => p.categoria === filtroActual);
            const visibles = filtrados.slice(0, mostrarHasta);
            const container = document.getElementById('masonry');
            container.innerHTML = '';

            visibles.forEach(prod => {{
                const cant = cantidades[prod.id] || 0;
                const subtotal = prod.precio * cant;
                const badge = prod.personalizable ? `<span class="badge-personalizable">Personalizable</span>` : '';
                const subtotalHtml = cant > 0 ? `<span class="subtotal-display">Subtotal: ${{subtotal.toFixed(2)}}</span>` : '';

                const pin = document.createElement('div');
                pin.className = 'pin';
                pin.innerHTML = `
                    <div class="pin-image-wrapper">
                        <img src="${{prod.imagen}}" alt="${{prod.nombre}}" loading="lazy">
                        ${{badge}}
                        <div class="pin-overlay">
                            <span class="pin-nombre">${{prod.nombre}}</span>
                            <span class="pin-precio">$${{prod.precio.toFixed(2)}}</span>
                        </div>
                    </div>
                    <div class="pin-footer">
                        <div>${{subtotalHtml}}</div>
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="quantity-control" data-id="${{prod.id}}">
                                <button class="qty-minus" data-id="${{prod.id}}">−</button>
                                <span class="qty-number" id="qty-${{prod.id}}">${{cant}}</span>
                                <button class="qty-plus" data-id="${{prod.id}}">+</button>
                            </div>
                            <button class="btn-pedir" data-id="${{prod.id}}">Pedir</button>
                        </div>
                    </div>
                `;
                container.appendChild(pin);
            }});

            const cargarContainer = document.getElementById('cargar-mas-container');
            cargarContainer.innerHTML = '';
            if (filtrados.length > mostrarHasta) {{
                const btn = document.createElement('button');
                btn.className = 'btn-cargar-mas';
                btn.textContent = 'Cargar más diseños';
                btn.onclick = () => enviarMensaje('cargar_mas');
                cargarContainer.appendChild(btn);
            }} else {{
                const msg = document.createElement('div');
                msg.className = 'footer-message';
                msg.textContent = '🌟 Has llegado al final del catálogo.';
                cargarContainer.appendChild(msg);
            }}
        }}

        // Delegación de eventos
        document.addEventListener('click', function(e) {{
            const btn = e.target.closest('button');
            if (!btn) return;
            const id = btn.dataset.id;
            if (!id) return;

            if (btn.classList.contains('qty-plus')) {{
                const pid = parseInt(id);
                cantidades[pid] = (cantidades[pid] || 0) + 1;
                const qtySpan = document.getElementById('qty-' + pid);
                if (qtySpan) qtySpan.textContent = cantidades[pid];
                const prod = productos.find(p => p.id === pid);
                const pin = qtySpan.closest('.pin');
                const footer = pin.querySelector('.pin-footer');
                const contenedor = footer.querySelector('div:first-child');
                const oldSub = contenedor.querySelector('.subtotal-display');
                if (oldSub) oldSub.remove();
                if (cantidades[pid] > 0) {{
                    const newSub = document.createElement('span');
                    newSub.className = 'subtotal-display';
                    newSub.textContent = 'Subtotal: $' + (prod.precio * cantidades[pid]).toFixed(2);
                    contenedor.appendChild(newSub);
                }}
                enviarMensaje({{ action: 'increment', id: pid }});
            }} else if (btn.classList.contains('qty-minus')) {{
                const pid = parseInt(id);
                if (cantidades[pid] > 0) {{
                    cantidades[pid]--;
                    const qtySpan = document.getElementById('qty-' + pid);
                    if (qtySpan) qtySpan.textContent = cantidades[pid];
                    const prod = productos.find(p => p.id === pid);
                    const pin = qtySpan.closest('.pin');
                    const footer = pin.querySelector('.pin-footer');
                    const contenedor = footer.querySelector('div:first-child');
                    const oldSub = contenedor.querySelector('.subtotal-display');
                    if (oldSub) oldSub.remove();
                    if (cantidades[pid] > 0) {{
                        const newSub = document.createElement('span');
                        newSub.className = 'subtotal-display';
                        newSub.textContent = 'Subtotal: $' + (prod.precio * cantidades[pid]).toFixed(2);
                        contenedor.appendChild(newSub);
                    }}
                    enviarMensaje({{ action: 'decrement', id: pid }});
                }}
            }} else if (btn.classList.contains('btn-pedir')) {{
                const pid = parseInt(id);
                const cant = cantidades[pid] || 0;
                if (cant === 0) {{
                    alert('Primero selecciona una cantidad con el botón +.');
                    return;
                }}
                const prod = productos.find(p => p.id === pid);
                const subtotal = (prod.precio * cant).toFixed(2);
                alert(`PEDIDO\\nDiseño: ${{prod.nombre}}\\nCantidad: ${{cant}}\\nSubtotal: $${subtotal}`);
            }}
        }});

        // Filtros
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const cat = this.dataset.category;
                filtroActual = cat;
                mostrarHasta = 9;
                enviarMensaje({{ action: 'filter', category: cat }});
            }});
        }});

        // Inicializar
        renderizar();
    </script>
</body>
</html>
    """
    return html

# =============================================
# CALLBACK PARA RECIBIR MENSAJES DEL IFRAME
# =============================================
def on_message(value):
    if value is None:
        return
    if isinstance(value, dict):
        if value.get("action") == "increment":
            pid = value.get("id")
            if pid in st.session_state.cantidades:
                st.session_state.cantidades[pid] += 1
                st.rerun()
        elif value.get("action") == "decrement":
            pid = value.get("id")
            if pid in st.session_state.cantidades and st.session_state.cantidades[pid] > 0:
                st.session_state.cantidades[pid] -= 1
                st.rerun()
        elif value.get("action") == "filter":
            st.session_state.filtro_actual = value.get("category", "all")
            st.session_state.mostrar_hasta = 9
            st.rerun()
    elif isinstance(value, str) and value == "cargar_mas":
        st.session_state.mostrar_hasta += 9
        st.rerun()

# =============================================
# CONFIGURAR PÁGINA Y MOSTRAR COMPONENTE
# =============================================
st.set_page_config(page_title="Catálogo de Bordados", layout="wide")

# Ocultar elementos de Streamlit
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { margin-top: -50px; }
</style>
""", unsafe_allow_html=True)

# Mostrar el componente con altura dinámica
st.components.v1.html(
    generar_html(),
    height=None,
    scrolling=False,
)

# Pequeño espacio al final
st.markdown("<br>", unsafe_allow_html=True)

# Nota: El callback on_message se ejecuta automáticamente al recibir mensajes
# porque el componente usa postMessage con el tipo 'streamlit:setComponentValue'.
