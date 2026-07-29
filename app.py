import streamlit as st

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
    # Más productos (para probar "Cargar más")
    {"id": 7, "nombre": "Mariposa 2", "categoria": "animales", "precio": 5.50, "imagen": "https://picsum.photos/seed/mariposa2/300/400", "personalizable": False},
    {"id": 8, "nombre": "Ramo 2", "categoria": "floral", "precio": 7.00, "imagen": "https://picsum.photos/seed/ramo2/300/350", "personalizable": False},
    {"id": 9, "nombre": "Letra A", "categoria": "letras", "precio": 3.50, "imagen": "https://picsum.photos/seed/letraA/300/420", "personalizable": True},
    {"id": 10, "nombre": "Águila 2", "categoria": "animales", "precio": 9.00, "imagen": "https://picsum.photos/seed/aguila2/300/390", "personalizable": False},
    {"id": 11, "nombre": "Mandala 2", "categoria": "geometrico", "precio": 7.50, "imagen": "https://picsum.photos/seed/mandala2/300/360", "personalizable": False},
    {"id": 12, "nombre": "Nombre 2", "categoria": "nombres", "precio": 4.50, "imagen": "https://picsum.photos/seed/nombre2/300/470", "personalizable": True},
]

# =============================================
# CONFIGURACIÓN DE ESTADO
# =============================================
if "mostrar_hasta" not in st.session_state:
    st.session_state.mostrar_hasta = 9
if "cantidades" not in st.session_state:
    st.session_state.cantidades = {p["id"]: 0 for p in PRODUCTOS}
if "filtro_actual" not in st.session_state:
    st.session_state.filtro_actual = "all"

# =============================================
# FUNCIÓN PARA GENERAR EL HTML (con llaves escapadas)
# =============================================
def generar_html():
    filtro = st.session_state.filtro_actual
    productos_filtrados = PRODUCTOS if filtro == "all" else [p for p in PRODUCTOS if p["categoria"] == filtro]
    productos_visibles = productos_filtrados[:st.session_state.mostrar_hasta]

    # Construir tarjetas
    tarjetas = ""
    for prod in productos_visibles:
        cant = st.session_state.cantidades.get(prod["id"], 0)
        subtotal = prod["precio"] * cant
        badge = '<span class="badge-personalizable">Personalizable</span>' if prod["personalizable"] else ""
        subtotal_html = f'<span class="subtotal-display">Subtotal: ${subtotal:.2f}</span>' if cant > 0 else ""

        tarjetas += f"""
        <div class="pin">
            <div class="pin-image-wrapper">
                <img src="{prod["imagen"]}" alt="{prod["nombre"]}" loading="lazy">
                {badge}
                <div class="pin-overlay">
                    <span class="pin-nombre">{prod["nombre"]}</span>
                    <span class="pin-precio">${prod["precio"]:.2f}</span>
                </div>
            </div>
            <div class="pin-footer">
                <div>{subtotal_html}</div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <div class="quantity-control" data-id="{prod["id"]}">
                        <button class="qty-minus" data-id="{prod["id"]}">−</button>
                        <span class="qty-number" id="qty-{prod["id"]}">{cant}</span>
                        <button class="qty-plus" data-id="{prod["id"]}">+</button>
                    </div>
                    <button class="btn-pedir" data-id="{prod["id"]}">Pedir</button>
                </div>
            </div>
        </div>
        """

    # Botón "Cargar más"
    cargar_mas_btn = ""
    if len(productos_filtrados) > st.session_state.mostrar_hasta:
        cargar_mas_btn = f"""
        <div style="text-align:center; margin: 30px 0;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'cargar_mas'}}, '*')"
                    style="background:#1A5F7A; color:white; border:none; padding:12px 40px; border-radius:30px; font-size:1.1rem; font-weight:600; cursor:pointer; box-shadow:0 4px 15px rgba(26,95,122,0.3);">
                Cargar más diseños
            </button>
        </div>
        """

    # HTML COMPLETO (TODAS LAS LLAVES { } DENTRO DE JAVASCRIPT O CSS DEBEN SER DOBLES {{ }})
    # ¡Aquí está la clave! ESCAPAMOS todas las llaves que no sean para Python
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; font-family: 'Inter', -apple-system, sans-serif; }}
            body {{
                background: transparent;
                padding: 0;
                margin: 0;
                max-width: 1400px;
                margin: 0 auto;
            }}
            .header {{
                margin-bottom: 30px;
                padding-top: 20px;
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

        <div class="filters">
            <button class="filter-btn active" data-category="all">Todas</button>
            <button class="filter-btn" data-category="animales">Animales</button>
            <button class="filter-btn" data-category="floral">Floral</button>
            <button class="filter-btn" data-category="geometrico">Geométrico</button>
            <button class="filter-btn" data-category="letras">Letras</button>
            <button class="filter-btn" data-category="nombres">Nombres</button>
        </div>

        <div class="masonry" id="masonry">
            {tarjetas}
        </div>

        {cargar_mas_btn}

        <script>
            // Productos (solo para referencia en el frontend)
            const productos = {PRODUCTOS};

            // Estado de cantidades (se sincroniza con Python mediante postMessage)
            let cantidades = {{}};
            productos.forEach(p => cantidades[p.id] = 0);

            // Inicializar cantidades desde Python
            const cantidadesPython = {st.session_state.cantidades};
            Object.keys(cantidadesPython).forEach(id => {{
                cantidades[id] = cantidadesPython[id] || 0;
            }});

            // Actualizar UI de una tarjeta
            function actualizarUI(id) {{
                const qtySpan = document.getElementById('qty-' + id);
                if (!qtySpan) return;
                qtySpan.textContent = cantidades[id] || 0;

                const pin = qtySpan.closest('.pin');
                if (!pin) return;
                const footer = pin.querySelector('.pin-footer');
                const subtotalContainer = footer.querySelector('div:first-child');
                const prod = productos.find(p => p.id == id);
                const subtotal = prod.precio * (cantidades[id] || 0);

                // Eliminar subtotal anterior
                const oldSub = subtotalContainer.querySelector('.subtotal-display');
                if (oldSub) oldSub.remove();

                // Agregar nuevo si > 0
                if (cantidades[id] > 0) {{
                    const newSub = document.createElement('span');
                    newSub.className = 'subtotal-display';
                    newSub.textContent = 'Subtotal: $' + subtotal.toFixed(2);
                    subtotalContainer.appendChild(newSub);
                }}
            }}

            // Manejar eventos de los botones
            document.addEventListener('click', function(e) {{
                const btn = e.target.closest('button');
                if (!btn) return;
                const id = btn.dataset.id;
                if (!id) return;

                if (btn.classList.contains('qty-plus')) {{
                    cantidades[id] = (cantidades[id] || 0) + 1;
                    actualizarUI(id);
                    // Enviar a Streamlit
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{ action: 'increment', id: parseInt(id) }}
                    }}, '*');
                }} else if (btn.classList.contains('qty-minus')) {{
                    if (cantidades[id] > 0) {{
                        cantidades[id]--;
                        actualizarUI(id);
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: {{ action: 'decrement', id: parseInt(id) }}
                        }}, '*');
                    }}
                }} else if (btn.classList.contains('btn-pedir')) {{
                    const cant = cantidades[id] || 0;
                    if (cant === 0) {{
                        alert('Primero selecciona una cantidad con el botón +.');
                        return;
                    }}
                    const prod = productos.find(p => p.id == id);
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
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{ action: 'filter', category: cat }}
                    }}, '*');
                }});
            }});

            // Cargar más diseños (capturar el botón con onclick)
            document.querySelector('[onclick*="cargar_mas"]')?.addEventListener('click', function() {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: 'cargar_mas'
                }}, '*');
            }});
        </script>
    </body>
    </html>
    """
    return html

# =============================================
# APLICACIÓN STREAMLIT
# =============================================
st.set_page_config(page_title="Catálogo de Bordados", layout="wide")

# Renderizar el HTML
st.components.v1.html(
    generar_html(),
    height=10000,
    scrolling=True,
)
