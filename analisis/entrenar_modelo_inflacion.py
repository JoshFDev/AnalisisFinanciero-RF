import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

RUTA_INFLACION = r"C:\Users\jaboy\Downloads\ProyectoDos\ProyectoB1CD\ProyectoB1CD\datos\INFLACION (1).xlsx"
RUTA_TIPOCAMBIO = r"C:\Users\jaboy\Downloads\ProyectoDos\ProyectoB1CD\ProyectoB1CD\datos\Consulta_20250923-093032320 (1).xlsx"

# ===============================
# CARGA DE LOS ARCHIVOS
# ===============================
df_inflacion = pd.read_excel(RUTA_INFLACION)

df_cambio = pd.read_excel(RUTA_TIPOCAMBIO, header=None, names=["Fecha", "TipoCambio"])

# ===============================
#  PREPARACIÓN DEL DATASET
# ===============================
# Convertir el año de la fecha del tipo de cambio
df_cambio["Fecha"] = pd.to_datetime(df_cambio["Fecha"], errors="coerce")
df_cambio["Año"] = df_cambio["Fecha"].dt.year

# Promediar tipo de cambio por año (para empatar con inflación anual)
df_cambio_anual = df_cambio.groupby("Año")["TipoCambio"].mean().reset_index()

# Unir con el dataset de inflación (por año)
df = pd.merge(df_inflacion, df_cambio_anual, on="Año", how="inner")

# Renombrar columna si es necesario
if "Tasa de Inflación" in df.columns:
    df.rename(columns={"Tasa de Inflación": "Inflacion"}, inplace=True)

# Verificación
print("Columnas del DataFrame final:", df.columns)
print(df.head())

# ===============================
# ENTRENAMIENTO DEL MODELO
# ===============================
X = df[["Inflacion"]]
y = df["TipoCambio"]

modelo = RandomForestRegressor(n_estimators=200, random_state=42)
modelo.fit(X, y)

# ===============================
# GUARDAR MODELO
# ===============================
os.makedirs("analisis/modelos", exist_ok=True)
ruta_modelo = os.path.join("analisis", "modelos", "modelo_inflacion.pkl")
joblib.dump(modelo, ruta_modelo)

print(f"Modelo entrenado y guardado en: {ruta_modelo}")
