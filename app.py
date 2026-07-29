import streamlit as st

# Toda la interfaz (HTML, CSS y JS) va aquí dentro
HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Bordados</title>
    <style>
        /* ----- RESET Y ESTILOS GENERALES ----- */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        body {
            background-color: #F8FAFC;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2rem;
            color: #1A5F7A;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .header p {
            color: #64748B;
            font-size: 1.1rem;
            margin-top: 5px;
        }

        /* ----- FILTROS (PÍLDORAS) ----- */
        .filters {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 15px;
        }
        .filter-btn {
            padding: 8px 20px;
            border-radius: 30px;
            border: 1.5px solid #CBD5E1;
            background: transparent;
            color: #64748B;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .filter-btn:hover {
            border-color: #1A5F7A;
            color: #1A5F7A;
        }
        .filter-btn.active {
            background: #1A5F7A;
            border-color: #1A5F7A;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(26, 95, 122, 0.3);
        }

        /* ----- MURO (MASONRY) ----- */
        .masonry {
            column-count: 3;
            column-gap: 20px;
            margin-bottom: 40px;
        }

        /* ----- TARJETA (PIN) ----- */
        .pin {
            break-inside: avoid;
            margin-bottom: 20px;
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease;
            position: relative;
            cursor: pointer;
        }
        .pin:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.15);
        }
        .pin:hover img {
            transform: scale(1.03);
        }
        .pin img {
            width: 100%;
            display: block;
            transition: transform 0.4s ease;
        }
        .pin-image-wrapper {
            position: relative;
        }

        /* Badge "Personalizable" */
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
            letter-spacing: 0.3px;
            display: flex;
            align-items: center;
            gap: 4px;
            z-index: 5;
            box-shadow: 0 2px 8px rgba(34, 163, 159, 0.4);
        }

        /* Overlay inferior */
        .pin-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 30px 15px 15px 15px;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
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
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 12px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
        }

        /* ----- CONTROL DE CANTIDAD ----- */
        .quantity-control {
            position: absolute;
            bottom: 15px;
            right: 15px;
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(8px);
            padding: 4px 6px;
            border-radius: 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10;
            pointer-events: auto;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .quantity-control button {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: none;
            font-size: 1.2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .qty-minus {
            background: transparent;
            color: #1A5F7A;
            border: 1.5px solid #CBD5E1 !important;
        }
        .qty-minus:hover {
            background: #F1F5F9;
        }
        .qty-number {
            font-size: 1rem;
            font-weight: 700;
            color: #1A5F7A;
            min-width: 24px;
            text-align: center;
        }
        .qty-plus {
            background: #1A5F7A;
            color: white;
            box-shadow: 0 2px 8px rgba(26, 95, 122, 0.4);
        }
        .qty-plus:hover {
            background: #0f4a5e;
            transform: scale(1.05);
        }

        /* ----- BOTÓN FLOTANTE DEL CARRITO ----- */
        .cart-float {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 100;
            background: #1A5F7A;
            color: white;
            border: none;
            padding: 16px 28px;
            border-radius: 60px;
            font-size: 1.1rem;
            font-weight: 600;
            box-shadow: 0 8px 30px rgba(26, 95, 122, 0.5);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
        }
        .cart-float:hover {
            transform: scale(1.05);
            background: #0f4a5e;
        }
        .cart-float .total-badge {
            background: white;
            color: #1A5F7A;
            padding: 2px 12px;
            border-radius: 30px;
            font-weight: 700;
        }

        /* ----- TOAST (NOTIFICACIÓN) ----- */
        .toast {
            position: fixed;
            bottom: 100px;
            right: 30px;
            background: #1A5F7A;
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            font-weight: 500;
            z-index: 200;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.4s ease;
            pointer-events: none;
            border-left: 5px solid #22A39F;
        }
        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        /* ----- MODAL (CHECKOUT) ----- */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(6px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .modal-overlay.active {
            display: flex;
        }
        .modal-content {
            background: white;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 35px;
            border-radius: 24px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.3);
            animation: fadeInUp 0.3s ease;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: scale(0.95) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }
        .modal-content h2 {
            color: #1A5F7A;
            font-size: 1.8rem;
            margin-bottom: 20px;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 10px;
        }
        .modal-resumen {
            background: #F8FAFC;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .modal-resumen-item {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px dashed #E2E8F0;
            font-size: 0.95rem;
        }
        .modal-resumen-item:last-child {
            border-bottom: none;
        }
        .modal-total {
            display: flex;
            justify-content: space-between;
            font-size: 1.4rem;
            font-weight: 700;
            color: #1A5F7A;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 2px solid #1A5F7A;
        }
        .form-group {
            margin-bottom: 18px;
        }
        .form-group label {
            display: block;
            font-weight: 600;
            color: #1A2B3C;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 15px;
            border: 1.5px solid #E2E8F0;
            border-radius: 12px;
            font-size: 1rem;
            transition: 0.2s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #1A5F7A;
            box-shadow: 0 0 0 3px rgba(26, 95, 122, 0.1);
        }
        .payment-options {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .payment-options button {
            padding: 10px 20px;
            border-radius: 30px;
            border: 2px solid #E2E8F0;
            background: white;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
            flex: 1;
            min-width: 80px;
        }
        .payment-options button.selected {
            border-color: #1A5F7A;
            background: #EFF6FF;
            color: #1A5F7A;
            font-weight: 600;
            box-shadow: 0 0 0 3px rgba(26, 95, 122, 0.15);
        }
        .file-upload {
            border: 2px dashed #CBD5E1;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .file-upload:hover {
            border-color: #1A5F7A;
            background: #F8FAFC;
        }
        .file-upload input {
            display: none;
        }
        .btn-submit {
            width: 100%;
            padding: 14px;
            background: #1A5F7A;
            color: white;
            border: none;
            border-radius: 14px;
            font-size: 1.2rem;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
            margin-top: 10px;
        }
        .btn-submit:hover {
            background: #0f4a5e;
        }
        .btn-close-modal {
            background: transparent;
            border: none;
            font-size: 1.5rem;
            float: right;
            cursor: pointer;
            color: #94A3B8;
        }

        /* ----- RESPONSIVE ----- */
        @media (max-width: 768px) {
            .masonry { column-count: 2; column-gap: 12px; }
            .header h1 { font-size: 1.6rem; }
            .cart-float { padding: 12px 20px; font-size: 0.9rem; bottom: 20px; right: 20px; }
            .modal-content { padding: 25px; margin: 10px; }
            .quantity-control { bottom: 10px; right: 10px; }
            .quantity-control button { width: 28px; height: 28px; font-size: 1rem; }
            .pin-overlay { padding: 20px 10px 10px 10px; }
            .pin-nombre { font-size: 0.85rem; }
            .pin-precio { font-size: 0.9rem; }
        }
        @media (max-width: 480px) {
            .masonry { column-count: 2; column-gap: 8px; }
            .filter-btn { padding: 6px 14px; font-size: 0.8rem; }
        }
    </style>
</head>
<body>

    <!-- HEADER -->
    <div class="header">
        <h1>🧵 Catálogo de Diseños</h1>
        <p>Un muro de inspiración — ajusta cantidades y agrega a tu pedido.</p>
    </div>

    <!-- FILTROS -->
    <div class="filters" id="filters">
        <button class="filter-btn active" data-category="all">Todas</button>
        <button class="filter-btn" data-category="animales">Animales</button>
        <button class="filter-btn" data-category="floral">Floral</button>
        <button class="filter-btn" data-category="geometrico">Geométrico</button>
        <button class="filter-btn" data-category="letras">Letras</button>
        <button class="filter-btn" data-category="nombres">Nombres</button>
    </div>

    <!-- MURO MASONRY -->
    <div class="masonry" id="masonry"></div>

    <!-- TOAST -->
    <div class="toast" id="toast"></div>

    <!-- BOTÓN FLOTANTE CARRITO -->
    <button class="cart-float" id="openModalBtn">
        🛒 Ver Pedido
        <span class="total-badge" id="cartTotal">$0.00</span>
    </button>

    <!-- MODAL CHECKOUT -->
    <div class="modal-overlay" id="checkoutModal">
        <div class="modal-content">
            <button class="btn-close-modal" id="closeModalBtn">✕</button>
            <h2>📋 Finalizar Pedido</h2>

            <div class="modal-resumen" id="modalResumen">
                <!-- Se llena con JS -->
            </div>

            <div class="form-group">
                <label>Nombre y Apellido</label>
                <input type="text" id="clienteNombre" placeholder="Ej: Ana Pérez">
            </div>

            <div class="form-group">
                <label>Tipo de Persona</label>
                <select id="clienteTipo">
                    <option value="natural">Persona Natural</option>
                    <option value="empresa">Empresa</option>
                </select>
            </div>

            <div class="form-group">
                <label>Método de Pago</label>
                <div class="payment-options" id="paymentOptions">
                    <button data-method="yape">📱 Yape</button>
                    <button data-method="plin">📱 Plin</button>
                    <button data-method="transferencia">🏦 Transferencia</button>
                    <button data-method="efectivo">💵 Efectivo</button>
                </div>
            </div>

            <div class="form-group">
                <label>Adjuntar Captura de Pago</label>
                <div class="file-upload" id="fileUploadBox">
                    <p>📤 Haz clic para subir o arrastra tu captura</p>
                    <input type="file" id="fileInput" accept="image/*">
                </div>
                <span id="fileNombre" style="font-size:0.9rem; color:#22A39F; display:block; margin-top:5px;"></span>
            </div>

            <button class="btn-submit" id="submitPedidoBtn">✅ Enviar Pedido</button>
        </div>
    </div>

    <script>
        // ----- DATOS DE PRODUCTOS -----
        const productos = [
            { id: 1, nombre: "Mariposa Monarca", categoria: "animales", precio: 5.00, imagen: "https://picsum.photos/seed/mariposa/300/450", personalizable: false },
            { id: 2, nombre: "Ramo Floral", categoria: "floral", precio: 6.50, imagen: "https://picsum.photos/seed/ramo/300/320", personalizable: false },
            { id: 3, nombre: "Iniciales", categoria: "letras", precio: 4.00, imagen: "https://picsum.photos/seed/inicial/300/500", personalizable: true },
            { id: 4, nombre: "Águila Real", categoria: "animales", precio: 8.00, imagen: "https://picsum.photos/seed/aguila/300/380", personalizable: false },
            { id: 5, nombre: "Mandala", categoria: "geometrico", precio: 7.00, imagen: "https://picsum.photos/seed/mandala/300/350", personalizable: false },
            { id: 6, nombre: "Nombre Propio", categoria: "nombres", precio: 4.00, imagen: "https://picsum.photos/seed/nombre/300/480", personalizable: true }
        ];

        // ----- ESTADO GLOBAL -----
        let carrito = {}; // { id: cantidad }

        // ----- REFERENCIAS DOM -----
        const masonry = document.getElementById('masonry');
        const toast = document.getElementById('toast');
        const cartTotalSpan = document.getElementById('cartTotal');
        const modal = document.getElementById('checkoutModal');
        const modalResumen = document.getElementById('modalResumen');
        const openModalBtn = document.getElementById('openModalBtn');
        const closeModalBtn = document.getElementById('closeModalBtn');
        const fileInput = document.getElementById('fileInput');
        const fileNombre = document.getElementById('fileNombre');
        const submitBtn = document.getElementById('submitPedidoBtn');

        // ----- RENDERIZAR MURO -----
        function renderProductos(filtro = 'all') {
            masonry.innerHTML = '';
            const filtrados = filtro === 'all' ? productos : productos.filter(p => p.categoria === filtro);
            
            filtrados.forEach(prod => {
                const cant = carrito[prod.id] || 0;
                const pin = document.createElement('div');
                pin.className = 'pin';
                pin.innerHTML = `
                    <div class="pin-image-wrapper">
                        <img src="${prod.imagen}" alt="${prod.nombre}" loading="lazy">
                        ${prod.personalizable ? `<span class="badge-personalizable">✏️ Personalizable</span>` : ''}
                        <div class="pin-overlay">
                            <span class="pin-nombre">${prod.nombre}</span>
                            <span class="pin-precio">$${prod.precio.toFixed(2)}</span>
                        </div>
                        <div class="quantity-control" data-id="${prod.id}">
                            <button class="qty-minus" data-id="${prod.id}">−</button>
                            <span class="qty-number" id="qty-${prod.id}">${cant}</span>
                            <button class="qty-plus" data-id="${prod.id}">+</button>
                        </div>
                    </div>
                `;
                masonry.appendChild(pin);
            });

            // Asignar eventos a los botones después de renderizar
            document.querySelectorAll('.qty-plus').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    agregarProducto(id);
                });
            });
            document.querySelectorAll('.qty-minus').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    quitarProducto(id);
                });
            });
        }

        // ----- FUNCIONES CARRITO -----
        function agregarProducto(id) {
            if (!carrito[id]) carrito[id] = 0;
            carrito[id] += 1;
            actualizarUI(id);
            
            // Toast
            const prod = productos.find(p => p.id === id);
            mostrarToast(`🧵 ${prod.nombre} agregado. Subtotal: $${(prod.precio * carrito[id]).toFixed(2)}`);
        }

        function quitarProducto(id) {
            if (carrito[id] && carrito[id] > 0) {
                carrito[id] -= 1;
                if (carrito[id] === 0) delete carrito[id];
                actualizarUI(id);
            }
        }

        function actualizarUI(id) {
            // Actualizar número en la tarjeta
            const qtySpan = document.getElementById(`qty-${id}`);
            if (qtySpan) qtySpan.textContent = carrito[id] || 0;

            // Actualizar total general
            let total = 0;
            for (const [pid, cant] of Object.entries(carrito)) {
                const prod = productos.find(p => p.id === parseInt(pid));
                if (prod) total += prod.precio * cant;
            }
            cartTotalSpan.textContent = `$${total.toFixed(2)}`;

            // Actualizar el resumen del modal si está abierto
            if (modal.classList.contains('active')) {
                actualizarModal();
            }
        }

        function mostrarToast(mensaje) {
            toast.textContent = mensaje;
            toast.classList.add('show');
            clearTimeout(toast._timeout);
            toast._timeout = setTimeout(() => toast.classList.remove('show'), 2000);
        }

        // ----- FILTROS -----
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const cat = this.dataset.category;
                renderProductos(cat);
                // Re-aplicar cantidades en el nuevo render
                for (const [id, cant] of Object.entries(carrito)) {
                    const span = document.getElementById(`qty-${id}`);
                    if (span) span.textContent = cant;
                }
            });
        });

        // ----- MODAL -----
        function actualizarModal() {
            let html = '';
            let totalGeneral = 0;
            let items = [];

            for (const [pid, cant] of Object.entries(carrito)) {
                if (cant === 0) continue;
                const prod = productos.find(p => p.id === parseInt(pid));
                if (!prod) continue;
                const subtotal = prod.precio * cant;
                totalGeneral += subtotal;
                items.push({ nombre: prod.nombre, cant, unitario: prod.precio, subtotal });
            }

            if (items.length === 0) {
                html = '<p style="color: #94A3B8; text-align:center; padding:20px;">No has agregado ningún diseño aún.</p>';
            } else {
                items.forEach(item => {
                    html += `
                        <div class="modal-resumen-item">
                            <span><strong>${item.nombre}</strong> x${item.cant}</span>
                            <span>$${item.subtotal.toFixed(2)} <small style="color:#94A3B8;">($${item.unitario.toFixed(2)} c/u)</small></span>
                        </div>
                    `;
                });
                html += `
                    <div class="modal-total">
                        <span>💰 TOTAL</span>
                        <span>$${totalGeneral.toFixed(2)}</span>
                    </div>
                `;
            }
            modalResumen.innerHTML = html;
        }

        openModalBtn.addEventListener('click', () => {
            actualizarModal();
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        closeModalBtn.addEventListener('click', () => {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });

        // ----- MÉTODOS DE PAGO -----
        document.querySelectorAll('.payment-options button').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.payment-options button').forEach(b => b.classList.remove('selected'));
                this.classList.add('selected');
            });
        });

        // ----- SUBIDA DE ARCHIVO -----
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileNombre.textContent = `📎 Archivo seleccionado: ${this.files[0].name}`;
            }
        });

        document.getElementById('fileUploadBox').addEventListener('click', () => fileInput.click());

        // ----- ENVIAR PEDIDO -----
        submitBtn.addEventListener('click', () => {
            const nombre = document.getElementById('clienteNombre').value.trim();
            const tipo = document.getElementById('clienteTipo').value;
            const metodoSeleccionado = document.querySelector('.payment-options button.selected');
            const metodo = metodoSeleccionado ? metodoSeleccionado.textContent.trim() : 'No seleccionado';
            const archivo = fileInput.files[0];

            if (!nombre) {
                alert('⚠️ Por favor, ingresa tu nombre y apellido.');
                return;
            }

            let resumen = `🧾 PEDIDO CONFIRMADO\n`;
            resumen += `👤 Cliente: ${nombre}\n`;
            resumen += `🏢 Tipo: ${tipo === 'natural' ? 'Persona Natural' : 'Empresa'}\n`;
            resumen += `💳 Pago: ${metodo}\n`;
            resumen += `📎 Archivo: ${archivo ? archivo.name : 'No se adjuntó captura'}\n`;
            resumen += `───────────────────\n`;

            let total = 0;
            for (const [pid, cant] of Object.entries(carrito)) {
                if (cant === 0) continue;
                const prod = productos.find(p => p.id === parseInt(pid));
                if (prod) {
                    const subtotal = prod.precio * cant;
                    total += subtotal;
                    resumen += `${prod.nombre} x${cant} = $${subtotal.toFixed(2)}\n`;
                }
            }
            resumen += `───────────────────\n`;
            resumen += `💰 TOTAL A PAGAR: $${total.toFixed(2)}`;

            alert(resumen);
            
            // (Opcional) Resetear carrito después de enviar
            // carrito = {};
            // renderProductos();
            // cartTotalSpan.textContent = '$0.00';
            // modal.classList.remove('active');
            // document.body.style.overflow = 'auto';
        });

        // ----- INICIALIZAR -----
        renderProductos('all');
    </script>
</body>
</html>
"""

# ----- STREAMLIT APP -----
st.set_page_config(page_title="Catálogo de Bordados", layout="wide")
st.components.v1.html(HTML_CODE, height=1200, scrolling=True)
