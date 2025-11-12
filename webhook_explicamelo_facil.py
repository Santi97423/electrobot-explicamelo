from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Cargar el modelo y el vectorizador
model = joblib.load("modelo_entrenado.pkl")
vectorizer = joblib.load("vectorizador.pkl")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No se recibió ninguna pregunta"}), 400

    # Procesar la pregunta con el modelo
    X = vectorizer.transform([question])
    prediction = model.predict(X)[0]

    return jsonify({"answer": f"Esto es lo que aprendí sobre '{question}': {prediction}"})


# 🔹 Ruta base opcional (para que no de 404 en la raíz)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Webhook del bot funcionando correctamente ✅"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
