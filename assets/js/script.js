document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ Dashboard financiero cargado");

  // ==========================================================
  // 🔹 SISTEMA DE PREDICCIÓN
  // ==========================================================
const btnPredecir = document.getElementById("btnPredecir");
const resultado = document.getElementById("resultadoPrediccion");

if (btnPredecir) {
  btnPredecir.addEventListener("click", async () => {
    const tasa = document.getElementById("tasa").value.trim();
    const fecha = document.getElementById("fecha").value.trim();
    const tasa_interes = document.getElementById("tasa_interes").value.trim();
    const pib = document.getElementById("pib").value.trim();
    const petroleo = document.getElementById("petroleo").value.trim();

    if (!tasa) {
      resultado.innerHTML = `<div class="prediction-error"><i class="fas fa-exclamation-circle"></i> La tasa de inflación es obligatoria.</div>`;
      return;
    }

    resultado.innerHTML = `<div class="prediction-loading"><i class="fas fa-spinner fa-spin"></i> Calculando predicción...</div>`;

    try {
      const response = await fetch("/predecir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tasa_inflacion: tasa,
          fecha_str: fecha || "",
          tasa_interes_input: tasa_interes || null,
          pib_input: pib || null,
          petroleo_input: petroleo || null
        })
      });

      const data = await response.json();

      if (data.error) {
        resultado.innerHTML = `<div class="prediction-error"><i class="fas fa-times-circle"></i> ${data.error}</div>`;
        return;
      }

      resultado.innerHTML = `
        <div class="prediction-result">
          <h3><i class="fas fa-dollar-sign"></i> Resultado de Predicción</h3>
          <p><strong>Fecha:</strong> ${fecha || "Histórica / Actual"}</p>
          <p><strong>Tasa de Inflación:</strong> ${tasa}%</p>
          <p><strong>Tasa de Interés usada:</strong> ${data.tasa_interes?.toFixed(2) || "Automática"}%</p>
          <p><strong>PIB usado:</strong> ${data.pib || "Automático"}</p>
          <p><strong>Precio del Petróleo:</strong> ${data.petroleo || "Automático"}</p>
          <h2 class="resultado-final">${data.prediccion.toFixed(2)} MXN/USD</h2>
        </div>`;

      // 🔹 Generar gráfica
      const datosGrafica = {
        inflacion: tasa,
        tasa_interes: tasa_interes || null,
        tipo_cambio_predicho: data.prediccion
      };

      const respGraf = await fetch('/generar_grafica', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosGrafica)
      });

      const dataGraf = await respGraf.json();
      console.log("📈 Gráfica generada:", dataGraf);

      const img = document.getElementById('grafica');
      if (img && dataGraf.grafica_url) {
        img.src = dataGraf.grafica_url + "?t=" + new Date().getTime();
        img.style.display = "block";
      }

    } catch (error) {
      resultado.innerHTML = `<div class="prediction-error"><i class="fas fa-bug"></i> Error al conectar con el servidor.</div>`;
      console.error(error);
    }
  });
}


  // ==========================================================
  // 🔹 SISTEMA DE RECONOCIMIENTO DE EMOCIONES
  // ==========================================================
  let emotionInterval = null;

  // Función para actualizar la emoción detectada
  async function updateEmotion() {
    try {
      console.log("🔄 Actualizando emoción...");
      const response = await fetch('/emotion');
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📊 Emoción detectada:", data);
      
      const emotionElement = document.getElementById('emotion');
      const emojiElement = document.getElementById('emoji');
      const emotionBox = document.querySelector('.emotion-box');
      
      if (emotionElement) emotionElement.textContent = data.emotion;
      if (emojiElement) emojiElement.textContent = data.emoji;
      
      // Cambiar color según la emoción
      if (emotionBox) {
        const colors = {
          'Feliz': '#4CAF50',
          'Triste': '#2196F3',
          'Enojado': '#F44336',
          'Sorprendido': '#FF9800',
          'Miedo': '#9C27B0',
          'Disgustado': '#795548',
          'Neutral': '#607D8B',
          'Detectando...': '#00b4d8'
        };
        
        emotionBox.style.borderColor = colors[data.emotion] || colors['Detectando...'];
        emotionBox.style.transition = 'border-color 0.5s ease';
      }
    } catch (err) {
      console.error('❌ Error al obtener emoción:', err);
      const emotionElement = document.getElementById('emotion');
      const emojiElement = document.getElementById('emoji');
      
      if (emotionElement) emotionElement.textContent = 'Error de conexión';
      if (emojiElement) emojiElement.textContent = '❌';
    }
  }

  // Función para verificar si estamos en la sección de emociones
  function isEmotionSectionActive() {
    // Verificar por hash en la URL
    if (window.location.hash === '#emociones') {
      return true;
    }
    
    // Verificar si la sección es visible
    const emocionesSection = document.getElementById('emociones');
    if (!emocionesSection) return false;
    
    const rect = emocionesSection.getBoundingClientRect();
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    const windowWidth = window.innerWidth || document.documentElement.clientWidth;
    
    // Verificar si la sección está al menos parcialmente visible
    const vertInView = (rect.top <= windowHeight) && (rect.bottom >= 0);
    const horInView = (rect.left <= windowWidth) && (rect.right >= 0);
    
    return vertInView && horInView;
  }

  // Función para iniciar la detección de emociones
  function startEmotionDetection() {
    if (emotionInterval) {
      return; // Ya está corriendo
    }
    
    console.log('🎭 Iniciando detección de emociones');
    updateEmotion(); // Primera llamada inmediata
    
    emotionInterval = setInterval(updateEmotion, 500);
    
    // Actualizar estado visual
    const statusElement = document.getElementById('status');
    if (statusElement) {
      statusElement.textContent = 'Activo';
      statusElement.style.color = '#4CAF50';
    }
  }

  // Función para detener la detección de emociones
  function stopEmotionDetection() {
    if (emotionInterval) {
      console.log('🛑 Deteniendo detección de emociones');
      clearInterval(emotionInterval);
      emotionInterval = null;
    }
    
    // Actualizar estado visual
    const statusElement = document.getElementById('status');
    if (statusElement) {
      statusElement.textContent = 'Inactivo';
      statusElement.style.color = '#FF5722';
    }
  }

  // Verificar estado de la sección de emociones
  function checkEmotionSection() {
    if (isEmotionSectionActive()) {
      startEmotionDetection();
    } else {
      stopEmotionDetection();
    }
  }

  // Inicializar el sistema de emociones
  function initEmotionSystem() {
    console.log('✅ Inicializando sistema de emociones');
    
    // Verificar al cargar la página
    setTimeout(checkEmotionSection, 100);
    
    // Escuchar eventos de navegación
    window.addEventListener('hashchange', checkEmotionSection);
    window.addEventListener('scroll', checkEmotionSection);
    window.addEventListener('resize', checkEmotionSection);
    
    // Verificar periódicamente
    setInterval(checkEmotionSection, 1000);
  }

  // ==========================================================
  // 🔹 NAVEGACIÓN MEJORADA
  // ==========================================================
  
  // Navegación suave para enlaces internos
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const target = document.querySelector(targetId);
      
      if (target) {
        // Cerrar menú móvil si está abierto
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebarOverlay');
        
        if (sidebar && sidebar.classList.contains('active')) {
          sidebar.classList.remove('active');
          if (sidebarOverlay) sidebarOverlay.classList.remove('active');
        }
        
        // Scroll suave
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Actualizar URL
        history.pushState(null, null, targetId);
        
        // Verificar sección de emociones después de navegar
        setTimeout(checkEmotionSection, 300);
      }
    });
  });

  // Efectos visuales al hacer scroll
  function initScrollEffects() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    const checkVisibility = () => {
      cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (cardTop < windowHeight - 100) {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }
      });
    };

    window.addEventListener('scroll', checkVisibility);
    
    // Trigger inicial
    setTimeout(checkVisibility, 100);
  }

  // ==========================================================
  // 🔹 INICIALIZACIÓN COMPLETA
  // ==========================================================
  initEmotionSystem();
  initScrollEffects();
  
  console.log("Todos los sistemas inicializados");
});

// 🔒 Evitar fechas anteriores al día actual
const fechaInput = document.getElementById("fecha");
const hoy = new Date().toISOString().split("T")[0];
fechaInput.min = hoy;

// 📊 Mostrar descripción cuando haya gráfica
const grafica = document.getElementById("grafica");
const descripcion = document.getElementById("descripcionGrafica");

// Cuando se actualiza la gráfica
function mostrarGrafica(src) {
  grafica.src = src;
  grafica.style.display = "block";
  descripcion.style.display = "block";
}

// 🧩 Zoom centrado con overlay
grafica.addEventListener("click", () => {
  if (!grafica.src) return;

  // Crear fondo oscuro
  const overlay = document.createElement("div");
  overlay.classList.add("zoom-overlay");

  // Crear imagen ampliada
  const imgZoom = document.createElement("img");
  imgZoom.src = grafica.src;
  imgZoom.classList.add("zoomed-image");
  overlay.appendChild(imgZoom);
  document.body.appendChild(overlay);

  let scale = 1;
  let isDragging = false;
  let startX, startY, translateX = 0, translateY = 0;

  // Zoom con scroll
  imgZoom.addEventListener("wheel", (e) => {
    e.preventDefault();
    scale += e.deltaY * -0.001;
    scale = Math.min(Math.max(1, scale), 4);
    imgZoom.style.transform = `scale(${scale}) translate(${translateX}px, ${translateY}px)`;
  });

  // Movimiento con arrastre
  imgZoom.addEventListener("mousedown", (e) => {
    isDragging = true;
    startX = e.clientX - translateX;
    startY = e.clientY - translateY;
    imgZoom.style.cursor = "grabbing";
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
    imgZoom.style.cursor = "grab";
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    translateX = e.clientX - startX;
    translateY = e.clientY - startY;
    imgZoom.style.transform = `scale(${scale}) translate(${translateX}px, ${translateY}px)`;
  });

  // Cerrar con clic o tecla ESC
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.remove();
  });
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") overlay.remove();
  });
});
// Zoom para imágenes del dataset de emociones
document.querySelectorAll(".dataset-img").forEach(img => {
  img.style.cursor = "zoom-in";
  
  img.addEventListener("click", function() {
    const overlay = document.createElement("div");
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.9);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 10000;
      cursor: zoom-out;
    `;
    
    const imgZoom = document.createElement("img");
    imgZoom.src = this.src;
    imgZoom.alt = this.alt;
    imgZoom.style.cssText = `
      max-width: 90%;
      max-height: 90%;
      transform: scale(1);
      transition: transform 0.3s ease;
      border-radius: 10px;
    `;
    
    overlay.appendChild(imgZoom);
    document.body.appendChild(overlay);
    
    // Zoom con scroll
    let scale = 1;
    overlay.addEventListener("wheel", (e) => {
      e.preventDefault();
      if (e.deltaY < 0) {
        scale += 0.1;
      } else {
        scale = Math.max(0.5, scale - 0.1);
      }
      imgZoom.style.transform = `scale(${scale})`;
    });
    
    // Cerrar al hacer click fuera
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        document.body.removeChild(overlay);
      }
    });
    
    // Cerrar con ESC
    document.addEventListener("keydown", function closeOnEsc(e) {
      if (e.key === "Escape") {
        document.body.removeChild(overlay);
        document.removeEventListener("keydown", closeOnEsc);
      }
    });
  });
});
//toggle
function toggleDescripcion(element) {
  const item = element.parentElement;
  item.classList.toggle('active');
}