# webhook_explicamelo_facil.py
from flask import Flask, request, jsonify, abort
import joblib
import re
import numpy as np
import os

app = Flask(__name__)

# --- Cargar modelo y vectorizador ---
modelo = joblib.load("modelo_explicamelo_facil.joblib")
vectorizador = joblib.load("vectorizador.joblib")

# --- Diccionario de respuestas ---
respuestas = {
    "cdio": "📘 *CDIO* significa Concebir, Diseñar, Implementar y Operar. Es un modelo educativo que forma ingenieros a través de proyectos reales.",
    "mision": "🎯 *Misión:* Formar ingenieros electrónicos con calidad humana, ética e innovación tecnológica para el desarrollo regional.",
    "vision": "🌎 *Visión:* Ser un programa líder en formación integral, investigación y proyección social.",
    "perfil": "👨‍🔧 *Perfil profesional:* Diseñar, implementar y gestionar sistemas electrónicos en control, automatización y telecomunicaciones.",
    "materias": "📚 *Materias:* Puedes consultar la malla curricular para ver las asignaturas por semestre. ¿Quieres que te la muestre?",
    "proyeccion": "🤝 *Proyección social:* Es la interacción del programa con la comunidad mediante proyectos que aportan soluciones tecnológicas."
}

# --- Seguridad opcional ---
API_KEY = os.environ.get("API_KEY", None)

def limpiar_texto(t):
    t = t.lower()
    t = re.sub(r'[^a-záéíóúñ\s]', '', t)
    return t

@app.route("/webhook", methods=["POST"])
def webhook():
    # Validación de API key
    if API_KEY:
        header = request.headers.get("x-api-key")
        if header != API_KEY:
            return abort(401)

    data = request.get_json(silent=True)
    texto = data.get("queryResult", {}).get("queryText", "").strip()
    if not texto:
        return jsonify({"fulfillmentMessages": [{"text": {"text": ["No recibí ninguna pregunta."]}}]})

    texto_limpio = limpiar_texto(texto)
    X = vectorizador.transform([texto_limpio])
    pred = modelo.predict_proba(X)
    idx = np.argmax(pred)
    clase = modelo.classes_[idx]
    confianza = pred[0][idx]

    if confianza < 0.40:
        respuesta = "No estoy seguro de eso 🤔. ¿Podrías reformular la pregunta?"
    else:
        respuesta = respuestas.get(clase, "Lo siento, no tengo una respuesta preparada para eso.")

    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [respuesta]}}
        ]
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
