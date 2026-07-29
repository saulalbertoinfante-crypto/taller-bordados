import streamlit as st
import streamlit.components.v1 as components

# Configuración de página ancha en Streamlit
st.set_page_config(
    page_title="Catálogo de Diseños",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Renderizado de la App Visual en HTML/CSS/JS
components.html(
    """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo de Diseños</title>
  <style>
    /* VARIABLES Y PALETA DE COLORES AZULES */
    :root {
      --primary: #1A5F7A;
      --secondary: #22A39F;
      --bg-light: #F8FAFC;
      --text-dark: #0F172A;
      --text-muted: #64748B;
      --border-color: #CBD5E1;
      --shadow-sm: 0 4px 15px rgba(0, 0, 0, 0.06);
      --shadow-lg: 0 20px 30px -10px rgba(0, 0, 0, 0.22);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-light);
      color: var(--text-dark);
      padding: 20px 15px;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* 1. HEADER */
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

    /* 2. FILTROS EN PÍLDORAS */
    .filter-bar {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 35px;
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

    /* 3. MURO MASONRY PINTEREST */
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

    /* 4 & 6. LA TARJETA Y EFECTO HOVER */
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
      background: rgba(255, 255, 255, 0.9);
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
      background: transparent;
      color: var(--text-dark);
    }

    .btn-minus:hover {
      background: rgba(0, 0, 0, 0.1);
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

    /* 5. MENSAJE TOAST EMERGENTE */
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
      padding: 14px 22px;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 500;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
      animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes slideUp {
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
      <h1>Catálogo de Diseños</h1>
      <p>Explora y agrega a tu cotización</p>
    </header>

    <!-- Filtros Píldora -->
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

  <div class="toast-container" id="toastContainer"></div>

  <script>
    const productos = [
      { id: 1, nombre: "Mariposa Monarca", categoria: "animales", precio: 5.00, imagen: "https://picsum.photos/seed/mariposa/300/400", personalizable: false },
      { id: 2, nombre: "Ramo Floral", categoria: "floral", precio: 6.50, imagen: "https://picsum.photos/seed/ramo/300/350", personalizable: false },
      { id: 3, nombre: "Iniciales", categoria: "letras", precio: 4.00, imagen: "https://picsum.photos/seed/inicial/300/450", personalizable: true },
      { id: 4, nombre: "Águila Real", categoria: "animales", precio: 8.00, imagen: "https://picsum.photos/seed/aguila/300/380", personalizable: false },
      { id: 5, nombre: "Mandala", categoria: "geometrico", precio: 7.00, imagen: "https://picsum.photos/seed/mandala/300/320", personalizable: false },
      { id: 6, nombre: "Nombre Propio", categoria: "nombres", precio: 4.00, imagen: "https://picsum.photos/seed/nombre/300/480", personalizable: true }
    ];

    const carrito = {};
    productos.forEach(item => { carrito[item.id] = 0; });

    const wall = document.getElementById("masonryWall");
    const filterBar = document.getElementById("filterBar");
    const toastContainer = document.getElementById("toastContainer");

    function renderProducts(cat = "todas") {
      wall.innerHTML = "";
      
      const filtered = cat === "todas" 
        ? productos 
        : productos.filter(p => p.categoria.toLowerCase() === cat.toLowerCase());

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

    function changeQty(id, delta) {
      const prod = productos.find(p => p.id === id);
      if (!prod) return;

      const current = carrito[id] || 0;
      const next = Math.max(0, current + delta);

      if (current !== next) {
        carrito[id] = next;
        const elem = document.getElementById(`qty-${id}`);
        if (elem) elem.textContent = next;

        if (delta > 0) {
          triggerToast(`Agregaste ${prod.nombre}`);
        }
      }
    }

    function triggerToast(text) {
      const toast = document.createElement("div");
      toast.className = "toast";
      toast.textContent = text;

      toastContainer.appendChild(toast);

      setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
      }, 2000);
    }

    filterBar.addEventListener("click", (e) => {
      if (e.target.classList.contains("chip-btn")) {
        document.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        renderProducts(e.target.dataset.category);
      }
    });

    renderProducts("todas");
  </script>
</body>
</html>
""",
    height=1300,
    scrolling=True
)
