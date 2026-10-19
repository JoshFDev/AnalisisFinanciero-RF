import os
import sys
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# analisis/__init__.py
from .graficas import (
    generar_grafica_random_forest,
    generar_matriz_confusion,
    generar_arboles_decision_simple,
    generar_grafica_importancia
)

from .procesar_datos import cargar_y_procesar_datos


def analizar_devaluacion():
    print("Cargando y procesando datos...")
    df_combinado = cargar_y_procesar_datos()

    X = df_combinado[['Tasa de Inflación']].values
    y = df_combinado['Tipo_Cambio'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🤖 Entrenando modelo Random Forest...")
    modelo = RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    os.makedirs("assets/modelos", exist_ok=True)
    ruta_modelo = os.path.join("assets/modelos", "modelo_entrenado.pkl")
    joblib.dump(modelo, ruta_modelo)

    print("🎨 Generando gráficas...")
    generar_grafica_random_forest(df_combinado, modelo)
    generar_matriz_confusion(y_test, y_pred)
    generar_arboles_decision_simple(modelo, feature_names=['Tasa de Inflación'], max_arboles=2)
    generar_grafica_importancia(modelo, feature_names=['Tasa de Inflación'])

    print("Análisis completado")
    print(f"R²: {r2:.4f}")
    print(f"Modelo guardado en: {ruta_modelo}")

    return {'r_cuadrado': r2, 'modelo': modelo, 'df_combinado': df_combinado}

def predecir_tipo_cambio(tasa_inflacion):
    ruta_modelo = os.path.join("assets/modelos", "modelo_entrenado.pkl")
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError("Modelo no encontrado. Ejecuta primero analizar_devaluacion()")
    modelo = joblib.load(ruta_modelo)
    return float(modelo.predict(np.array([[tasa_inflacion]]))[0])

if __name__ == "__main__":
    analizar_devaluacion()
