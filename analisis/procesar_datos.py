# analisis/procesar_datos.py
import os
import pandas as pd

def cargar_y_procesar_datos():
    """
    Carga y procesa todos los datasets:
    - Tipo de cambio
    - Inflación
    - Tasa de interés
    - PIB anual
    - Petróleo
    Devuelve un DataFrame combinado listo para usar en el modelo.
    """
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ==========================
    # Rutas a archivos
    # ==========================
    TIPO_CAMBIO_PATH = os.path.join(ROOT, 'datos', 'Consulta_20250923-093032320 (1).xlsx')
    INFLACION_PATH = os.path.join(ROOT, 'datos', 'INFLACION (1).xlsx')
    TASA_PATH = os.path.join(ROOT, 'datos', 'Tasa objetivo.xlsx')
    PIB_PATH = os.path.join(ROOT, 'datos', 'PIB_trimestral.xlsx')
    PETROLEO_PATH = os.path.join(ROOT, 'datos', 'Precio_Petroleo.csv')

    # ==========================
    # Tipo de cambio
    # ==========================
    df_tc = pd.read_excel(TIPO_CAMBIO_PATH, skiprows=17, names=['Fecha', 'Tipo_Cambio'])
    df_tc['Fecha'] = pd.to_datetime(df_tc['Fecha'], dayfirst=True, errors='coerce')
    df_tc = df_tc.dropna(subset=['Fecha', 'Tipo_Cambio'])
    df_tc['Año'] = df_tc['Fecha'].dt.year
    df_tc_anual = df_tc.groupby('Año')['Tipo_Cambio'].mean().reset_index()

    # ==========================
    # Inflación
    # ==========================
    df_inf = pd.read_excel(INFLACION_PATH)
    df_inf['Fecha'] = pd.to_datetime(df_inf['Año'].astype(str) + '-01-01', errors='coerce')
    df_inf['Año'] = df_inf['Fecha'].dt.year

    # ==========================
    # Tasa de interés
    # ==========================
    df_tasa = pd.read_excel(TASA_PATH, header=None, names=['Fecha', 'Tasa_interes'])
    df_tasa['Fecha'] = pd.to_datetime(df_tasa['Fecha'], dayfirst=True, errors='coerce')
    df_tasa['Año'] = df_tasa['Fecha'].dt.year
    df_tasa_anual = df_tasa.groupby('Año')['Tasa_interes'].mean().reset_index()

    # ==========================
    # PIB trimestral -> PIB anual
    # ==========================
    df_pib_raw = pd.read_excel(PIB_PATH, header=None)
    años_raw = df_pib_raw.iloc[0].ffill()  # rellenar vacíos
    años = pd.to_numeric(años_raw, errors='coerce').ffill().astype(int).tolist()
    trimestres = df_pib_raw.iloc[1].tolist()
    datos = df_pib_raw.iloc[2:].reset_index(drop=True)

    lista_filas = []
    for col_idx, año in enumerate(años):
        for fila_idx in range(datos.shape[0]):
            pib_val = datos.iloc[fila_idx, col_idx]
            if pd.notnull(pib_val):
                lista_filas.append({'Año': año, 'Trimestre': trimestres[col_idx], 'PIB': pib_val})
    df_pib = pd.DataFrame(lista_filas)
    df_pib_anual = df_pib.groupby('Año')['PIB'].mean().reset_index()

    # ==========================
    # Petróleo
    # ==========================
    df_pet = pd.read_csv(PETROLEO_PATH, encoding='latin1', header=None, names=['Fecha', 'Cierre'])
    df_pet['Fecha'] = df_pet['Fecha'].astype(str).str.replace('\ufeff', '')
    df_pet['Fecha'] = pd.to_datetime(df_pet['Fecha'], dayfirst=True, errors='coerce')
    df_pet['Año'] = df_pet['Fecha'].dt.year
    df_pet_anual = df_pet.groupby('Año')['Cierre'].mean().reset_index()
    df_pet_anual = df_pet_anual.rename(columns={'Cierre': 'Petroleo'})

    # ==========================
    # Unir todos los datos
    # ==========================
    df = df_tc_anual.merge(df_inf[['Año', 'Tasa de Inflación']], on='Año', how='outer')
    df = df.merge(df_tasa_anual, on='Año', how='outer')
    df = df.merge(df_pib_anual[['Año', 'PIB']], on='Año', how='outer')
    df = df.merge(df_pet_anual, on='Año', how='outer')
    df = df.rename(columns={'Tipo_Cambio': 'TipoCambio'})

    # Quitar filas con NA
    df = df.rename(columns={'Tasa de Inflación': 'Inflacion'})

    return df
