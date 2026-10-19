from flask import Flask, request, jsonify, send_from_directory, Response, render_template
import os
import pandas as pd
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from analisis.graficas import generar_grafica_usuario
import pandas as pd
import joblib
import os
import time

app = Flask(__name__)

modelo_path = os.path.join('modelo', 'modelo_random_forest.pkl')
modelo = joblib.load(modelo_path)
# ==========================================================
#IMPORTAR PREDICCIÓN MANUAL
# ==========================================================
try:
    from scripts.prediccion_manual import predecir_manual_mixto as predecir_manual
    print(" Módulo 'prediccion_manual' importado correctamente")
except ImportError as e:
    print(f" Error al importar 'prediccion_manual': {e}")
    exit(1)

# ==========================================================
# IMPORTAR ANÁLISIS
# ==========================================================
try:
    from analisis.modelo_regresion import analizar_devaluacion
    print(" Función 'analizar_devaluacion' importada correctamente")
except ImportError as e:
    print(f" Error al importar 'analizar_devaluacion': {e}")

# ==========================================================
# IMPORTAR DATASET DE TASAS HISTÓRICAS
# ==========================================================
try:
    from analisis.graficas import df_tasa
    print("✅ Dataset de tasas históricas cargado correctamente")
except ImportError as e:
    print(f"❌ Error al importar 'df_tasa': {e}")
    df_tasa = pd.DataFrame(columns=["Fecha", "Tasa_interes"])

# ==========================================================
# 🔹 INICIALIZAR FLASK
# ==========================================================
app = Flask(__name__)

# ==========================================================
# 🔹 SISTEMA DE RECONOCIMIENTO DE EMOCIONES
# ==========================================================
# Cargar modelo de emociones
try:
    model = tf.keras.models.load_model('emotion_model.h5')
    print("✅ Modelo de emociones cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar el modelo de emociones: {e}")
    model = None

# Lista de emociones y emojis
EMOTIONS = ['Enojado', 'Disgustado', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorprendido']
EMOJI = {
    'Enojado': '😠',
    'Disgustado': '🤢',
    'Miedo': '😨',
    'Feliz': '😄',
    'Neutral': '😐',
    'Triste': '😢',
    'Sorprendido': '😮'
}

# Cargar clasificador de rostros
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("✅ Clasificador de rostros cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar el clasificador de rostros: {e}")
    face_cascade = None

current_emotion = {'emotion': 'Detectando...', 'emoji': '🧠'}

def gen_frames():
    global current_emotion
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) if face_cascade else []

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                roi = cv2.resize(roi, (48, 48))
                roi = roi.astype('float') / 255.0
                roi = np.expand_dims(roi, axis=(0, -1))

                # Predicción de emoción
                if model:
                    prediction = model.predict(roi, verbose=0)[0]
                    emotion_idx = np.argmax(prediction)
                    emotion = EMOTIONS[emotion_idx]
                    confidence = np.max(prediction)

                    current_emotion['emotion'] = emotion
                    current_emotion['emoji'] = EMOJI[emotion]

                    color = (0, 255, 0) if confidence > 0.6 else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"{emotion} ({confidence*100:.1f}%)", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ==========================================================
# 🔹 ENDPOINTS DEL SISTEMA DE EMOCIONES
# ==========================================================
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion')
def emotion():
    return jsonify(current_emotion)

# ==========================================================
# 🔹 ENDPOINT: /predecir
# ==========================================================
@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        data = request.get_json(force=True)

        # === Variables principales ===
        tasa_inflacion = data.get("tasa_inflacion")
        fecha_str = data.get("fecha_str")

        # === Variables opcionales ===
        tasa_interes_input = data.get("tasa_interes_input")
        pib_input = data.get("pib_input")
        petroleo_input = data.get("petroleo_input")

        # === Validaciones ===
        if tasa_inflacion is None or tasa_inflacion == "":
            return jsonify({"error": "Debes proporcionar la tasa de inflación"}), 400

        # Validar formato de fecha
        fecha_obj = pd.to_datetime(fecha_str, errors='coerce') if fecha_str else None
        if fecha_str and pd.isna(fecha_obj):
            return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}), 400

        # === Tasa de interés histórica (si aplica) ===
        tasa_interes_hist = None
        if fecha_obj is not None and not df_tasa.empty:
            df_filtrado = df_tasa[df_tasa['Fecha'] <= fecha_obj]
            if not df_filtrado.empty:
                tasa_interes_hist = df_filtrado['Tasa_interes'].iloc[-1]

        # === Determinar tasa final ===
        try:
            if tasa_interes_input:
                tasa_interes_final = float(tasa_interes_input)
            elif tasa_interes_hist is not None:
                tasa_interes_final = float(tasa_interes_hist)
            else:
                tasa_interes_final = None
        except ValueError:
            return jsonify({"error": "La tasa de interés debe ser numérica"}), 400

        # === Ejecutar predicción ===
        try:
            prediccion = predecir_manual(
                tasa_inflacion=float(tasa_inflacion),
                fecha_str=fecha_str or "",
                tasa_interes_input=tasa_interes_final,
                pib_input=pib_input,
                petroleo_input=petroleo_input
            )
        except Exception as e:
            return jsonify({"error": f"Error en la predicción: {str(e)}"}), 400

        # === Generar gráfica ===
        try:
            # Llama a tu función que genera la gráfica (ajusta el nombre si difiere)
            grafica_path = generar_grafica_usuario(prediccion, fecha_str, tasa_interes_final)
            grafica_url = f"/assets/imagenes/graficas/grafica_usuario.png?t={int(time.time()*1000)}"
        except Exception as e:
            grafica_url = None  # Si falla la gráfica, no rompemos la predicción

        # === Respuesta final ===
        return jsonify({
            "prediccion": round(prediccion, 2),
            "tasa_interes": tasa_interes_final if tasa_interes_final is not None else "Histórico/Automático",
            "pib": pib_input or "Histórico/Automático",
            "petroleo": petroleo_input or "Histórico/Automático",
            "grafica_url": grafica_url
        })

    except Exception as e:
        return jsonify({"error": f"Error en el endpoint: {str(e)}"}), 500


# ==========================================================
# 🔹 ENDPOINT: /analizar
# ==========================================================
@app.route('/analizar', methods=['GET'])
def analizar():
    try:
        resultados = analizar_devaluacion()
        return jsonify({
            "mensaje": "✅ Análisis completado correctamente",
            "r2": round(resultados.get("r_cuadrado", 0), 4)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================================
#ENDPOINT: INTERFAZ PRINCIPAL
# ==========================================================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# ==========================================================
# 🔹 FUNCIÓN OPCIONAL: LISTAR ESTRUCTURA DE CARPETAS
# ==========================================================
def listar_archivos_carpeta(ruta, nivel=0):
    prefijo = "│   " * (nivel - 1) + ("├── " if nivel > 0 else "")
    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)
        print(f"{prefijo}{elemento}")
        if os.path.isdir(ruta_completa):
            listar_archivos_carpeta(ruta_completa, nivel + 1)

# ==========================================================
#CARGAR DATASET REAL DE TIPO DE CAMBIO (EXCEL)
# ==========================================================
excel_path = r"C:\Users\jaboy\Downloads\ProyectoDos\ProyectoB1CD\ProyectoB1CD\datos\Consulta_20250923-093032320 (1).xlsx"

try:
    df_original = pd.read_excel(excel_path)
    print(f"✅ Dataset cargado correctamente desde: {excel_path}")
    print(f"📊 Columnas detectadas: {list(df_original.columns)}")

    # Normalizar nombres de columnas (por si vienen con espacios)
    df_original.columns = df_original.columns.str.strip()

    # Verificar que tenga las columnas necesarias
    if "TipoCambio" not in df_original.columns:
        print("")
    else:
        print("✅ Columna 'TipoCambio' detectada correctamente.")

except Exception as e:
    print(f"Error al cargar el dataset: {e}")
    df_original = pd.DataFrame()

import time

import time
from flask import request, jsonify
from analisis.graficas import generar_grafica_usuario

@app.route('/generar_grafica', methods=['POST'])
def generar_grafica():
    data = request.get_json()
    inflacion = data.get('inflacion')
    tasa_interes = data.get('tasa_interes', None)
    tipo_cambio_predicho = data.get('tipo_cambio_predicho', None)  # ✅ lo leemos

    if inflacion is None:
        return jsonify({"error": "No se recibió la inflación"}), 400

    try:
        ruta = generar_grafica_usuario(
            modelo,
            inflacion_usuario=float(inflacion),
            tasa_interes_usuario=float(tasa_interes) if tasa_interes else None,
            tipo_cambio_fijo=float(tipo_cambio_predicho) if tipo_cambio_predicho else None  # ✅ la función lo debe aceptar
        )

        timestamp = int(time.time() * 1000)
        url = f"/{ruta.replace('\\', '/')}?t={timestamp}"
        return jsonify({"grafica_url": url})

    except Exception as e:
        print(" Error al generar gráfica:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# EJECUCIÓN DEL SERVIDOR
# ==========================================================
if __name__ == "__main__":
    ruta_proyecto = r"C:\Users\jaboy\Downloads\ProyectoDos\ProyectoB1CD\ProyectoB1CD"
    listar_archivos_carpeta(ruta_proyecto)

    os.makedirs("assets/imagenes/graficas", exist_ok=True)

    print("Iniciando servidor Flask")
    print("Accede a: http://127.0.0.1:5000")
    app.run(debug=True)