import os
from analisis.procesar_datos import cargar_y_procesar_datos
from analisis.graficas import generar_grafica_random_forest
from analisis.modelo_regresion import analizar_devaluacion

def generar_reporte_html(resultados, df):
    """Genera el archivo HTML final con los resultados del análisis"""
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(ROOT, 'index.html')

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Análisis histórico de la devaluación del peso mexicano y su impacto en la economía nacional</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <div class="layout">

    <!-- ======== MENÚ LATERAL ======== -->
    <nav class="sidebar" id="sidebar">
      <div class="menu-header">
        <div class="logo-container">
          <i class="fas fa-chart-line logo-icon"></i>
          <h2 class="menu-title">Análisis Financiero</h2>
        </div>
        <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>

      <ul class="menu-links">
        <li><a href="#introduccion" class="menu-link blue"><i class="fas fa-home"></i><span>Introducción</span></a></li>
        <li><a href="#resultados" class="menu-link green"><i class="fas fa-chart-bar"></i><span>Resultados</span></a></li>
        <li><a href="#graficas" class="menu-link aero"><i class="fas fa-chart-pie"></i><span>Gráficas</span></a></li>
        <li><a href="#prediccion" class="menu-link orange"><i class="fas fa-calculator"></i><span>Predicción</span></a></li>
        <li><a href="#datos" class="menu-link purple"><i class="fas fa-database"></i><span>Datos</span></a></li>
      </ul>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar"><i class="fas fa-user"></i></div>
          <div class="user-details">
            <span class="user-name">Proyecto UAEMex</span>
            <span class="user-role">Ciencia de Datos</span>
          </div>
        </div>
        <div class="footer-mini">© 2025 UAEMex</div>
      </div>
    </nav>

    <div class="sidebar-overlay" id="sidebarOverlay"></div>

    <!-- ======== CONTENIDO PRINCIPAL ======== -->
    <div class="main-content">

      <!-- HERO -->
      <header class="hero">
        <div class="hero-content">
          <div class="hero-badge">Análisis en Tiempo Real</div>
          <h1 class="hero-title">Análisis de la Devaluación del <span class="highlight">Peso Mexicano</span></h1>
          <p class="subtitle">Análisis histórico de la devaluación del peso mexicano y su impacto en la economía nacional · 1996–2024</p>
          <div class="hero-actions">
            <button id="btnDescargar" class="btn-primary"><i class="fas fa-download"></i> Descargar Reporte</button>
            <button class="btn-secondary"><i class="fas fa-chart-line"></i> Ver Tendencias</button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="chart-placeholder animated-chart">
            <div class="chart-bar" style="height: 30%"></div>
            <div class="chart-bar" style="height: 60%"></div>
            <div class="chart-bar" style="height: 45%"></div>
            <div class="chart-bar" style="height: 80%"></div>
            <div class="chart-bar" style="height: 55%"></div>
            <div class="chart-bar" style="height: 70%"></div>
          </div>
        </div>
      </header>

      <main>
        <!-- INTRODUCCIÓN -->
        <section id="introduccion" class="card fade-in">
          <div class="section-header"><i class="fas fa-home section-icon"></i><h2>Introducción</h2></div>
          <p>La devaluación del peso mexicano ha sido un fenómeno recurrente en distintos periodos de la historia económica del país, impactando tanto a nivel social como financiero. Este proyecto analiza la relación entre el tipo de cambio y la tasa de inflación mediante modelos de regresión polinomial, destacando tendencias clave y resultados significativos.</p>
          <div class="info-grid">
            <div class="info-item"><i class="fas fa-calendar-alt"></i><div><h4>Periodo de Estudio</h4><p>1996 - 2024</p></div></div>
            <div class="info-item"><i class="fas fa-chart-line"></i><div><h4>Método de Análisis</h4><p> Random Forest </p></div></div>
            <div class="info-item"><i class="fas fa-database"></i><div><h4>Fuentes de Datos</h4><p>Banxico & INEGI</p></div></div>
          </div>
        </section>

        <!-- RESULTADOS -->
        <section id="resultados" class="card fade-in">
          <div class="section-header"><i class="fas fa-chart-bar section-icon"></i><h2>Resultados Estadísticos</h2></div>
          <div class="metricas">
            <div class="metrica tile"><div class="metrica-icon"><i class="fas fa-project-diagram"></i></div><span>Modelo Usado</span><h3 id="ecuacion">Random Forest</h3><p class="metrica-desc">Algoritmo de ensamble para regresión</p></div>
            <div class="metrica tile"><div class="metrica-icon"><i class="fas fa-crosshairs"></i></div><span>Coeficiente R²</span><h3 id="r-cuadrado">0.8726</h3><p class="metrica-desc">Alta precisión predictiva</p></div>
            <div class="metrica tile"><div class="metrica-icon"><i class="fas fa-percentage"></i></div><span>Precisión del Modelo</span><h3 id="porcentaje">87.26%</h3><p class="metrica-desc">Tasa de acierto en predicciones</p></div>
          </div>
        </section>

        <!-- GRÁFICAS -->
        <section id="graficas" class="card fade-in">
          <div class="section-header"><i class="fas fa-chart-pie section-icon"></i><h2>Visualizaciones Generadas</h2></div>
          <div class="graficas-grid">
            <div class="grafica-item card">
              <div class="grafica-header"><h3>Random Forest: Tipo de Cambio vs Inflación</h3></div>
              <div class="grafica-media"><img src="assets/imagenes/graficas/regresion_random_forest.png" alt="Gráfica Random Forest"></div>
            </div>
            <div class="grafica-item card">
              <div class="grafica-header"><h3>Matriz de Confusión</h3></div>
              <div class="grafica-media"><img src="assets/imagenes/graficas/matriz_confusion.png" alt="Matriz de Confusión"></div>
            </div>
            <div class="grafica-item card">
              <div class="grafica-header"><h3>Importancia de Características</h3></div>
              <div class="grafica-media"><img src="assets/imagenes/graficas/importancia_caracteristicas.png" alt="Importancia de Características"></div>
            </div>
            <div class="grafica-item card">
              <div class="grafica-header"><h3>Primer Arbol de Decision</h3></div>
              <div class="grafica-media"><img src="assets/imagenes/graficas/arbol_decision_1.png" alt="Importancia de Características"></div>
            </div>            
          </div>
        </section>

<!-- PREDICCIÓN -->
<section id="prediccion" class="card fade-in">
  <div class="section-header"><i class="fas fa-calculator section-icon"></i><h2>Predicción del Tipo de Cambio</h2></div>
  <p>Introduce los valores requeridos para estimar el tipo de cambio. Puedes dejar algunos campos vacíos para que se usen datos históricos según la fecha seleccionada.</p>
  
  <div class="prediccion-container">
    <div class="prediccion-box">

      <!-- Tasa de inflación -->
      <div class="input-group">
        <label for="tasa"><i class="fas fa-percentage"></i> Tasa de inflación (%) <span style="color:red">*</span></label>
        <input type="number" id="tasa" placeholder="Ej: 5.2" step="0.01" min="0" required>
      </div>

      <!-- Fecha -->
      <div class="input-group">
        <label for="fecha"><i class="fas fa-calendar"></i> Fecha (YYYY-MM-DD)</label>
        <input type="date" id="fecha" placeholder="Opcional si das los datos manualmente">
      </div>

      <!-- Tasa de interés -->
      <div class="input-group">
        <label for="tasa_interes"><i class="fas fa-chart-line"></i> Tasa de interés (%)</label>
        <input type="number" id="tasa_interes" placeholder="Ej: 10.5 (deja vacío para usar histórico)" step="0.01" min="0">
      </div>

      <!-- PIB -->
      <div class="input-group">
        <label for="pib"><i class="fas fa-chart-area"></i> PIB promedio anual</label>
        <input type="number" id="pib" placeholder="Ej: 1850000 (deja vacío para usar histórico)" step="0.01">
      </div>

      <!-- Precio del petróleo -->
      <div class="input-group">
        <label for="petroleo"><i class="fas fa-oil-can"></i> Precio del petróleo (USD/barril)</label>
        <input type="number" id="petroleo" placeholder="Ej: 75.3 (deja vacío para usar histórico)" step="0.01" min="0">
      </div>

      <button id="btnPredecir" class="btn-predict"><i class="fas fa-bolt"></i> Predecir</button>
    </div>

    <div id="resultadoPrediccion" class="resultado-prediccion">
      <div class="prediction-placeholder">
        <i class="fas fa-search-dollar"></i>
        <p>Completa al menos la tasa de inflación y/o la fecha para obtener una predicción.</p>
      </div>
    </div>
  </div>
</section>


        <!-- DATOS -->
        <section id="datos" class="card fade-in">
          <div class="section-header"><i class="fas fa-database section-icon"></i><h2>Datos Utilizados</h2></div>
          <div class="datos-info">
            <div class="fuente">
              <div class="fuente-icon"><i class="fas fa-university"></i></div>
              <h3>Banco de México</h3>
              <p>Serie histórica del tipo de cambio peso-dólar (1954–2025)</p>
            </div>
            <div class="fuente">
              <div class="fuente-icon"><i class="fas fa-chart-line"></i></div>
              <h3>INEGI</h3>
              <p>Tasa de inflación anual (1996–2024)</p>
            </div>
          </div>
        </section>
    <!-- BOTÓN PARA MOSTRAR DATOS -->
    <div class="boton-mostrar-container" style="text-align: center; margin: 30px 0;">
        <button id="btnMostrarDatos" class="btn-primary">
            <i class="fas fa-table"></i> Mostrar Datos de Inflación
        </button>
    </div>

<section style="background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <h2 style="text-align: center; margin-bottom: 15px; color: #333;">📊 Vista previa del dataset de Inflación</h2>
  <p style="text-align: center; color: #666; margin-bottom: 20px;">Datos históricos de inflación en México (1996-2025*)</p>

  <div style="overflow-x: auto; border: 2px solid #e0e0e0; border-radius: 4px; padding: 10px;">
    <table id="tablaExcel" style="width: 100%; border-collapse: collapse; background: white;">
      <thead style="background: #667eea;">
        <tr id="cabecera"></tr>
      </thead>
      <tbody id="cuerpo"></tbody>
    </table>
  </div>
  
  <p style="text-align: center; color: #888; margin-top: 10px; font-size: 14px;">*Proyección para 2025</p>
</section>

      </main>

      <footer>
        <div class="footer-content">
          <div class="footer-brand"><i class="fas fa-chart-line"></i><span>Análisis Financiero UAEMex</span></div>
          <p>© 2025 Proyecto de Ciencia de Datos | Universidad Autónoma del Estado de México</p>
        </div>
      </footer>
    </div>
  </div>

  <script src="assets/js/script.js" defer></script>
</body>
</html>

"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ HTML generado en {html_path}")


def main():
    print("🚀 Iniciando análisis de devaluación del peso mexicano...")
    df = cargar_y_procesar_datos()
    resultados = analizar_devaluacion()
    generar_grafica_random_forest(df, resultados['modelo'])
    generar_reporte_html(resultados, df)
    print("✅ ¡Análisis completado!")


if __name__ == "__main__":
    main()
