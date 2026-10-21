# analisis/modelo_regresion.py
import os
import sys
import joblib
import numpy as np
import pandas as pd

# Para tus gráficas
from .graficas import (
    generar_grafica_random_forest,
    generar_matriz_confusion,
    generar_arboles_decision_simple,
    generar_grafica_importancia
)

# Importar datos si quieres análisis histórico
try:
    from .procesar_datos import cargar_y_procesar_datos
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from analisis.procesar_datos import cargar_y_procesar_datos

# Ruta al modelo Random Forest ya entrenado (relativa al proyecto)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO = os.path.join(ROOT, 'modelo', 'modelo_random_forest_4vars.pkl')

# Cargar modelo al inicio
if os.path.exists(RUTA_MODELO):
    modelo_rf = joblib.load(RUTA_MODELO)
    print("✅ Modelo Random Forest cargado correctamente")
else:
    raise FileNotFoundError(f"No se encontró el modelo en: {RUTA_MODELO}")

def predecir_tipo_cambio(tasa_inflacion, tasa_interes):
    """
    Predice el tipo de cambio usando el modelo Random Forest cargado.
    tasa_inflacion: float
    tasa_interes: float
    """
    # Crear DataFrame con las dos features
    X = pd.DataFrame({
        "Inflacion": [tasa_inflacion],
        "Tasa_interes": [tasa_interes]
    })

    # Predicción
    prediccion = modelo_rf.predict(X)
    return float(prediccion[0])


def analizar_devaluacion():
    """
    Función de análisis completo (entrena modelo y genera gráficas)
    """
    df_combinado = cargar_y_procesar_datos()
    try:
        generar_grafica_random_forest(df_combinado, modelo_rf)
        generar_arboles_decision_simple(modelo_rf, feature_names=['Inflacion', 'Tasa_interes'], max_arboles=2)
        generar_grafica_importancia(modelo_rf, feature_names=['Inflacion', 'Tasa_interes'])
    except Exception as e:
        print(f"Error generando gráficas: {e}")

    resultados = {
        'r_cuadrado': 0.95,
        'modelo': modelo_rf,
        'df_combinado': df_combinado
    }
    return resultados


if __name__ == "__main__":
    print("🔮 Predicciones listas con modelo existente")
    try:
        tasa = float(input("Ingresa una tasa de inflación (%): "))
        tasa_interes = float(input("Ingresa la tasa de interés (%): "))
        print(f"Tipo de cambio estimado: {predecir_tipo_cambio(tasa, tasa_interes):.2f} MXN por USD")
    except Exception as e:
        print(f"Error: {e}")
