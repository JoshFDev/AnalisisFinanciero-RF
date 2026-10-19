# scripts/prediccion_manual.py
import os
import pandas as pd
import joblib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de datos y modelo
MODELO_PATH = os.path.join(ROOT, 'modelo', 'modelo_random_forest_4vars.pkl')
TASA_PATH = os.path.join(ROOT, 'datos', 'Tasa objetivo.xlsx')
PIB_PATH = os.path.join(ROOT, 'datos', 'PIB_trimestral.xlsx')
PETROLEO_PATH = os.path.join(ROOT, 'datos', 'Precio_Petroleo.csv')
INFLACION_PATH = os.path.join(ROOT, 'datos', 'INFLACION (1).xlsx')

# -------------------------
# Cargar modelo
# -------------------------
modelo = joblib.load(MODELO_PATH)

# -------------------------
# Cargar datos auxiliares para lookups
# -------------------------
# Tasa (sin encabezado)
df_tasa = pd.read_excel(TASA_PATH, header=None, names=['Fecha', 'Tasa_interes'])
df_tasa['Fecha'] = pd.to_datetime(df_tasa['Fecha'], dayfirst=True, errors='coerce')
df_tasa = df_tasa.dropna(subset=['Fecha', 'Tasa_interes']).sort_values('Fecha').reset_index(drop=True)

# PIB trimestral (formato de tus ficheros como filas: años, trimestres, datos...)
df_pib_raw = pd.read_excel(PIB_PATH, header=None)
# Primera fila: años (rellenamos hacia la derecha)
años = pd.to_numeric(df_pib_raw.iloc[0], errors='coerce').ffill()
trimestres = df_pib_raw.iloc[1].tolist()
datos = df_pib_raw.iloc[2:].reset_index(drop=True)

lista = []
for col_idx, año in enumerate(años):
    try:
        año_int = int(año)
    except Exception:
        continue
    for fila_idx in range(datos.shape[0]):
        val = datos.iloc[fila_idx, col_idx]
        if pd.notnull(val):
            lista.append({'Año': año_int, 'Trimestre': trimestres[col_idx], 'PIB': val})
df_pib = pd.DataFrame(lista)
df_pib_anual = df_pib.groupby('Año', as_index=False)['PIB'].mean()
df_pib_anual['Fecha'] = pd.to_datetime(df_pib_anual['Año'].astype(int).astype(str) + '-01-01', errors='coerce')
df_pib_anual = df_pib_anual.dropna(subset=['Fecha']).sort_values('Fecha').reset_index(drop=True)

# Petróleo (csv sin encabezado: Fecha, Cierre)
df_pet = pd.read_csv(PETROLEO_PATH, encoding='latin1', header=None, names=['Fecha', 'Cierre'])
df_pet['Fecha'] = df_pet['Fecha'].astype(str).str.replace('\ufeff', '')
df_pet['Fecha'] = pd.to_datetime(df_pet['Fecha'], dayfirst=True, errors='coerce')
df_pet = df_pet.dropna(subset=['Fecha', 'Cierre']).sort_values('Fecha').reset_index(drop=True)
df_pet['Año'] = df_pet['Fecha'].dt.year
df_pet_anual = df_pet.groupby('Año', as_index=False)['Cierre'].mean().rename(columns={'Cierre':'Petroleo'})
df_pet_anual['Fecha'] = pd.to_datetime(df_pet_anual['Año'].astype(int).astype(str) + '-01-01', errors='coerce')
df_pet_anual = df_pet_anual.dropna(subset=['Fecha']).sort_values('Fecha').reset_index(drop=True)

# Inflación (si alguna vez quieres lookups)
df_inf = pd.read_excel(INFLACION_PATH)  # ya tiene 'Año' y 'Tasa de Inflación' columnas
df_inf['Fecha'] = pd.to_datetime(df_inf['Año'].astype(str) + '-01-01', errors='coerce')
df_inf = df_inf.dropna(subset=['Fecha']).sort_values('Fecha').reset_index(drop=True)

# -------------------------
# Helpers
# -------------------------
def lookup_most_recent(df, fecha_obj, value_col):
    """
    Busca en df el último registro con Fecha <= fecha_obj y devuelve value_col.
    df debe tener columna 'Fecha' ordenada asc.
    """
    df_f = df[df['Fecha'] <= fecha_obj]
    if df_f.empty:
        return None
    return df_f.iloc[-1][value_col]

# -------------------------
# Función de predicción mixta/manual
# -------------------------
def predecir_manual_mixto(tasa_inflacion,
                          fecha_str="",    # YYYY-MM-DD opcional: si se da, permite lookups históricos
                          tasa_interes_input=None,
                          pib_input=None,
                          petroleo_input=None):
    # Inflación obligatoria
    tasa_inflacion = float(tasa_inflacion)

    fecha_obj = None
    if fecha_str:
        fecha_obj = pd.to_datetime(fecha_str, errors='coerce')
        if fecha_obj is pd.NaT:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD o deja vacío.")

    # Tasa de interés: si el usuario no la pasa y hay fecha, buscamos histórico
    if tasa_interes_input is None:
        if fecha_obj is None:
            raise ValueError("Si no proporcionas tasa_interes, debes dar una fecha para tomar la histórica.")
        tasa_interes = lookup_most_recent(df_tasa, fecha_obj, 'Tasa_interes')
        if tasa_interes is None:
            raise ValueError("No hay tasa histórica anterior a la fecha dada.")
    else:
        tasa_interes = float(tasa_interes_input)

    # PIB: si no se pasa, buscamos histórico por fecha
    if pib_input is None:
        if fecha_obj is None:
            raise ValueError("Si no proporcionas PIB, debes dar una fecha para tomar la histórica.")
        pib = lookup_most_recent(df_pib_anual, fecha_obj, 'PIB')
        if pib is None:
            raise ValueError("No hay PIB histórico anterior a la fecha dada.")
    else:
        pib = float(pib_input)

    # Petróleo
    if petroleo_input is None:
        if fecha_obj is None:
            raise ValueError("Si no proporcionas precio del petróleo, debes dar una fecha para tomar la histórica.")
        petroleo = lookup_most_recent(df_pet_anual, fecha_obj, 'Petroleo')
        if petroleo is None:
            raise ValueError("No hay precio de petróleo histórico anterior a la fecha dada.")
    else:
        petroleo = float(petroleo_input)

    # Preparar input y predecir
    X_pred = pd.DataFrame([{
        'Tasa de Inflación': tasa_inflacion,
        'Tasa_interes': float(tasa_interes),
        'PIB': float(pib),
        'Petroleo': float(petroleo)
    }])

    pred = modelo.predict(X_pred)[0]
    return float(pred)

# -------------------------
# CLI interactivo
# -------------------------
if __name__ == "__main__":
    print("Predicción CON opción mixta (fecha opcional + sobreescritura manual)")
    try:
        tasa_inflacion = float(input("Ingresa la tasa de inflación (%) (obligatorio): ").strip())

        fecha_str = input("Ingresa la fecha (YYYY-MM-DD) [opcional, deja vacío para no usar históricos]: ").strip()

        # Pedimos inputs opcionales; si dejas vacío, usará histórico (si diste fecha)
        tasa_interes_raw = input("Ingresa la tasa de interés (%) [enter = usar histórico según fecha]: ").strip()
        pib_raw = input("Ingresa el PIB (promedio anual) [enter = usar histórico según fecha]: ").strip()
        pet_raw = input("Ingresa precio petróleo (USD/barril) [enter = usar histórico según fecha]: ").strip()

        tasa_interes = float(tasa_interes_raw) if tasa_interes_raw != "" else None
        pib = float(pib_raw) if pib_raw != "" else None
        petroleo = float(pet_raw) if pet_raw != "" else None

        pred = predecir_manual_mixto(tasa_inflacion, fecha_str, tasa_interes, pib, petroleo)
        print(f"\n💰 Tipo de cambio estimado: {pred:.2f} MXN por USD")

    except Exception as e:
        print(f"Error: {e}")
