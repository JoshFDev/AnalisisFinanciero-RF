# analisis/graficas.py
import os
import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')  # Evita problemas de Tkinter / GUI
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, confusion_matrix
from sklearn.tree import plot_tree
import seaborn as sns

# ==========================
# Rutas de archivos
# ==========================
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIPO_CAMBIO_PATH = os.path.join(ROOT, 'datos', 'Consulta_20250923-093032320 (1).xlsx')
INFLACION_PATH = os.path.join(ROOT, 'datos', 'INFLACION (1).xlsx')
TASA_PATH = os.path.join(ROOT, 'datos', 'Tasa objetivo.xlsx')

# ==========================
# Cargar datasets
# ==========================
df_tc = pd.read_excel(TIPO_CAMBIO_PATH, header=None, names=['Fecha', 'Tipo_Cambio'])
df_inf = pd.read_excel(INFLACION_PATH)
df_tasa = pd.read_excel(TASA_PATH, header=None, names=['Fecha', 'Tasa_interes'])

# ==========================
# Formatear fechas
# ==========================
df_tc['Fecha'] = pd.to_datetime(df_tc['Fecha'], dayfirst=True, errors='coerce')
df_tasa['Fecha'] = pd.to_datetime(df_tasa['Fecha'], dayfirst=True, errors='coerce')
df_inf['Fecha'] = pd.to_datetime(df_inf['Año'].astype(str) + '-01-01')

# ==========================
# Unir datasets
# ==========================
df = pd.merge_asof(df_tc.sort_values('Fecha'),
                df_tasa.sort_values('Fecha'),
                on='Fecha', direction='backward')
df = pd.merge_asof(df.sort_values('Fecha'),
                df_inf.sort_values('Fecha'),
                on='Fecha', direction='backward')
df = df.dropna()
df = df.rename(columns={'Tasa de Inflación': 'Inflacion', 'Tipo_Cambio': 'TipoCambio'})

# ==========================
# Entrenar modelo
# ==========================
X = df[['Inflacion', 'Tasa_interes']]
y = df['TipoCambio']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = RandomForestRegressor(n_estimators=200, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"=== Precisión del modelo (R²): {r2:.4f} ===")

# ==========================
# Guardar modelo
# ==========================
MODELO_DIR = os.path.join(ROOT, 'modelo')
os.makedirs(MODELO_DIR, exist_ok=True)
MODELO_PATH = os.path.join(MODELO_DIR, 'modelo_random_forest.pkl')
joblib.dump(modelo, MODELO_PATH)
print("Modelo entrenado y guardado correctamente.")

# ==========================
# Funciones
# ==========================
def generar_grafica_random_forest(df, modelo):
    X = df[['Inflacion', 'Tasa_interes']].values
    y = df['TipoCambio'].values
    y_pred = modelo.predict(X)
    plt.figure(figsize=(8,5))
    plt.plot(y, label='Real', marker='o')
    plt.plot(y_pred, label='Predicción', marker='x')
    plt.title("Random Forest: Predicción vs Real")
    plt.xlabel("Muestras")
    plt.ylabel("Tipo de Cambio")
    plt.legend()
    plt.grid(True)
    os.makedirs("assets/imagenes/graficas", exist_ok=True)
    plt.savefig("assets/imagenes/graficas/regresion_random_forest.png")
    plt.close()

def generar_matriz_confusion(y_test, y_pred):
    y_test_clas = np.round(y_test)
    y_pred_clas = np.round(y_pred)
    cm = confusion_matrix(y_test_clas, y_pred_clas)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Matriz de Confusión")
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.savefig("assets/imagenes/graficas/matriz_confusion.png")
    plt.close()

def generar_arboles_decision_simple(modelo, feature_names, max_arboles=2):
    os.makedirs("assets/imagenes/graficas", exist_ok=True)
    for i, arbol in enumerate(modelo.estimators_[:max_arboles], 1):
        plt.figure(figsize=(12,8))
        plot_tree(arbol, feature_names=feature_names, filled=True, rounded=True)
        plt.title(f"Árbol {i} del Random Forest")
        plt.savefig(f"assets/imagenes/graficas/arbol_decision_{i}.png")
        plt.close()

def generar_grafica_importancia(modelo, feature_names):

    importancias = modelo.feature_importances_
    plt.figure(figsize=(8,5))
    plt.bar(feature_names, importancias, color='skyblue')
    plt.title("Importancia de Características")
    plt.ylabel("Importancia")
    plt.xlabel("Características")
    os.makedirs("assets/imagenes/graficas", exist_ok=True)
    plt.savefig("assets/imagenes/graficas/importancia_caracteristicas.png")
    plt.close()

def generar_grafica_usuario(modelo, inflacion_usuario, tasa_interes_usuario=None, tipo_cambio_fijo=None):
    import numpy as np
    from .procesar_datos import cargar_y_procesar_datos

    df = cargar_y_procesar_datos().sort_values('Inflacion').astype({'Inflacion': float, 'TipoCambio': float})

    X_hist = df[['Inflacion', 'Tasa_interes']]
    y_pred_hist = modelo.predict(X_hist)

    try:
        if tasa_interes_usuario is None or tasa_interes_usuario == "" or np.isnan(float(tasa_interes_usuario)):
            tasa_interes_usuario = float(df['Tasa_interes'].iloc[-1])
        else:
            tasa_interes_usuario = float(tasa_interes_usuario)
    except Exception:
        tasa_interes_usuario = float(df['Tasa_interes'].iloc[-1])

    # === Crear nuevo punto para predecir ===
    X_nuevo = pd.DataFrame({
        'Inflacion': [float(inflacion_usuario)],
        'Tasa_interes': [tasa_interes_usuario]
    })

    try:
        tipo_cambio_usuario = tipo_cambio_fijo or float(modelo.predict(X_nuevo)[0])
    except Exception as e:
        print(f"Error al predecir tipo de cambio: {e}")
        tipo_cambio_usuario = float(np.mean(y_pred_hist))

    # === Validar valor numérico final ===
    if np.isnan(tipo_cambio_usuario) or not np.isfinite(tipo_cambio_usuario):
        tipo_cambio_usuario = float(np.mean(y_pred_hist))

    # === Crear gráfica ===
    ruta_directorio = os.path.join('assets', 'imagenes', 'graficas')
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta = os.path.join(ruta_directorio, 'grafica_usuario.png')

    plt.figure(figsize=(10, 6))
    plt.plot(df['Inflacion'], y_pred_hist, 'r-x', label='Predicción Modelo RF')
    plt.scatter(df['Inflacion'], df['TipoCambio'], color='blue', label='Datos Históricos')
    plt.scatter(float(inflacion_usuario), tipo_cambio_usuario, color='green', s=120, edgecolors='black',
                label=f'Nuevo Punto ({tipo_cambio_usuario:.2f} MXN/USD)')

    plt.ylim(10, 25)
    plt.xlabel('Inflación (%)')
    plt.ylabel('Tipo de Cambio (MXN/USD)')
    plt.title('Predicción de Tipo de Cambio con Random Forest')
    plt.legend()
    plt.grid(True)
    plt.savefig(ruta, bbox_inches='tight')
    plt.close()

    print(f"Gráfica generada correctamente ({tipo_cambio_usuario:.2f} MXN/USD) [Inflación={inflacion_usuario}%, Tasa={tasa_interes_usuario}%]")
    return ruta
