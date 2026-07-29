import streamlit as st

HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Bordados</title>
    <style>
        /* Reset y base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        body {
            background: #F8FAFC;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
            /* Eliminamos cualquier overflow oculto para que el scroll sea natural */
            overflow-y: auto;
            height: auto;
        }
        .header {
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2rem;
            color: #1A5F7A;
            font-weight: 600;
        }
        .header p {
            color: #64748B;
            font-size: 1.1rem;
        }

        /* Filtros */
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
            transition: all 0.2s;
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

        /* Muro Masonry */
        .masonry {
            column-count: 3;
            column-gap: 20px;
            margin-bottom: 40px;
        }

        /* Tarjeta */
        .pin {
            break-inside: avoid;
            margin-bottom: 20px;
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease;
        }
        .pin:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.15);
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

        /* Badge Personalizable */
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
            box-shadow: 0 2px 8px rgba(34, 163, 159, 0.4);
            letter-spacing: 0.3px;
        }

        /* Overlay inferior (nombre + precio) */
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
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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

        /* Info inferior de la tarjeta (controles) */
        .pin-footer {
            padding: 12px 15px 15px 15px;
            background: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid #F1F5F9;
        }

        /* Subtotal (sin iconos) */
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

        /* Control de cantidad */
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
            box-shadow: 0 2px 8px rgba(26, 95, 122, 0.3);
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

        /* Botón Pedir */
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
            box-shadow: 0 4px 12px rgba(26, 95, 122, 0.3);
        }
        .btn-pedir:hover {
            background: #0f4a5e;
            transform: scale(1.02);
        }

        /* ----- MODAL (Checkout individual) ----- */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
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
            max-width: 500px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.3s ease;
            position: relative;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: scale(0.95) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }
        .modal-content h2 {
            color: #1A5F7A;
            font-size: 1.5rem;
            margin-bottom: 15px;
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
            font-size: 1.3rem;
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
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px 15px;
            border: 1.5px solid #E2E8F0;
            border-radius: 12px;
            font-size: 1rem;
            transition: 0.2s;
        }
        .form-group input:focus,
        .form-group select:focus {
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
            padding: 10px 16px;
            border-radius: 30px;
            border: 2px solid #E2E8F0;
            background: white;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
            flex: 1;
            min-width: 70px;
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
            padding: 20px;
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
            font-size: 1.1rem;
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
            font-size: 1.8rem;
            position: absolute;
            top: 15px;
            right: 20px;
            cursor: pointer;
            color: #94A3B8;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .masonry {
                column-count: 2;
                column-gap: 12px;
            }
            .header h1 {
                font-size: 1.6rem;
            }
        }
        @media (max-width: 480px) {
            .masonry {
                column-count: 2;
                column-gap: 8px;
            }
            .filter-btn {
                padding: 6px 14px;
                font-size: 0.8rem;
            }
            .pin-footer {
                flex-wrap: wrap;
                gap: 8px;
            }
            .subtotal-display {
                font-size: 0.85rem;
                margin-right: 0;
                width: 100%;
                text-align: center;
            }
            .quantity-control {
                flex: 1;
                justify-content: center;
            }
            .btn-pedir {
                flex: 1;
                text-align: center;
            }
        }
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

    <!-- Modal -->
    <div class="modal-overlay" id="modalOverlay">
        <div class="modal-content" id="modalContent">
            <button class="btn-close-modal" id="closeModalBtn">✕</button>
            <h2 id="modalTitle">Pedido</h2>
            <div class="modal-resumen" id="modalResumen"></div>
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
                    <button data-method="yape">Yape</button>
                    <button data-method="plin">Plin</button>
                    <button data-method="transferencia">Transferencia</button>
                    <button data-method="efectivo">Efectivo</button>
                </div>
            </div>
            <div class="form-group">
                <label>Adjuntar Captura de Pago</label>
                <div class="file-upload" id="fileUploadBox">
                    <p>Haz clic para subir o arrastra tu captura</p>
                    <input type="file" id="fileInput" accept="image/*">
                </div>
                <span id="fileNombre" style="font-size:0.9rem; color:#22A39F; display:block; margin-top:5px;"></span>
            </div>
            <button class="btn-submit" id="submitPedidoBtn">Confirmar Pedido</button>
        </div>
    </div>

    <script>
        // Datos de productos
        const productos = [
            { id: 1, nombre: "Mariposa Monarca", categoria: "animales", precio: 5.00, imagen: "https://picsum.photos/seed/mariposa/300/450", personalizable: false },
            { id: 2, nombre: "Ramo Floral", categoria: "floral", precio: 6.50, imagen: "https://picsum.photos/seed/ramo/300/320", personalizable: false },
            { id: 3, nombre: "Iniciales", categoria: "letras", precio: 4.00, imagen: "https://picsum.photos/seed/inicial/300/500", personalizable: true },
            { id: 4, nombre: "Águila Real", categoria: "animales", precio: 8.00, imagen: "https://picsum.photos/seed/aguila/300/380", personalizable: false },
            { id: 5, nombre: "Mandala", categoria: "geometrico", precio: 7.00, imagen: "https://picsum.photos/seed/mandala/300/350", personalizable: false },
            { id: 6, nombre: "Nombre Propio", categoria: "nombres", precio: 4.00, imagen: "https://picsum.photos/seed/nombre/300/480", personalizable: true }
        ];

        // Estado de cantidades
        let cantidades = {};
        productos.forEach(p => cantidades[p.id] = 0);

        // Referencias DOM
        const masonry = document.getElementById('masonry');
        const modalOverlay = document.getElementById('modalOverlay');
        const modalTitle = document.getElementById('modalTitle');
        const modalResumen = document.getElementById('modalResumen');
        const closeModalBtn = document.getElementById('closeModalBtn');
        const submitBtn = document.getElementById('submitPedidoBtn');
        const clienteNombre = document.getElementById('clienteNombre');
        const clienteTipo = document.getElementById('clienteTipo');
        const fileInput = document.getElementById('fileInput');
        const fileNombre = document.getElementById('fileNombre');
        const paymentOptions = document.getElementById('paymentOptions');
        let currentProductId = null;

        // Renderizar muro
        function renderProductos(filtro = 'all') {
            masonry.innerHTML = '';
            const filtrados = filtro === 'all' ? productos : productos.filter(p => p.categoria === filtro);

            filtrados.forEach(prod => {
                const cant = cantidades[prod.id] || 0;
                const subtotal = (prod.precio * cant).toFixed(2);

                const pin = document.createElement('div');
                pin.className = 'pin';
                pin.innerHTML = `
                    <div class="pin-image-wrapper">
                        <img src="${prod.imagen}" alt="${prod.nombre}" loading="lazy">
                        ${prod.personalizable ? `<span class="badge-personalizable">Personalizable</span>` : ''}
                        <div class="pin-overlay">
                            <span class="pin-nombre">${prod.nombre}</span>
                            <span class="pin-precio">$${prod.precio.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="pin-footer">
                        <div>
                            ${cant > 0 ? `<span class="subtotal-display">Subtotal: $${subtotal}</span>` : ''}
                        </div>
                        <div style="display:flex; align-items:center; gap:10px;">
                            <div class="quantity-control" data-id="${prod.id}">
                                <button class="qty-minus" data-id="${prod.id}">−</button>
                                <span class="qty-number" id="qty-${prod.id}">${cant}</span>
                                <button class="qty-plus" data-id="${prod.id}">+</button>
                            </div>
                            <button class="btn-pedir" data-id="${prod.id}">Pedir</button>
                        </div>
                    </div>
                `;
                masonry.appendChild(pin);
            });

            // Eventos
            document.querySelectorAll('.qty-plus').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    cantidades[id] = (cantidades[id] || 0) + 1;
                    actualizarUI(id);
                });
            });
            document.querySelectorAll('.qty-minus').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    if (cantidades[id] > 0) {
                        cantidades[id]--;
                        actualizarUI(id);
                    }
                });
            });
            document.querySelectorAll('.btn-pedir').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    abrirModal(id);
                });
            });
        }

        // Actualizar UI de una tarjeta
        function actualizarUI(id) {
            const qtySpan = document.getElementById(`qty-${id}`);
            if (qtySpan) qtySpan.textContent = cantidades[id] || 0;

            const pin = qtySpan?.closest('.pin');
            if (pin) {
                const footer = pin.querySelector('.pin-footer');
                const subtotalSpan = footer.querySelector('.subtotal-display');
                const prod = productos.find(p => p.id === id);
                const subtotal = (prod.precio * (cantidades[id] || 0)).toFixed(2);
                if (cantidades[id] > 0) {
                    if (!subtotalSpan) {
                        const newSub = document.createElement('span');
                        newSub.className = 'subtotal-display';
                        newSub.textContent = `Subtotal: $${subtotal}`;
                        footer.querySelector('div:first-child').appendChild(newSub);
                    } else {
                        subtotalSpan.textContent = `Subtotal: $${subtotal}`;
                    }
                } else {
                    if (subtotalSpan) subtotalSpan.remove();
                }
            }
        }

        // Abrir modal
        function abrirModal(id) {
            currentProductId = id;
            const prod = productos.find(p => p.id === id);
            const cant = cantidades[id] || 0;
            if (cant === 0) {
                alert('Primero selecciona una cantidad con el botón +.');
                return;
            }
            const subtotal = (prod.precio * cant).toFixed(2);

            modalTitle.textContent = `Pedido: ${prod.nombre}`;
            modalResumen.innerHTML = `
                <div class="modal-resumen-item"><span>Diseño</span><span><strong>${prod.nombre}</strong></span></div>
                <div class="modal-resumen-item"><span>Cantidad</span><span>${cant}</span></div>
                <div class="modal-resumen-item"><span>Precio Unitario</span><span>$${prod.precio.toFixed(2)}</span></div>
                <div class="modal-total"><span>Subtotal</span><span>$${subtotal}</span></div>
            `;

            // Resetear campos
            clienteNombre.value = '';
            clienteTipo.value = 'natural';
            document.querySelectorAll('.payment-options button').forEach(b => b.classList.remove('selected'));
            fileInput.value = '';
            fileNombre.textContent = '';

            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden'; // Evita scroll del body cuando el modal está abierto
        }

        function cerrarModal() {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = ''; // Restaura scroll del body
            currentProductId = null;
        }

        closeModalBtn.addEventListener('click', cerrarModal);
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) cerrarModal();
        });

        // Métodos de pago
        paymentOptions.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', function() {
                paymentOptions.querySelectorAll('button').forEach(b => b.classList.remove('selected'));
                this.classList.add('selected');
            });
        });

        // Subida de archivo
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileNombre.textContent = `Archivo: ${this.files[0].name}`;
            }
        });
        document.getElementById('fileUploadBox').addEventListener('click', () => fileInput.click());

        // Enviar pedido
        submitBtn.addEventListener('click', () => {
            if (currentProductId === null) return;
            const prod = productos.find(p => p.id === currentProductId);
            const cant = cantidades[currentProductId] || 0;
            const subtotal = (prod.precio * cant).toFixed(2);

            const nombre = clienteNombre.value.trim();
            if (!nombre) {
                alert('Por favor, ingresa tu nombre y apellido.');
                return;
            }
            const tipo = clienteTipo.value === 'natural' ? 'Persona Natural' : 'Empresa';
            const metodoSeleccionado = paymentOptions.querySelector('button.selected');
            const metodo = metodoSeleccionado ? metodoSeleccionado.textContent.trim() : 'No seleccionado';
            const archivo = fileInput.files[0];

            let resumen = `PEDIDO CONFIRMADO\n`;
            resumen += `Cliente: ${nombre}\n`;
            resumen += `Tipo: ${tipo}\n`;
            resumen += `Pago: ${metodo}\n`;
            resumen += `Archivo: ${archivo ? archivo.name : 'No se adjuntó'}\n`;
            resumen += `───────────────────\n`;
            resumen += `Diseño: ${prod.nombre}\n`;
            resumen += `Cantidad: ${cant}\n`;
            resumen += `Subtotal: $${subtotal}\n`;

            alert(resumen);
            cerrarModal();
        });

        // Filtros
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                renderProductos(this.dataset.category);
            });
        });

        // Inicializar
        renderProductos('all');
    </script>
</body>
</html>
"""

st.set_page_config(page_title="Catálogo de Bordados", layout="wide")
# Eliminamos la altura fija para que el componente ocupe todo el espacio disponible
st.components.v1.html(HTML_CODE, height=None, scrolling=False)
