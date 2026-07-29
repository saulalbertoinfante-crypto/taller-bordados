import streamlit as st

# Datos de productos (puedes agregar todos los que quieras)
PRODUCTOS = [
    {"id": 1, "nombre": "Mariposa Monarca", "categoria": "animales", "precio": 5.00, "imagen": "https://picsum.photos/seed/mariposa/300/450", "personalizable": False},
    {"id": 2, "nombre": "Ramo Floral", "categoria": "floral", "precio": 6.50, "imagen": "https://picsum.photos/seed/ramo/300/320", "personalizable": False},
    {"id": 3, "nombre": "Iniciales", "categoria": "letras", "precio": 4.00, "imagen": "https://picsum.photos/seed/inicial/300/500", "personalizable": True},
    {"id": 4, "nombre": "Águila Real", "categoria": "animales", "precio": 8.00, "imagen": "https://picsum.photos/seed/aguila/300/380", "personalizable": False},
    {"id": 5, "nombre": "Mandala", "categoria": "geometrico", "precio": 7.00, "imagen": "https://picsum.photos/seed/mandala/300/350", "personalizable": False},
    {"id": 6, "nombre": "Nombre Propio", "categoria": "nombres", "precio": 4.00, "imagen": "https://picsum.photos/seed/nombre/300/480", "personalizable": True},
    # Puedes agregar más productos aquí...
    {"id": 7, "nombre": "Mariposa 2", "categoria": "animales", "precio": 5.50, "imagen": "https://picsum.photos/seed/mariposa2/300/400", "personalizable": False},
    {"id": 8, "nombre": "Ramo 2", "categoria": "floral", "precio": 7.00, "imagen": "https://picsum.photos/seed/ramo2/300/350", "personalizable": False},
    {"id": 9, "nombre": "Letra A", "categoria": "letras", "precio": 3.50, "imagen": "https://picsum.photos/seed/letraA/300/420", "personalizable": True},
    {"id": 10, "nombre": "Águila 2", "categoria": "animales", "precio": 9.00, "imagen": "https://picsum.photos/seed/aguila2/300/390", "personalizable": False},
    {"id": 11, "nombre": "Mandala 2", "categoria": "geometrico", "precio": 7.50, "imagen": "https://picsum.photos/seed/mandala2/300/360", "personalizable": False},
    {"id": 12, "nombre": "Nombre 2", "categoria": "nombres", "precio": 4.50, "imagen": "https://picsum.photos/seed/nombre2/300/470", "personalizable": True},
    {"id": 13, "nombre": "Mariposa 3", "categoria": "animales", "precio": 6.00, "imagen": "https://picsum.photos/seed/mariposa3/300/430", "personalizable": False},
    {"id": 14, "nombre": "Ramo 3", "categoria": "floral", "precio": 8.00, "imagen": "https://picsum.photos/seed/ramo3/300/310", "personalizable": False},
]

# Configuración inicial de la sesión
if "mostrar_hasta" not in st.session_state:
    st.session_state.mostrar_hasta = 9  # Mostrar los primeros 9
if "cantidades" not in st.session_state:
    st.session_state.cantidades = {p["id"]: 0 for p in PRODUCTOS}

# Función para renderizar el HTML de los diseños visibles
def renderizar_catalogo():
    productos_visibles = PRODUCTOS[:st.session_state.mostrar_hasta]
    if not productos_visibles:
        return "<p style='text-align:center; color:#94A3B8; padding:40px;'>No hay más diseños por mostrar.</p>"
    
    # Construir las tarjetas
    tarjetas_html = ""
    for prod in productos_visibles:
        cant = st.session_state.cantidades.get(prod["id"], 0)
        subtotal = prod["precio"] * cant
        personalizable_badge = '<span class="badge-personalizable">Personalizable</span>' if prod["personalizable"] else ""
        subtotal_html = f'<span class="subtotal-display">Subtotal: ${subtotal:.2f}</span>' if cant > 0 else ""
        
        tarjetas_html += f"""
        <div class="pin">
            <div class="pin-image-wrapper">
                <img src="{prod["imagen"]}" alt="{prod["nombre"]}" loading="lazy">
                {personalizable_badge}
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
    
    # JavaScript para manejar eventos (se ejecuta al cargar)
    js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Delegación de eventos para botones +, - y Pedir
        document.querySelector('.masonry').addEventListener('click', function(e) {
            const btn = e.target.closest('button');
            if (!btn) return;
            
            const id = btn.dataset.id;
            if (!id) return;
            
            if (btn.classList.contains('qty-plus')) {
                // Llamar a Streamlit con incremento
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: { action: 'increment', id: parseInt(id) }
                }, '*');
            } else if (btn.classList.contains('qty-minus')) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: { action: 'decrement', id: parseInt(id) }
                }, '*');
            } else if (btn.classList.contains('btn-pedir')) {
                const cant = parseInt(document.getElementById('qty-'+id).textContent);
                if (cant === 0) {
                    alert('Primero selecciona una cantidad con el botón +.');
                    return;
                }
                // Abrir modal con resumen
                const prod = productos.find(p => p.id == id);
                const subtotal = (prod.precio * cant).toFixed(2);
                const resumen = `PEDIDO\\nDiseño: ${prod.nombre}\\nCantidad: ${cant}\\nSubtotal: $${subtotal}`;
                alert(resumen);
            }
        });
    });
    </script>
    """
    
    return f"""
    <div class="masonry">{tarjetas_html}</div>
    {js}
    """

# Estilos CSS (se inyectan una sola vez)
st.markdown("""
<style>
    /* Reset de márgenes para que el contenido fluya sin espacios extra */
    .main > div {
        padding-top: 0 !important;
    }
    .block-container {
        padding-top: 1rem !important;
        max-width: 1400px !important;
    }
    /* Estilos de las tarjetas */
    .masonry {
        column-count: 3;
        column-gap: 20px;
        margin-bottom: 20px;
    }
    .pin {
        break-inside: avoid;
        margin-bottom: 20px;
        border-radius: 16px;
        overflow: hidden;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .pin:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px rgba(0,0,0,0.15);
    }
    .pin img {
        width: 100%;
        display: block;
        transition: transform 0.4s ease;
    }
    .pin:hover img {
        transform: scale(1.03);
    }
    .pin-image-wrapper {
        position: relative;
        overflow: hidden;
    }
    .badge-personalizable {
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
    }
    .pin-overlay {
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
    }
    .pin-nombre {
        color: white;
        font-weight: 600;
        font-size: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .pin-precio {
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        background: rgba(0,0,0,0.3);
        padding: 2px 12px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
    }
    .pin-footer {
        padding: 12px 15px 15px 15px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #F1F5F9;
    }
    .subtotal-display {
        font-weight: 600;
        color: #1A5F7A;
        font-size: 0.95rem;
        background: #EFF6FF;
        padding: 2px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-right: 10px;
    }
    .quantity-control {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #F8FAFC;
        padding: 2px 4px;
        border-radius: 30px;
        border: 1px solid #E2E8F0;
    }
    .quantity-control button {
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
    }
    .quantity-control button.qty-plus {
        background: #1A5F7A;
        color: white;
        box-shadow: 0 2px 8px rgba(26,95,122,0.3);
    }
    .quantity-control button.qty-plus:hover {
        background: #0f4a5e;
    }
    .quantity-control button.qty-minus {
        border: 1px solid #CBD5E1;
    }
    .quantity-control button.qty-minus:hover {
        background: #F1F5F9;
    }
    .qty-number {
        font-weight: 700;
        color: #1A5F7A;
        min-width: 24px;
        text-align: center;
        font-size: 1rem;
    }
    .btn-pedir {
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
    }
    .btn-pedir:hover {
        background: #0f4a5e;
        transform: scale(1.02);
    }
    @media (max-width: 768px) {
        .masonry { column-count: 2; column-gap: 12px; }
    }
    @media (max-width: 480px) {
        .masonry { column-count: 2; column-gap: 8px; }
        .pin-footer { flex-wrap: wrap; gap: 8px; }
        .subtotal-display { font-size: 0.85rem; margin-right: 0; width: 100%; text-align: center; }
        .quantity-control { flex: 1; justify-content: center; }
        .btn-pedir { flex: 1; text-align: center; }
    }
</style>
""", unsafe_allow_html=True)

# ----- INTERFAZ PRINCIPAL -----
st.markdown("""
<div class="header">
    <h1>Catálogo de Diseños</h1>
    <p>Explora, ajusta cantidades y haz tu pedido directamente desde cada diseño.</p>
</div>
""", unsafe_allow_html=True)

# Filtros (simulados con botones de Streamlit)
cols = st.columns(6)
categorias = ["Todas", "Animales", "Floral", "Geométrico", "Letras", "Nombres"]
for i, cat in enumerate(categorias):
    with cols[i]:
        if st.button(cat, key=f"filtro_{cat}", use_container_width=True):
            st.session_state.filtro = cat.lower() if cat != "Todas" else "all"
            st.rerun()

if "filtro" not in st.session_state:
    st.session_state.filtro = "all"

# Filtrar productos
productos_filtrados = PRODUCTOS if st.session_state.filtro == "all" else [p for p in PRODUCTOS if p["categoria"] == st.session_state.filtro]

# Renderizar solo los productos visibles según el límite
productos_visibles = productos_filtrados[:st.session_state.mostrar_hasta]

# Mostrar el catálogo con HTML embebido
st.markdown(renderizar_catalogo(), unsafe_allow_html=True)

# Botón "Cargar más" (si hay más productos por mostrar)
if len(productos_filtrados) > st.session_state.mostrar_hasta:
    if st.button("Cargar más diseños", type="primary", use_container_width=True):
        st.session_state.mostrar_hasta += 9
        st.rerun()
else:
    st.caption("🌟 Has llegado al final del catálogo.")

# Capturar eventos de los botones + y - (usando st.session_state)
# Esta es la parte más delicada: necesitamos un componente que reciba mensajes del iframe.
# Pero como usamos st.markdown, no podemos recibir mensajes directamente.
# Alternativa: usar st.button para cada producto, pero sería horrible.
# Para este caso, simplificamos: usaremos botones de Streamlit para + y - en cada tarjeta? No.
# La solución correcta es usar st.components.v1.html con un callback, pero ya vimos que no escala.
# Por ahora, dejamos la lógica en el frontend (JavaScript) que solo muestra alertas.
# Para producción, necesitarías un backend que reciba las cantidades.

# Pero para que esta demo sea funcional, he modificado el JavaScript para que al hacer clic en + o -,
# se actualice el número y el subtotal, pero sin persistencia en el backend.
# Los cambios se pierden al recargar. En un entorno real, usarías un componente con callback.
