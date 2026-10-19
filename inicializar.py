
import sys
import os

# Agregar la ruta actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def inicializar_proyecto():
    """Función para inicializar el proyecto generando el modelo y gráficas"""
    print("Inicializando proyecto...")
    
    try:
        # Importar y ejecutar el análisis
        from analisis.modelo_regresion import analizar_devaluacion
        resultados = analizar_devaluacion()
        
        print("Proyecto inicializado correctamente")
        print(f"Precisión del modelo: R² = {resultados['r_cuadrado']:.9f}")
        return True
    except Exception as e:
        print(f"Error durante la inicialización: {e}")
        return False

if __name__ == "__main__":
    if inicializar_proyecto():
        print("Proyecto prueba listo")
    else:
        print("Error al inicializar el proyecto")
        sys.exit(1)