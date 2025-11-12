from flask import Flask, request, jsonify
import re

app = Flask(__name__)

print("🚀 Iniciando Bot Explícamelo Fácil...")

# Base de conocimientos COMPLETA
base_conocimiento = {
    "cdio": "**CDIO** es un modelo educativo innovador que significa: **Concebir, Diseñar, Implementar y Operar**. Es un framework que prepara a los ingenieros para enfrentar desafíos reales del mundo profesional mediante proyectos prácticos y aprendizaje experiencial.",
    
    "mision": "La **Misión** del Programa de Ingeniería Electrónica es formar profesionales integrales con sólidos conocimientos técnicos, capacidad innovadora y compromiso social, que contribuyan al desarrollo tecnológico sostenible del país.",
    
    "vision": "La **Visión** es ser reconocido como uno de los mejores programas de Ingeniería Electrónica a nivel nacional, destacándonos por investigación aplicada y formación de profesionales altamente competitivos.",
    
    "perfil": "El **Ingeniero Electrónico** diseña sistemas electrónicos, desarrolla proyectos de automatización, gestiona redes de comunicación y trabaja en áreas como telecomunicaciones, robótica e Internet de las Cosas (IoT).",
    
    "materias": "El **Plan de Estudios** incluye: Matemáticas, Circuitos, Electrónica Digital, Programación, Telecomunicaciones, Control Automático, Microcontroladores y Proyectos Integradores por semestre.",
    
    "proyeccion": "La **Proyección Social** conecta la universidad con la comunidad mediante proyectos tecnológicos para comunidades vulnerables, asesoría a PYMEs y programas de alfabetización digital."
}

# Palabras clave para cada tema
palabras_clave = {
    "cdio": ["cdio", "concebir", "diseñar", "implementar", "operar", "modelo educativo"],
    "mision": ["misión", "mision", "objetivo", "propósito", "razón de ser"],
    "vision": ["visión", "vision", "futuro", "aspiración", "a dónde vamos"],
    "perfil": ["perfil", "profesional", "qué hace", "campo laboral", "trabajo", "áreas"],
    "materias": ["materias", "asignaturas", "cursos", "plan de estudios", "malla curricular", "pensum"],
    "proyeccion": ["proyección social", "proyeccion social", "comunidad", "impacto social", "responsabilidad social"]
}

def predecir_tema(pregunta):
    """Predice el tema basado en palabras clave"""
    pregunta = pregunta.lower().strip()
    
    # Buscar coincidencias exactas primero
    for tema, palabras in palabras_clave.items():
        for palabra in palabras:
            if palabra in pregunta:
                return tema, 0.9  # Alta confianza
    
    # Búsqueda por similitud parcial
    for tema, palabras in palabras_clave.items():
        for palabra in palabras:
            if any(pal in pregunta for pal in palabra.split()):
                return tema, 0.7  # Confianza media
    
    return "general", 0.3  # Confianza baja

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🤖 Bot 'Explícamelo Fácil' - ACTIVO",
        "status": "online",
        "topics": list(base_conocimiento.keys()),
        "version": "3.0"
    })

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        if request.method == "GET":
            return jsonify({
                "instruction": "Usa POST para enviar preguntas",
                "example": '{"question": "qué es cdio"}'
            })
        
        # Obtener datos JSON
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No se recibió JSON",
                "solution": "Envía: {'question': 'tu pregunta'}"
            }), 400
        
        pregunta = data.get("question", "").strip()
        
        if not pregunta:
            return jsonify({
                "error": "Pregunta vacía",
                "solution": "La pregunta no puede estar vacía"
            }), 400
        
        print(f"📥 Pregunta recibida: {pregunta}")
        
        # Predecir tema
        tema, confianza = predecir_tema(pregunta)
        
        # Generar respuesta
        if tema in base_conocimiento and confianza > 0.5:
            respuesta = {
                "answer": base_conocimiento[tema],
                "detected_topic": tema,
                "confidence": round(confianza, 2),
                "original_question": pregunta,
                "status": "success"
            }
        else:
            respuesta = {
                "answer": "¡Hola! Soy tu asistente de Ingeniería Electrónica 🤖. Puedo explicarte sobre: CDIO, Misión, Visión, Perfil profesional, Materias o Proyección social. ¿Sobre qué tema quieres información?",
                "detected_topic": "bienvenida",
                "confidence": 1.0,
                "original_question": pregunta,
                "available_topics": list(base_conocimiento.keys()),
                "status": "welcome"
            }
        
        print(f"✅ Respuesta enviada: {tema} (confianza: {confianza})")
        return jsonify(respuesta)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            "error": "Error interno",
            "message": "El servicio está funcionando, pero hubo un problema con tu pregunta",
            "status": "error"
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "explicamelo_facil"})

if __name__ == "__main__":
    print("✅ Bot listo en puerto 5000")
    print("🌐 Webhook: /webhook")
    print("📚 Temas disponibles:", list(base_conocimiento.keys()))
    app.run(host="0.0.0.0", port=5000, debug=False)
