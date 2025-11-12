from flask import Flask, request, jsonify
import joblib

# --- Inicialización del servidor Flask ---
app = Flask(__name__)

# --- Cargar el modelo y el vectorizador entrenados ---
try:
    modelo = joblib.load('modelo_explicamelo_facil.joblib')
    vectorizador = joblib.load('vectorizador.joblib')
    print("✅ Modelo y vectorizador cargados correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo o el vectorizador: {e}")

# --- Ruta raíz (para verificar que el servidor esté activo) ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Webhook del bot funcionando correctamente ✅"})

# --- Ruta principal del webhook ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "No se recibió ninguna pregunta"}), 400

        question = data["question"]
        X = vectorizer.transform([question])
        prediction = model.predict(X)[0]

        response = {
            "answer": f"Esto es lo que aprendí sobre '{question}': {prediction}"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500

# --- Punto de entrada ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
