# Analisis Financiero RF

Aplicacion web y proyecto de analisis de datos que estudia la devaluacion historica del peso mexicano frente al dolar estadounidense y su relacion con la inflacion, la tasa de interes, el PIB y el precio del petroleo. El proyecto entrena y utiliza modelos de regresion basados en Random Forest para predecir el tipo de cambio, genera visualizaciones del analisis y expone una interfaz web para realizar predicciones manuales o historicas. Incluye ademas un modulo opcional de reconocimiento de emociones faciales mediante webcam.

Repositorio: https://github.com/JoshFDev/AnalisisFinanciero-RF

## Tabla de contenidos

- [Descripcion general](#descripcion-general)
- [Caracteristicas principales](#caracteristicas-principales)
- [Stack tecnologico](#stack-tecnologico)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Fuentes de datos](#fuentes-de-datos)
- [Modelos incluidos](#modelos-incluidos)
- [Requisitos previos](#requisitos-previos)
- [Instalacion](#instalacion)
- [Configuracion](#configuracion)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Salidas generadas](#salidas-generadas)
- [Modulo de reconocimiento de emociones](#modulo-de-reconocimiento-de-emociones)
- [Notas y problemas conocidos](#notas-y-problemas-conocidos)
- [Autor](#autor)

## Descripcion general

El proyecto se divide en dos grandes partes:

1. Pipeline de analisis de datos: carga y procesa las series historicas, entrena un modelo Random Forest y genera graficas de resultados (regresion, matriz de confusion, arboles de decision e importancia de caracteristicas).
2. Aplicacion web Flask: sirve un panel interactivo (index.html) que permite capturar la tasa de inflacion y otros parametros, consultar valores historicos por fecha y obtener una prediccion del tipo de cambio junto con una grafica generada dinamicamente.

El periodo de estudio abarca datos historicos del tipo de cambio desde 1954 (Banco de Mexico) y de inflacion anual desde 1996 (INEGI), complementados con tasa de interes, PIB trimestral y precio del petroleo.

## Caracteristicas principales

- Procesamiento y agregacion anual de multiples fuentes de datos economicos.
- Modelo Random Forest para regresion del tipo de cambio (MXN por USD).
- Prediccion mixta: el usuario puede ingresar valores manualmente o dejar campos vacios para que el sistema obtenga valores historicos segun la fecha indicada.
- Validacion de entradas y manejo de errores en el backend.
- Generacion de graficas dinamicas por usuario (grafica_usuario.png).
- Panel web con formulario de prediccion, visualizacion de resultados y vista previa del dataset de inflacion.
- Modulo opcional de reconocimiento facial y clasificacion de emociones en tiempo real mediante webcam.
- Scripts de analisis y prediccion por linea de comandos.

## Stack tecnologico

Backend y analisis:

- Python 3.8 o superior (probado con 3.12)
- Flask
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- joblib
- OpenCV (opencv-python)
- TensorFlow / Keras

Frontend:

- HTML5
- CSS3
- JavaScript (Fetch API)
- Font Awesome

## Estructura del repositorio

```
AnalisisFinanciero-RF/
|-- analisis/
|   |-- __init__.py
|   |-- graficas.py
|   |-- modelo_regresion.py
|   |-- procesar_datos.py
|   |-- entrenar_modelo_inflacion.py
|   `-- modelos/
|       `-- modelo_inflacion.pkl
|-- assets/
|   |-- css/
|   |-- js/
|   |-- imagenes/
|   |   |-- graficas/
|   |   `-- dataSetEmociones/
|   |-- modelos/
|   |-- pdf/
|   |-- modelo_entrenado.pkl
|   `-- modelo_entrenado_diario.pkl
|-- datos/
|   |-- Consulta_20250923-093032320 (1).xlsx
|   |-- INFLACION (1).xlsx
|   |-- PIB_trimestral.xlsx
|   |-- Precio_Petroleo.csv
|   `-- Tasa objetivo.xlsx
|-- modelo/
|   |-- modelo_random_forest.pkl
|   `-- modelo_random_forest_4vars.pkl
|-- scripts/
|   |-- ejecutar_analisis.py
|   `-- prediccion_manual.py
|-- app.py
|-- config.py
|-- index.html
|-- inicializar.py
|-- run_analisis.py
|-- test_imports.py
|-- requirements.txt
`-- emotion_model.h5
```

## Fuentes de datos

Los archivos se encuentran en la carpeta `datos/`:

- `Consulta_20250923-093032320 (1).xlsx`: serie historica del tipo de cambio peso-dolar (Banco de Mexico).
- `INFLACION (1).xlsx`: tasa de inflacion anual (INEGI).
- `Tasa objetivo.xlsx`: tasa de interes objetivo.
- `PIB_trimestral.xlsx`: PIB trimestral, que se agrega a nivel anual.
- `Precio_Petroleo.csv`: precio del petroleo (cierre), agregado por ano.

El procesamiento convierte las series a frecuencia anual y las combina por ano, generando un DataFrame con las columnas Inflacion, Tasa_interes, PIB, Petroleo y TipoCambio.

## Modelos incluidos

- `modelo/modelo_random_forest.pkl`: modelo entrenado con 2 variables (Inflacion, Tasa_interes). Se utiliza en el pipeline de analisis y en la generacion de graficas historicas.
- `modelo/modelo_random_forest_4vars.pkl`: modelo entrenado con 4 variables (Tasa de Inflacion, Tasa_interes, PIB, Petroleo). Es el modelo utilizado por el endpoint de prediccion manual.
- `assets/modelo_entrenado.pkl` y `assets/modelo_entrenado_diario.pkl`: modelos generados por el pipeline de analisis.
- `analisis/modelos/modelo_inflacion.pkl`: modelo entrenado a partir de inflacion y tipo de cambio anual.
- `emotion_model.h5`: modelo Keras para clasificacion de 7 emociones (Enojado, Disgustado, Miedo, Feliz, Neutral, Triste, Sorprendido).

## Requisitos previos

- Python 3.8 o superior.
- pip.
- Los archivos de datos en `datos/` (incluidos en el repositorio).
- Webcam (opcional, solo para el modulo de reconocimiento de emociones).

## Instalacion

1. Clonar el repositorio:

```
git clone https://github.com/JoshFDev/AnalisisFinanciero-RF.git
cd AnalisisFinanciero-RF
```

2. Crear y activar un entorno virtual:

En Linux o macOS:

```
python3 -m venv venv
source venv/bin/activate
```

En Windows:

```
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

## Configuracion

El proyecto utiliza rutas relativas al directorio raiz del proyecto, por lo que debe ejecutarse desde la carpeta del repositorio. Algunos modulos (por ejemplo `analisis/modelo_regresion.py`) requieren que el modelo `modelo/modelo_random_forest_4vars.pkl` exista; este archivo se incluye en el repositorio.

Si se reentrenan los modelos o se cambian las rutas de los datos, revisar las constantes de ruta en:

- `analisis/procesar_datos.py`
- `analisis/graficas.py`
- `analisis/modelo_regresion.py`
- `analisis/entrenar_modelo_inflacion.py`
- `scripts/prediccion_manual.py`
- `app.py`

## Uso

### Ejecutar el pipeline de analisis

Genera el modelo, las graficas y el reporte HTML:

```
python run_analisis.py
```

O bien:

```
python scripts/ejecutar_analisis.py
```

Esto crea o actualiza archivos en `assets/imagenes/graficas/` y `index.html`.

### Inicializar el proyecto

```
python inicializar.py
```

Ejecuta el analisis de devaluacion y reporta el coeficiente R2 del modelo.

### Ejecutar la aplicacion web

```
python app.py
```

La aplicacion queda disponible en `http://127.0.0.1:5000`.

### Prediccion por linea de comandos

```
python scripts/prediccion_manual.py
```

Solicita la tasa de inflacion (obligatoria) y, de forma opcional, fecha, tasa de interes, PIB y precio del petroleo. Si no se proporcionan los valores opcionales y se indica una fecha, se toman valores historicos.

### Diagnostico de importaciones

```
python test_imports.py
```

Verifica la estructura de carpetas e importaciones basicas.

## Endpoints de la API

La aplicacion Flask expone los siguientes endpoints:

- `GET /`: sirve la interfaz principal (`index.html`).
- `POST /predecir`: recibe un JSON con `tasa_inflacion` (obligatorio) y, opcionalmente, `fecha_str`, `tasa_interes_input`, `pib_input` y `petroleo_input`. Devuelve la prediccion del tipo de cambio y la URL de la grafica generada.
- `GET /analizar`: ejecuta el analisis de devaluacion y devuelve el coeficiente R2.
- `POST /generar_grafica`: genera la grafica de usuario a partir de inflacion, tasa de interes y tipo de cambio predicho.
- `GET /video_feed`: stream de video de la webcam con deteccion de rostros y emociones.
- `GET /emotion`: devuelve la emocion detectada actualmente.
- `GET /assets/<path>`: sirve archivos estaticos de la carpeta `assets/`.

Ejemplo de peticion a `/predecir`:

```
curl -X POST http://127.0.0.1:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"tasa_inflacion": 5.2, "fecha_str": "2024-01-01"}'
```

## Salidas generadas

El pipeline genera archivos en `assets/imagenes/graficas/`:

- `regresion_random_forest.png`: prediccion frente a valores reales.
- `matriz_confusion.png`: matriz de confusion.
- `arbol_decision_1.png` y `arbol_decision_2.png`: arboles de decision del Random Forest.
- `importancia_caracteristicas.png`: importancia de las variables.
- `grafica_usuario.png`: grafica generada dinamicamente para una prediccion del usuario.

Tambien se generan modelos en `assets/modelos/` y `analisis/modelos/`.

## Modulo de reconocimiento de emociones

La aplicacion incluye un modulo opcional que utiliza la webcam para detectar rostros con OpenCV (clasificador Haar Cascade) y clasificar la emocion con el modelo `emotion_model.h5`. Las emociones reconocidas son: Enojado, Disgustado, Miedo, Feliz, Neutral, Triste y Sorprendido.

Este modulo requiere una webcam disponible y las dependencias OpenCV y TensorFlow instaladas. Si no se dispone de webcam o de las dependencias, la aplicacion puede seguir funcionando para el analisis financiero, aunque el stream de video no estara disponible.

## Notas y problemas conocidos

- Algunos modulos cargan datasets y modelos al importarse, por lo que la importacion puede tardar y generar archivos en disco.
- Los nombres de archivo de datos contienen espacios y parentesis; no se deben renombrar sin actualizar las rutas en el codigo.
- El panel web depende de que el servidor Flask este en ejecucion para las predicciones.
- El modulo de emociones requiere hardware de camara y puede no funcionar en entornos sin GUI o sin webcam.
- El archivo `requirements.txt` original solo listaba dependencias basicas; se amplio para incluir OpenCV, TensorFlow, seaborn y joblib, necesarios para ejecutar todas las funcionalidades.

## Autores

Proyecto desarrollado para la Universidad Autonoma del Estado de Mexico (UAEMex), area de Ciencia de Datos, por los ingenieros en computacion:

- Aboytes Uribe Joshua Sebastian
- Cazares Hernandez Sergio Axel
- Estrada Hernandez Agustin

Repositorio: https://github.com/JoshFDev/AnalisisFinanciero-RF
