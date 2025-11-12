from flask import Flask, request, jsonify
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import os

app = Flask(__name__)

# --- Función para entrenar o cargar el modelo ---
def obtener_modelo():
    try:
        # Intentar cargar modelo existente
        modelo = joblib.load('modelo_explicamelo_facil.joblib')
        vectorizador = joblib.load('vectorizador.joblib')
        print("✅ Modelo y vectorizador cargados desde archivos.")
        return modelo, vectorizador
    except:
        print("🔄 Entrenando nuevo modelo...")
        return entrenar_modelo()

# --- Dataset de entrenamiento ---
def entrenar_modelo():
    preguntas = [
        # CDIO
        "qué es cdio", "modelo cdio", "significado de cdio", "qué significa cdio", "explica cdio",
        # Misión
        "cuál es la misión", "dime la misión", "cuál es la mision del programa",
        # Visión
        "cuál es la visión", "dime la visión", "qué dice la visión",
        # Perfil profesional
        "qué es perfil profesional", "qué hace un ingeniero electrónico", "perfil profesional del ingeniero electrónico",
        # Materias
        "qué materias hay", "malla curricular", "qué materias se ven en sexto semestre", "materias del programa",
        # Proyección social
        "qué es proyección social", "en qué consiste la proyección social"
    ]

    clases = [
        "cdio","cdio","cdio","cdio","cdio",
        "mision","mision","mision",
        "vision","vision","vision",
        "perfil","perfil","perfil",
        "materias","materias","materias","materias",
        "proyeccion","proyeccion"
    ]

    # Preprocesamiento
    def limpiar_texto(t):
        t = t.lower()
        t = re.sub(r'[^a-záéíóúñ\s]', '', t)
        return t

    preguntas = [limpiar_texto(p) for p in preguntas]

    # Entrenar modelo
    vectorizador = TfidfVectorizer()
    X = vectorizador.fit_transform(preguntas)

    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X, clases)

    # Guardar modelo
    joblib.dump(modelo, "modelo_explicamelo_facil.joblib")
    joblib.dump(vectorizador, "vectorizador.joblib")
    
    print("✅ Modelo entrenado y guardado correctamente.")
    return modelo, vectorizador

# --- Cargar modelo al iniciar ---
modelo, vectorizador = obtener_modelo()

# --- Ruta de prueba ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Webhook del bot funcionando correctamente ✅",
        "status": "active",
        "model_loaded": modelo is not None
    })

# --- Ruta principal del webhook ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        if modelo is None or vectorizador is None:
            return jsonify({"error": "El modelo o el vectorizador no están cargados"}), 500

        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "No se recibió ninguna pregunta"}), 400

        question = data["question"]
        
        # Preprocesar la pregunta igual que en entrenamiento
        def limpiar_texto(t):
            t = t.lower()
            t = re.sub(r'[^a-záéíóúñ\s]', '', t)
            return t
        
        question_limpia = limpiar_texto(question)
        X = vectorizador.transform([question_limpia])
        prediction = modelo.predict(X)[0]

        # Respuestas más informativas
        respuestas = {
            "cdio": "CDIO es un modelo educativo innovador (Concebir, Diseñar, Implementar, Operar) que prepara a los ingenieros para enfrentar desafíos reales.",
            "mision": "La misión del programa es formar ingenieros electrónicos con competencias técnicas y humanísticas.",
            "vision": "La visión es ser un programa reconocido por su excelencia académica e impacto en la sociedad.",
            "perfil": "El ingeniero electrónico diseña, implementa y mantiene sistemas electrónicos y de telecomunicaciones.",
            "materias": "El plan de estudios incluye matemáticas, física, circuitos, electrónica digital, programación y más.",
            "proyeccion": "La proyección social conecta a la universidad con la comunidad mediante proyectos de impacto."
        }
        
        respuesta = respuestas.get(prediction, f"Tema identificado: {prediction}. Próximamente más información.")

        response = {
            "answer": respuesta,
            "detected_topic": prediction,
            "original_question": question
        }
        return jsonify(response)

    except Exception as e:
        print(f"⚠️ Error interno: {str(e)}")
        return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
