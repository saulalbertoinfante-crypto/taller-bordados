<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo de Bordados - Muro de Inspiración</title>
  <style>
    /* VARIABLES Y PALETA DE COLORES */
    :root {
      --primary: #1A5F7A;
      --secondary: #22A39F;
      --bg-light: #F8FAFC;
      --text-dark: #0F172A;
      --text-muted: #64748B;
      --border-color: #CBD5E1;
      --shadow-sm: 0 4px 15px rgba(0, 0, 0, 0.06);
      --shadow-lg: 0 20px 30px -10px rgba(0, 0, 0, 0.22);
      --success: #10B981;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: var(--bg-light);
      color: var(--text-dark);
      padding: 20px 15px 100px 15px;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* HEADER */
    header {
      text-align: center;
      margin-bottom: 25px;
    }

    header h1 {
      font-size: 2.2rem;
      color: var(--primary);
      font-weight: 800;
    }

    header p {
      font-size: 1rem;
      color: var(--text-muted);
      margin-top: 5px;
    }

    /* FILTROS EN PÍLDORAS */
    .filter-bar {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 30px;
    }

    .chip-btn {
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 8px 22px;
      border-radius: 50px;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.25s ease;
      outline: none;
    }

    .chip-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    .chip-btn.active {
      background-color: var(--primary);
      border-color: var(--primary);
      color: #FFFFFF;
      box-shadow: 0 4px 12px rgba(26, 95, 122, 0.3);
    }

    /* PILAR 1: MURO MASONRY PINTEREST */
    .masonry-wall {
      column-count: 3;
      column-gap: 20px;
    }

    @media (max-width: 768px) {
      .masonry-wall {
        column-count: 2;
        column-gap: 15px;
      }
    }

    @media (max-width: 480px) {
      .masonry-wall {
        column-count: 1;
      }
    }

    /* LA TARJETA Y EFECTO HOVER */
    .card {
      position: relative;
      margin-bottom: 20px;
      border-radius: 16px;
      overflow: hidden;
      background-color: #FFFFFF;
      box-shadow: var(--shadow-sm);
      break-inside: avoid;
      -webkit-column-break-inside: avoid;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card:hover {
      box-shadow: var(--shadow-lg);
    }

    .card-img-wrapper {
      position: relative;
      width: 100%;
      overflow: hidden;
      display: block;
    }

    .card-img-wrapper img {
      width: 100%;
      height: auto;
      display: block;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card:hover .card-img-wrapper img {
      transform: scale(1.03);
    }

    /* BADGE PERSONALIZABLE */
    .badge-custom {
      position: absolute;
      top: 12px;
      left: 12px;
      background-color: var(--secondary);
      color: #FFFFFF;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      z-index: 2;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    /* OVERLAY Y TEXTO DEGRADADO */
    .card-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 50px 16px 16px 16px;
      background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      z-index: 1;
      pointer-events: none;
    }

    .card-info {
      color: #FFFFFF;
    }

    .card-title {
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 2px;
      text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    .card-price {
      font-size: 0.9rem;
      font-weight: 400;
      opacity: 0.9;
    }

    /* SELECTOR DE CANTIDAD FLOTANTE */
    .qty-controls {
      pointer-events: auto;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border-radius: 30px;
      display: flex;
      align-items: center;
      padding: 4px;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .btn-qty {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.2s, color 0.2s;
    }

    .btn-minus {
      background: #E2E8F0;
      color: var(--text-dark);
    }

    .btn-minus:hover {
      background: #CBD5E1;
    }

    .btn-plus {
      background-color: var(--primary);
      color: #FFFFFF;
    }

    .btn-plus:hover {
      background-color: #124357;
    }

    .qty-val {
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--text-dark);
      min-width: 16px;
      text-align: center;
    }

    /* BOTÓN BARRA FLOTANTE CHECKOUT */
    .checkout-floating-bar {
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 100;
      width: 90%;
      max-width: 500px;
    }

    .btn-checkout-trigger {
      width: 100%;
      background-color: var(--primary);
      color: #FFFFFF;
      border: none;
      padding: 16px 24px;
      border-radius: 50px;
      font-size: 1.1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 10px 25px rgba(26, 95, 122, 0.4);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: transform 0.2s, background-color 0.2s;
    }

    .btn-checkout-trigger:hover {
      background-color: #124357;
      transform: scale(1.02);
    }

    .cart-badge-count {
      background-color: var(--secondary);
      color: #FFFFFF;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.9rem;
    }

    /* PILAR 3: MODAL DE CHECKOUT */
    .modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 15px;
    }

    .modal-backdrop.active {
      display: flex;
    }

    .modal-content {
      background: #FFFFFF;
      width: 100%;
      max-width: 600px;
      max-height: 90vh;
      border-radius: 24px;
      overflow-y: auto;
      padding: 25px;
      box-shadow: var(--shadow-lg);
      position: relative;
      animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalSlideUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 12px;
    }

    .modal-header h2 {
      font-size: 1.4rem;
      color: var(--primary);
    }

    .btn-close-modal {
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      color: var(--text-muted);
    }

    /* RESUMEN DE COMPRA EN TABLA */
    .order-summary-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }

    .order-summary-table th, .order-summary-table td {
      padding: 10px 8px;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
      font-size: 0.9rem;
    }

    .order-summary-table th {
      color: var(--text-muted);
      font-weight: 600;
    }

    .total-row {
      font-size: 1.1rem !important;
      font-weight: 800;
      color: var(--primary);
    }

    /* FORMULARIO DE CLIENTE */
    .form-group {
      margin-bottom: 16px;
    }

    .form-group label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 6px;
      color: var(--text-dark);
    }

    .form-control {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      font-size: 0.95rem;
      outline: none;
    }

    .form-control:focus {
      border-color: var(--primary);
    }

    /* OPCIONES DE PAGO EN BOTONES CIRCULARES/PÍLDORAS */
    .payment-options {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 6px;
    }

    .payment-btn {
      flex: 1;
      min-width: 100px;
      padding: 10px;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      background: #FFFFFF;
      text-align: center;
      cursor: pointer;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-muted);
      transition: all 0.2s;
    }

    .payment-btn.selected {
      border-color: var(--primary);
      border-width: 2px;
      color: var(--primary);
      background: rgba(26, 95, 122, 0.05);
    }

    /* AREA DRAG & DROP FILE UPLOAD */
    .file-drop-area {
      border: 2px dashed var(--border-color);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      cursor: pointer;
      background: var(--bg-light);
      transition: border-color 0.2s;
    }

    .file-drop-area:hover {
      border-color: var(--primary);
    }

    .file-drop-area input[type="file"] {
      display: none;
    }

    .btn-submit-order {
      width: 100%;
      background-color: var(--success);
      color: #FFFFFF;
      border: none;
      padding: 14px;
      border-radius: 12px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      margin-top: 15px;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
      transition: background-color 0.2s;
    }

    .btn-submit-order:hover {
      background-color: #059669;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <h1>Catálogo de Bordados</h1>
      <p>Explora nuestros diseños y personaliza tu pedido</p>
    </header>

    <!-- Filtros por Categoría -->
    <div class="filter-bar" id="filterBar">
      <button class="chip-btn active" data-category="todas">Todas</button>
      <button class="chip-btn" data-category="animales">Animales</button>
      <button class="chip-btn" data-category="floral">Floral</button>
      <button class="chip-btn" data-category="letras">Letras</button>
      <button class="chip-btn" data-category="geometrico">Geométrico</button>
      <button class="chip-btn" data-category="nombres">Nombres</button>
    </div>

    <!-- Muro Masonry -->
    <div class="masonry-wall" id="masonryWall"></div>
  </div>

  <!-- Botón Flotante para Abrir Checkout -->
  <div class="checkout-floating-bar">
    <button class="btn-checkout-trigger" onclick="openCheckoutModal()">
      <span>🛒 Ver Pedido y Finalizar</span>
      <span class="cart-badge-count" id="cartTotalDisplay">$0.00</span>
    </button>
  </div>

  <!-- Modal de Checkout -->
  <div class="modal-backdrop" id="checkoutModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Resumen de tu Pedido</h2>
        <button class="btn-close-modal" onclick="closeCheckoutModal()">&times;</button>
      </div>

      <!-- Tabla del Carrito -->
      <table class="order-summary-table">
        <thead>
          <tr>
            <th>Diseño</th>
            <th>Cant.</th>
            <th>P. Unit.</th>
            <th>Subtotal</th>
          </tr>
        </thead>
        <tbody id="cartTableBody">
          <!-- Inyectado dinámicamente -->
        </tbody>
      </table>

      <!-- Formulario del Cliente -->
      <form id="checkoutForm" onsubmit="handleFormSubmit(event)">
        <div class="form-group">
          <label for="clientName">Nombre y Apellido</label>
          <input type="text" id="clientName" class="form-control" placeholder="Ej: Maria Perez" required>
        </div>

        <div class="form-group">
          <label for="personType">Tipo de Persona</label>
          <select id="personType" class="form-control" required>
            <option value="Persona Natural">Persona Natural</option>
            <option value="Empresa">Empresa</option>
          </select>
        </div>

        <!-- Método de Pago -->
        <div class="form-group">
          <label>Método de Pago</label>
          <div class="payment-options">
            <div class="payment-btn selected" onclick="selectPayment(this, 'Yape')">Yape</div>
            <div class="payment-btn" onclick="selectPayment(this, 'Plin')">Plin</div>
            <div class="payment-btn" onclick="selectPayment(this, 'Transferencia')">Transferencia</div>
            <div class="payment-btn" onclick="selectPayment(this, 'Efectivo')">Efectivo</div>
          </div>
        </div>

        <!-- Adjuntar Comprobante -->
        <div class="form-group">
          <label>Adjuntar Comprobante de Pago</label>
          <div class="file-drop-area" onclick="document.getElementById('fileInput').click()">
            <span id="fileNameDisplay">📁 Haz clic o arrastra tu captura de pantalla aquí</span>
            <input type="file" id="fileInput" accept="image/*" onchange="updateFileName(this)">
          </div>
        </div>

        <button type="submit" class="btn-submit-order">Enviar Pedido Formal</button>
      </form>
    </div>
  </div>

  <script>
    // DATOS EXACTOS
    const productos = [
      { id: 1, nombre: "Mariposa Monarca", categoria: "animales", precio: 5.00, imagen: "https://picsum.photos/seed/mariposa/300/450", personalizable: false },
      { id: 2, nombre: "Ramo Floral", categoria: "floral", precio: 6.50, imagen: "https://picsum.photos/seed/ramo/300/300", personalizable: false },
      { id: 3, nombre: "Iniciales", categoria: "letras", precio: 4.00, imagen: "https://picsum.photos/seed/inicial/300/500", personalizable: true },
      { id: 4, nombre: "Águila Real", categoria: "animales", precio: 8.00, imagen: "https://picsum.photos/seed/aguila/300/380", personalizable: false },
      { id: 5, nombre: "Mandala", categoria: "geometrico", precio: 7.00, imagen: "https://picsum.photos/seed/mandala/300/350", personalizable: false },
      { id: 6, nombre: "Nombre Propio", categoria: "nombres", precio: 4.00, imagen: "https://picsum.photos/seed/nombre/300/480", personalizable: true }
    ];

    // ESTADO DEL CARRITO (id -> cantidad)
    const carrito = {};
    productos.forEach(p => carrito[p.id] = 0);

    let selectedPaymentMethod = "Yape";

    const wall = document.getElementById("masonryWall");
    const filterBar = document.getElementById("filterBar");

    // PILAR 1: RENDERIZAR TARJETAS VISUALES
    function renderProducts(category = "todas") {
      wall.innerHTML = "";
      
      const filtered = category === "todas" 
        ? productos 
        : productos.filter(p => p.categoria.toLowerCase() === category.toLowerCase());

      filtered.forEach(p => {
        const card = document.createElement("div");
        card.className = "card";

        const badgeHtml = p.personalizable 
          ? `<div class="badge-custom">✏️ Personalizable</div>` 
          : "";

        card.innerHTML = `
          <div class="card-img-wrapper">
            ${badgeHtml}
            <img src="${p.imagen}" alt="${p.nombre}" loading="lazy">
            <div class="card-overlay">
              <div class="card-info">
                <div class="card-title">${p.nombre}</div>
                <div class="card-price">$${p.precio.toFixed(2)}</div>
              </div>
              <div class="qty-controls">
                <button class="btn-qty btn-minus" onclick="changeQty(${p.id}, -1)">−</button>
                <span class="qty-val" id="qty-${p.id}">${carrito[p.id]}</span>
                <button class="btn-qty btn-plus" onclick="changeQty(${p.id}, 1)">+</button>
              </div>
            </div>
          </div>
        `;
        wall.appendChild(card);
      });
    }

    // PILAR 2: LÓGICA DEL CARRITO Y MULTIPLICACIÓN
    function changeQty(id, delta) {
      const current = carrito[id] || 0;
      const next = Math.max(0, current + delta);
      
      carrito[id] = next;

      // Actualizar DOM individual
      const qtyElem = document.getElementById(`qty-${id}`);
      if (qtyElem) qtyElem.textContent = next;

      calculateTotal();
    }

    function calculateTotal() {
      let total = 0;
      productos.forEach(p => {
        total += (carrito[p.id] || 0) * p.precio;
      });

      document.getElementById("cartTotalDisplay").textContent = `$${total.toFixed(2)}`;
      return total;
    }

    // PILAR 3: MANEJO DEL MODAL Y RESUMEN
    function openCheckoutModal() {
      const tableBody = document.getElementById("cartTableBody");
      tableBody.innerHTML = "";

      let grandTotal = 0;
      let hasItems = false;

      productos.forEach(p => {
        const qty = carrito[p.id] || 0;
        if (qty > 0) {
          hasItems = true;
          const subtotal = qty * p.precio;
          grandTotal += subtotal;

          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${p.nombre}</td>
            <td>${qty}</td>
            <td>$${p.precio.toFixed(2)}</td>
            <td>$${subtotal.toFixed(2)}</td>
          `;
          tableBody.appendChild(row);
        }
      });

      if (!hasItems) {
        tableBody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: var(--text-muted);">No has seleccionado ningún producto aún.</td></tr>`;
      } else {
        const totalRow = document.createElement("tr");
        totalRow.className = "total-row";
        totalRow.innerHTML = `
          <td colspan="3">TOTAL GENERAL</td>
          <td>$${grandTotal.toFixed(2)}</td>
        `;
        tableBody.appendChild(totalRow);
      }

      document.getElementById("checkoutModal").classList.add("active");
    }

    function closeCheckoutModal() {
      document.getElementById("checkoutModal").classList.remove("active");
    }

    function selectPayment(element, method) {
      document.querySelectorAll(".payment-btn").forEach(btn => btn.classList.remove("selected"));
      element.classList.add("selected");
      selectedPaymentMethod = method;
    }

    function updateFileName(input) {
      const display = document.getElementById("fileNameDisplay");
      if (input.files && input.files[0]) {
        display.textContent = `📄 ${input.files[0].name}`;
      }
    }

    function handleFormSubmit(event) {
      event.preventDefault();

      const name = document.getElementById("clientName").value;
      const type = document.getElementById("personType").value;
      const fileInput = document.getElementById("fileInput");
      const fileName = fileInput.files[0] ? fileInput.files[0].name : "Ninguno";
      const total = calculateTotal();

      if (total === 0) {
        alert("Por favor, agrega al menos un producto a tu pedido antes de continuar.");
        return;
      }

      alert(`✅ ¡PEDIDO ENVIADO CON ÉXITO!\n\n` +
            `Cliente: ${name}\n` +
            `Tipo: ${type}\n` +
            `Método de Pago: ${selectedPaymentMethod}\n` +
            `Comprobante: ${fileName}\n` +
            `Total a Pagar: $${total.toFixed(2)}`);

      closeCheckoutModal();
    }

    // EVENTOS DE FILTRADO
    filterBar.addEventListener("click", (e) => {
      if (e.target.classList.contains("chip-btn")) {
        document.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        renderProducts(e.target.dataset.category);
      }
    });

    // INICIALIZACIÓN
    renderProducts("todas");
  </script>
</body>
</html>
