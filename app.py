import streamlit as st
import streamlit.components.v1 as components

# Configuración básica de la página en Streamlit
st.set_page_config(
    page_title="Muro de Inspiración",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Renderizar el HTML/CSS/JS dentro de Streamlit
components.html(
    """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Muro de Inspiración - Catálogo de Bordados</title>
  <style>
    /* RESET Y VARIABLES DE MARCA */
    :root {
      --primary: #1A5F7A;
      --secondary: #22A39F;
      --bg-light: #F8FAFC;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --border-light: #CBD5E1;
      --shadow-card: 0 4px 15px rgba(0, 0, 0, 0.05);
      --shadow-hover: 0 20px 30px -10px rgba(0, 0, 0, 0.2);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: var(--bg-light);
      color: var(--text-main);
      padding: 20px 10px;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* HEADER */
    header {
      margin-bottom: 25px;
      text-align: center;
    }

    header h1 {
      font-size: 2.2rem;
      color: var(--primary);
      font-weight: 700;
      letter-spacing: -0.5px;
    }

    /* 1. FILTROS EN PÍLDORAS (CHIPS) */
    .filter-container {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 30px;
    }

    .chip-btn {
      background: transparent;
      border: 1px solid var(--border-light);
      color: var(--text-muted);
      padding: 8px 20px;
      border-radius: 30px;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
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
      box-shadow: 0 4px 10px rgba(26, 95, 122, 0.25);
    }

    /* 2. LAYOUT MASONRY PINTEREST */
    .masonry-grid {
      column-count: 3;
      column-gap: 20px;
    }

    @media (max-width: 768px) {
      .masonry-grid {
        column-count: 2;
        column-gap: 15px;
      }
    }

    @media (max-width: 480px) {
      .masonry-grid {
        column-count: 1;
      }
    }

    /* 3 & 5. TARJETA, OVERLAY Y HOVER EFFECT */
    .card {
      position: relative;
      margin-bottom: 20px;
      border-radius: 16px;
      overflow: hidden;
      background-color: #FFFFFF;
      box-shadow: var(--shadow-card);
      break-inside: avoid;
      -webkit-column-break-inside: avoid;
      transition: box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1), transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card:hover {
      box-shadow: var(--shadow-hover);
    }

    .card-image-wrapper {
      position: relative;
      width: 100%;
      overflow: hidden;
      display: block;
    }

    .card-image-wrapper img {
      width: 100%;
      height: auto;
      display: block;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card:hover .card-image-wrapper img {
      transform: scale(1.03);
    }

    /* 6. BADGE PERSONALIZABLE */
    .badge-custom {
      position: absolute;
      top: 12px;
      left: 12px;
      background-color: var(--secondary);
      color: #FFFFFF;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 4px;
      z-index: 2;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    /* DEGRADADO Y DATOS DE LA TARJETA */
    .card-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 40px 16px 16px 16px;
      background: linear-gradient(transparent, rgba(0, 0, 0, 0.75));
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
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 2px;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    }

    .card-price {
      font-size: 0.9rem;
      font-weight: 400;
      opacity: 0.9;
    }

    /* 3. CONTROLADOR DE CANTIDAD FLOTANTE */
    .quantity-control {
      pointer-events: auto;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border-radius: 30px;
      display: flex;
      align-items: center;
      padding: 3px;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .btn-qty {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.2s, color 0.2s;
    }

    .btn-minus {
      background: transparent;
      color: var(--text-main);
    }

    .btn-minus:hover {
      background: rgba(0, 0, 0, 0.08);
    }

    .btn-plus {
      background-color: var(--primary);
      color: #FFFFFF;
    }

    .btn-plus:hover {
      background-color: #14495e;
    }

    .qty-display {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-main);
      min-width: 14px;
      text-align: center;
    }

    /* 4. TOAST NOTIFICACIÓN */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .toast {
      background-color: var(--primary);
      color: #FFFFFF;
      padding: 12px 20px;
      border-radius: 10px;
      font-size: 0.9rem;
      font-weight: 500;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
      animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <h1>Un muro de inspiración</h1>
    </header>

    <!-- Píldoras de Filtros -->
    <div class="filter-container" id="filterContainer">
      <button class="chip-btn active" data-category="todas">Todas</button>
      <button class="chip-btn" data-category="animales">Animales</button>
      <button class="chip-btn" data-category="floral">Floral</button>
      <button class="chip-btn" data-category="letras">Letras</button>
      <button class="chip-btn" data-category="geometrico">Geométrico</button>
      <button class="chip-btn" data-category="nombres">Nombres</button>
    </div>

    <!-- Muro Masonry -->
    <div class="masonry-grid" id="masonryGrid"></div>
  </div>

  <div class="toast-container" id="toastContainer"></div>

  <script>
    const designs = [
      { id: 1, name: "Mariposa Monarca", category: "animales", price: 5.00, image: "https://via.placeholder.com/300x400/1A5F7A/FFFFFF?text=Mariposa", personalizable: false },
      { id: 2, name: "Ramo Floral", category: "floral", price: 6.50, image: "https://via.placeholder.com/300x300/22A39F/FFFFFF?text=Ramo", personalizable: false },
      { id: 3, name: "Iniciales", category: "letras", price: 4.00, image: "https://via.placeholder.com/300x500/AEE2FF/1A5F7A?text=Iniciales", personalizable: true },
      { id: 4, name: "Águila Real", category: "animales", price: 8.00, image: "https://via.placeholder.com/300x350/1A5F7A/FFFFFF?text=Águila", personalizable: false },
      { id: 5, name: "Mandala Geométrico", category: "geometrico", price: 7.00, image: "https://via.placeholder.com/300x250/22A39F/FFFFFF?text=Mandala", personalizable: false },
      { id: 6, name: "Nombre Personalizado", category: "nombres", price: 4.00, image: "https://via.placeholder.com/300x450/AEE2FF/1A5F7A?text=Nombre", personalizable: true }
    ];

    const quantities = {};
    designs.forEach(item => { quantities[item.id] = 0; });

    const masonryGrid = document.getElementById("masonryGrid");
    const filterContainer = document.getElementById("filterContainer");
    const toastContainer = document.getElementById("toastContainer");

    function renderCards(category = "todas") {
      masonryGrid.innerHTML = "";
      
      const filtered = category === "todas" 
        ? designs 
        : designs.filter(d => d.category.toLowerCase() === category.toLowerCase());

      filtered.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";

        const badgeHtml = item.personalizable 
          ? `<div class="badge-custom"><span>✏️</span> Personalizable</div>` 
          : "";

        card.innerHTML = `
          <div class="card-image-wrapper">
            ${badgeHtml}
            <img src="${item.image}" alt="${item.name}" loading="lazy">
            <div class="card-overlay">
              <div class="card-info">
                <div class="card-title">${item.name}</div>
                <div class="card-price">$${item.price.toFixed(2)}</div>
              </div>
              <div class="quantity-control">
                <button class="btn-qty btn-minus" onclick="updateQuantity(${item.id}, -1)">−</button>
                <span class="qty-display" id="qty-${item.id}">${quantities[item.id]}</span>
                <button class="btn-qty btn-plus" onclick="updateQuantity(${item.id}, 1)">+</button>
              </div>
            </div>
          </div>
        `;
        masonryGrid.appendChild(card);
      });
    }

    function updateQuantity(id, change) {
      const item = designs.find(d => d.id === id);
      if (!item) return;

      const currentQty = quantities[id] || 0;
      const newQty = Math.max(0, currentQty + change);

      if (currentQty !== newQty) {
        quantities[id] = newQty;
        const qtyElement = document.getElementById(`qty-${id}`);
        if (qtyElement) {
          qtyElement.textContent = newQty;
        }

        if (change > 0) {
          const totalAcumulado = (newQty * item.price).toFixed(2);
          showToast(`🧵 ${item.name} agregado. Total acumulado: $${totalAcumulado}`);
        }
      }
    }

    function showToast(message) {
      const toast = document.createElement("div");
      toast.className = "toast";
      toast.textContent = message;

      toastContainer.appendChild(toast);

      setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
      }, 2000);
    }

    filterContainer.addEventListener("click", (e) => {
      if (e.target.classList.contains("chip-btn")) {
        document.querySelectorAll(".chip-btn").forEach(btn => btn.classList.remove("active"));
        e.target.classList.add("active");
        renderCards(e.target.dataset.category);
      }
    });

    renderCards("todas");
  </script>
</body>
</html>
""",
    height=1200,
    scrolling=True
)
